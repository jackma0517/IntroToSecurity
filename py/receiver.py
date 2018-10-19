import socket
import threading
import errno
import struct
import logging
from encryption import Encryption


class Receiver(threading.Thread):
    """
    This thread abstracts all the socket communication between
    the client and the server using a queue. 
    It is responsible for receiving messages through the socket
    and inserting them into the queue
    """

    def __init__(self, socket, queue):
        logging.info('Initializing receiver thread...')
        threading.Thread.__init__(self)
        self.socket = socket
        self.queue = queue
        self.socket.setblocking(False) 
        self.keep_alive = True
        self.authentication = False
        self.key = None

    def run(self):
        while (self.keep_alive):
            try:
                data = self.socket.recv(1024)
                if (data):
                    if self.authentication:
                        #dont use hmac version
                        #data = Encryption.decryptVerify(data, self.key)
                        data = Encryption.decrypt(data, self.key)
                    logging.info('Reciever received from socket: ' + str(data))
                    self.queue.put(data)
            except Exception as e:
                logging.info('Receiver exception: ' + str(e))
                continue
            
    def completeAuthentication(self, key):
        self.authentication = True
        self.key = key

    def close(self):
        self.keep_alive = False
