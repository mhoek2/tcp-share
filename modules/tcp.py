# app core modules
from modules.app.settings import Settings

import socket
import json

class TCP:
    def __init__( self, context ) -> None:
        self.context = context;
        self.settings : Settings = context.settings

    # server
    def start_server( self ) -> None:
        s = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
        host = self.settings.server_ip
        port = self.settings.tcp_port

        print( f"Start server on: {host}:{port} ")

        s.bind( (host, port) )
        s.listen(5)

        while True:
            c, addr = s.accept()
            print( f"Connection from: {addr[0]}:{addr[1]}" )
            c.send( b"Welcome client!" )

            received = str(c.recv(1024), "utf-8") 

            rcv_data = json.loads( received )

            if rcv_data['action']:
                # request to store a file
                if rcv_data['action'] == "store_file":
                    print( f"received file: {rcv_data['file']}" )

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