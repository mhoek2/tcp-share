# app core modules
from typing import TYPE_CHECKING, TypedDict
from modules.app.settings import Settings

import socket
import json
import subprocess
import platform
import base64

if TYPE_CHECKING:
    from main import Application

class TCP:

    class Server_t(TypedDict):
        ip: str
        port: int

    def __init__( self, context ) -> None:
        self.context : "Application" = context;
        self.settings : Settings = context.settings

        # Get the LAN IP address of the device
        self.set_local_ip()

    def set_local_ip( self ):
        """Try to get the LAN IP address of the host device"""
        try:
            # Create a temporary socket
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            # Connect to an external address (this won't actually send packets)
            s.connect(('8.8.8.8', 80))  # Using Google DNS as an external address
            self.settings.server_ip = s.getsockname()[0]  # Get the local IP address
        finally:
            s.close()

    # server
    def respond( self, c, send_data ):
        c.send( json.dumps( send_data ).encode() )
        c.close()  

    def start_server( self ) -> None:
        """Starts the TCP socker server, use this function as target in a dedicated thread, as it operates in an infinite loop. 
        This ensures the server can handle incoming connections concurrently 
        without blocking the main thread."""

        s = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
        print( f"Start server on: {self.settings.server_ip}:{self.settings.tcp_port} ")

        s.bind( (self.settings.server_ip, self.settings.tcp_port) )
        s.listen(5)

        while True:
            c, addr = s.accept()
            print( f"Connection from: {addr[0]}:{addr[1]}" )
            c.send( b"Welcome client!" )

            received = c.recv( self.settings.bufsize_payload ).decode('utf-8')
            rcv_data = json.loads( received )

            # check if this is a valid request
            if not 'action' in rcv_data:
                self.respond( c, { 'error': 'Invalid request' } )
                continue

            _action = rcv_data['action']

            # only allow 'get_allow_receive' request without allowConnection check
            if _action == "get_allow_receive":
                print( f"request get_allow_receive" )
                self.respond( c, { 'value': self.settings.allowConnection } )
                continue

            elif not self.settings.allowConnection:
                self.respond( c, { 'error': 'I do not allow connections!!' } )
                continue

            # clear local files request, assuming incoming files.
            if _action == "clear_all_files":
                state = True

                # skip if request is local.
                if addr[0] == self.settings.server_ip:
                    state = False

                if state:
                    self.context.read_write.removeTransferFiles()
                    self.context.read_write.removePdfFiles()
                    self.context.read_write.removeQRFiles()

                self.respond( c, { 'value': state } )
                continue

            # request to store a file
            elif _action == "store_file":
                file = rcv_data['file']
                print( f"received file: {file}" )
                filename = file['filename']
                content = file['contents']

                if file['is_bytes']:
                    print("write bytes")
                    content_bytes = base64.b64decode( content )
                    self.context.read_write.writePdfFile( filename, content_bytes )
                else:
                    self.context.read_write.writeTextFile( filename, content )

                self.context.log.log_file( filename, f"Received from: {addr[0]}" )
                self.respond( c, { 'success': 'File received successfully!' } )
                continue

        return

    # client
    def client_connect( self, server : Server_t, timeout=10 ) -> None:
        """Connect to a socket stream and return the instance, or False on timeout

           Parameters
           ----------
           server : tuple
                0: IP address
                1: TCP port
           timeout : int    *optional
                The maximum time in seconds before timeout is hit

           Returns
           -------
           socket: If valid connection returns socket instance
           bool: False if timeout is hit (Failed to connect)
        """
        s = socket.socket()
        s.settimeout(timeout)

        try:
            s.connect( ( server['ip'], server['port'] ) )
 
            received = s.recv( self.settings.bufsize_meta ).decode('utf-8')
 
            print(received)
        except socket.timeout:
            self.client_disconnect( s )
            return False

        return s

    def client_disconnect( self, s ) -> None:
        """Close the connection to a socket instance

           Parameters
           ----------
           s : socket
                The socket instance of the closing stream
           
        """
        s.close()

    def client_send_file( self, server : Server_t, filename : str, content : str ):
        """Connect to a socket stream and send over a file, then close the stream

           Parameters
           ----------
           server : tuple
                0: IP address
                1: TCP port
           filename : str
                The filename of the file that is sent
           content : str
                The content of the file that is sent
        """
        s = self.client_connect( server )

        if s == False:
            return False 

        is_bytes = False

        if isinstance( content, bytes ):
            is_bytes = True
            content = base64.b64encode(content).decode('utf-8') 

        send_data = {
            'action' : 'store_file',
            'file': {
                    'filename': filename,
                    'is_bytes': is_bytes,
                    'contents': content
                }
            }

        s.sendall( bytes( json.dumps( send_data ) + "\n", "utf-8" ) ) # Send data
        
        received = s.recv( self.settings.bufsize_meta ).decode('utf-8')
        rcv_data = json.loads( received )

        if 'success' in rcv_data:
            print( rcv_data['success'] )

        if 'error' in rcv_data:
            print( rcv_data['error'] )

        self.client_disconnect( s )

    def get_boolean( self, server : Server_t, parameter ):
       """Connect to a socket stream and request a boolean state, then close the stream

           Parameters
           ----------
           server : tuple
                0: IP address
                1: TCP port
           parameter : str
                The key the server needs to reply the requested boolean state

           Returns
           -------
           bool : State returned by the server, or False if request timedout
       """
       s = self.client_connect( server, 0.5 )

       if s == False:
            return False 

       s.sendall( bytes( json.dumps( { 'action' : parameter } ) + "\n", "utf-8" ) ) # Send data
       
       received = s.recv( self.settings.bufsize_meta ).decode('utf-8')
       rcv_data = json.loads( received )

       self.client_disconnect( s )

       return bool( rcv_data['value'] ) if 'value' in rcv_data else False

    def get_allow_receive( self, server : Server_t ):
        """Connect to a socket stream and request a boolean state, then close the stream

           Parameters
           ----------
           server : tuple
                0: IP address
                1: TCP port

           Returns
           -------
           bool : State of the server allows connections checkbox, or False if request timedout
        """
        return self.get_boolean( server, "get_allow_receive" )

    def server_clear_files( self, server: Server_t ):
        """Connect to a socket stream and request a boolean state, then close the stream

           Parameters
           ----------
           server : tuple
                0: IP address
                1: TCP port

           Returns
           -------
           bool : If the server successfully clear all files
        """
        return self.get_boolean( server, "clear_all_files" )

    # ping device
    def ping_device(self, host, network_timeout=1):
        """Send a ping packet to the specified host, using the system "ping" command.
          
           Parameters
           ----------
           server : tuple
                0: IP address
                1: TCP port

           Returns
           -------
           bool : True if device is reachable
        """
        args = [
            'ping'
        ]

        platform_os = platform.system().lower()

        if platform_os == 'windows':
            args.extend(['-n', '1'])
            args.extend(['-w', str(network_timeout * 1000)])
        elif platform_os in ('linux', 'darwin'):
            args.extend(['-c', '1'])
            args.extend(['-W', str(network_timeout)])
        else:
            raise NotImplemented('Unsupported OS: {}'.format(platform_os))

        args.append(host)

        try:
            if platform_os == 'windows':
                output = subprocess.run(args, check=True, universal_newlines=True, stdout=subprocess.PIPE ).stdout

                if output and 'TTL' not in output:
                    return False
            else:
                subprocess.run(args, check=True)

            return True
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
            return False