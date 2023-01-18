import socket
import config
from lexator import lexator
import threading
import sys
import os

class Conn:
    def __init__(self, address: tuple = ('localhost', 28900), simultaneous_conn: int = 10) -> None:
        # Create a TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # bind the socket
        self.address = address
        self.sock.bind(self.address)
        # listen of incomming connections
        self.sock.listen(simultaneous_conn)
        self.CLIENTS = []
        if config.DEBUG:
            print("starting conection on {}:{}".format(*self.address))
    def manage_protocol(self) -> None:
        while True:
            try:
                self.connection, self.client_address = self.sock.accept()
                if self.client_address not in self.CLIENTS:
                    self.CLIENTS.append(self.client_address)
                print("Connection from: " + str(self.client_address))
                try:
                    threading.Thread(target=self.on_new_client,
                                    args=(config.receive_buffer,)).start()
                except KeyboardInterrupt:
                    self.connection.close()
            except ConnectionResetError:
                pass

    def on_new_client(self, buffer: int = 1024):
        client = self.address
        while True:
            # receive data stream. it won't accept data packet greater than 1024 bytes
            data = self.connection.recv(buffer)
            data_formated = lexator(data)
            msg = ""

            try:
                if data_formated[0] == "remove":
                    self.CLIENTS.remove(self.client_address)
                    self.disconnect_client(self.client_address)
                    break
            except IndexError:
                pass
            
            if any('s' in item[0] for item in data_formated) and any('t' in item[0] for item in data_formated):
                target = ()
                for param in data_formated:
                    if "s" in param:
                        msg = str(param[1])
                    if "t" in param:
                        addr = str(param[1])
                                        
                '''
                REPAIR
                '''
                for address in self.CLIENTS:
                    print(address)
                    if addr == address[0]:
                        target = address 
                        print(target)
                try:
                    if config.DEBUG:
                        print("{} > {}".format(client, msg))
                    self.sock.sendto(bytes(msg, 'UTF-8'), target)
                    self.sock.connect(client);
                except socket.error as error:
                    print(error)
                    pass
                
                
    def send_message(self, msg: str, target: str, sender: str):
        try:
            if config.DEBUG:
                print("{} > {}".format(sender[0], msg))
            self.sock.sendto(bytes(msg, 'UTF-8'), target)
        except socket.error as error:
            print(error)
            pass
        
    def disconnect_client(self, target: str):
        print("Client: {} disconnected from {}".format(*(target, self.address)))
            
    def check_connections(self):
        try:
            for client in self.CLIENTS:
                pass
        except:
            pass


if __name__ == '__main__':
    if config.DEBUG:
        conn = Conn((config.server_ip, config.server_port))
        conn.manage_protocol()
