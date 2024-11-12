# app core modules
from modules.app.settings import Settings

import socket
import json

class TCP:
    def __init__( self, context ) -> None:
        self.context = context;
        self.settings : Settings = context.settings

        # Get the LAN IP address of the device
        self.set_local_ip()

    def set_local_ip( self ):
        try:
            # Create a temporary socket
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            # Connect to an external address (this won't actually send packets)
            s.connect(('8.8.8.8', 80))  # Using Google DNS as an external address
            self.settings.server_ip = s.getsockname()[0]  # Get the local IP address
        finally:
            s.close()

    # server
    def start_server( self ) -> None:
        s = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
        print( f"Start server on: {self.settings.server_ip}:{self.settings.tcp_port} ")

        s.bind( (self.settings.server_ip, self.settings.tcp_port) )
        s.listen(5)

        while True:
            c, addr = s.accept()
            print( f"Connection from: {addr[0]}:{addr[1]}" )
            c.send( b"Welcome client!" )

            received = str(c.recv(1024), "utf-8") 

            rcv_data = json.loads( received )

            send_data = { }

            if 'action' in rcv_data:
                # request to store a file
                if rcv_data['action'] == "store_file":
                    if self.settings.allowConnection:
                        print( f"received file: {rcv_data['file']}" )
                        send_data = { 'success': 'File received successfully!' }
                    else:
                        print("Connections is refused!")
                        send_data = { 'error': 'I do not allow connections!!' }

                # request to return a value
                if rcv_data['action'] == "get_allow_receive":
                    print( f"request get_allow_receive" )
                    send_data = { 'value': False }
                    
            c.send( json.dumps( send_data ).encode() )
            c.close()   
        return

    # client
    def client_connect( self, server ) -> None:
        s = socket.socket()
        s.connect( ( server[0], server[1] ) )

        received = str( s.recv(1024), "utf-8" ) 
        print(received)

        return s

    def client_disconnect( self, s ) -> None:
        s.close()

    def client_send_file( self, server, filename : str, content : str ):
        s = self.client_connect( server )

        send_data = {
            'action' : 'store_file',
            'file': {
                    'filename': filename,
                    'content': content
                }
            }

        s.sendall( bytes( json.dumps( send_data ) + "\n", "utf-8" ) ) # Send data
        
        rcv_data = json.loads( str( s.recv(1024), "utf-8" ) )
        
        if 'success' in rcv_data:
            print( rcv_data['success'] )

        if 'error' in rcv_data:
            print( rcv_data['error'] )

        self.client_disconnect( s )

    def get_boolean( self, server, parameter ):
       s = self.client_connect( server )

       s.sendall( bytes( json.dumps( { 'action' : parameter } ) + "\n", "utf-8" ) ) # Send data
       
       received = json.loads( str( s.recv(1024), "utf-8" ) )

       self.client_disconnect( s )
       return bool( received['value'] )

    def get_allow_receive( self, server ):
        state = self.get_boolean( server, "get_allow_receive" )

        if state:
            print("YES")
        else:
            print("NO")

        return

    def update( self ):
        print("-")