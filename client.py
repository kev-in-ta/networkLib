import socket
import datetime
import time
from cobs import cobs
import bluetooth

class ClWirelessClient:
    """
    Class for establishing wireless communications.
    """

    def __init__(self, host, port, protocol='TCP'):
        """
        Purpose:	Initialize various sensors
        Passed: 	Optionally the communication protocol
        """

        # Stores protocol in class variable
        self.protocol = protocol

        # Initiates various socket connections based on passed protocol
        if self.protocol == 'TCP':
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(10)
            self.socket.connect((host, port))
            print('Connected.')

        elif self.protocol == 'UDP':
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.socket.connect((host, port))

        elif self.protocol == 'BT':
            self.sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.sock.bind(('', 3))
            self.sock.listen(1)
            self.socket, self.address = self.sock.accept()

    def fnSendMessage(self, message):
        """
        Purpose:
        Passed:
        """

        # Encode message using constant oversized buffering
        dataCobs = cobs.encode(message)

        # Send encoded message through socket
        self.socket.send(dataCobs)

        # Send a 0 value to signal end of message
        if self.protocol == ('TCP' or 'BT'):
            self.socket.send(b'\x00')

    def fnShutDown(self):
        """
        Purpose:	Shutdown sockets
        Passed: 	None
        """

        print('Closing Socket')
        try:
            self.socket.close()
            self.sock.close()
        except Exception as e:
            print(e)

# MAIN PROGRAM

if __name__ == "__main__":

    host = '192.168.43.14'
    port = 65432

    # Continously try to reconnect if connection fails
    while True:

        connectedStatus = False

        try:
            print('Connecting to computer...')
            instWirelessClient = ClWirelessClient(host, port)
            connectedStatus = True

            while True:
                message = b'This is my message!'
                time.sleep(1)
                instWirelessClient.fnSendMessage(message)

        except Exception as e:
            time.sleep(1)
            # Shutdown sockets if necessary
            if connectedStatus:
                instWirelessClient.fnShutDown()
                connectedStatus = False
            print(e)

        pass