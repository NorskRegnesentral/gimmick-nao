# 
# 
from __future__ import print_function
import os
import zmq
from zmq.eventloop import zmqstream

class SimpleGimmickClient(object):
    """A simple client for ZeroMQ that connects to a well known socket,
    sends our image data, and waits for a response with the type"""
    BASE_DIR = os.path.join(os.path.sep, "var", "run", "user", str(os.getuid()))
    DIR_PATH = os.path.join(BASE_DIR, "no.nr.gimmick") if os.path.exists(BASE_DIR) else os.path.join(os.path.sep, "tmp", "no.nr.gimmick") 

    def __init__(self):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        self.socket.connect("ipc://" + os.path.join(SimpleGimmickClient.DIR_PATH, "gimmick_local_socket"))

    def sendImageData(self, image):
        """Send the numpy array to the server and return the
        result of what it thinks it is"""
        metadata = dict(dtype = str(image.dtype), shape=image.shape)
        self.socket.send_json(metadata, zmq.SNDMORE)
        self.socket.send(image, 0)

        message = self.socket.recv()
        print("Received reply [ {} ]".format(message))
        return message
