import sys
import socket
import config

class Client:
    def __init__(self, address: tuple = ('localhost', 28900)) -> None:
        # Create a TCP/IP socket
        self.sock = socket.socket() #socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.address = address
        self.connected = False
        try:
            self.sock.connect(self.address)
            if config.DEBUG:
                print('Starting up on {} port {}'.format(*self.address))
            self.connected = True
        except OSError:
            print("Server might be down")
        
    def client_loop(self):
        if self.connected:
            while True:
                try:
                    if config.DEBUG:
                        data = bytes(input("> "), 'UTF-8')
                        self.sock.send(data)
                except OSError as e:
                    print(e)
                    pass    
        else:
            print('Connetion was not stablished ')
if __name__ == '__main__':
    if config.DEBUG:
        cliente = Client((config.server_ip, config.server_port))
        cliente.client_loop()