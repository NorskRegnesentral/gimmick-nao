#!/usr/bin/env python3

import os
import zmq
from typing import List
import numpy as np

class GimmickServer():
    DIR_PATH = os.path.join(os.path.sep, "var", "run", "user", str(os.getuid()), "no.nr.gimmick")
    if not os.path.exists(os.path.join(os.path.sep, "var", "run" "user")):
        DIR_PATH = os.path.join(os.path.sep, "tmp", "no.nr.gimmick")

    def __init__(self):
        """
        Initialize the server and get ready for getting images
        """
        self.test_and_make_dir()
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        self.socket.bind("ipc://" + os.path.join(GimmickServer.DIR_PATH, "gimmick_local_socket"))

    def begin_receive(self, flags = 0, copy = True, track = False) -> np.ndarray:
        metadata = self.socket.recv_json(flags=flags)
        blob = self.socket.recv(flags=flags, copy=copy, track=track)
        image = np.frombuffer(bytes(memoryview(blob)), dtype=metadata['dtype'])
        image = image.reshape(metadata['shape'])

    def test_and_make_dir(self) -> None:
        """
        Making a directory for aiding the communication between the server and
        remote. The method creates the directory in /tmp if it doesn't already exist.
        """
        print(f"does {GimmickServer.DIR_PATH} exist?")

        if not os.path.exists(GimmickServer.DIR_PATH):
            print("No, make it")
            os.makedirs(GimmickServer.DIR_PATH)


    def process_image(self, image: np.ndarray) -> str:
        return "rock"

    def send_result(self, result: str):
        self.socket.send_string(result)
        

if __name__ == "__main__":
    server = GimmickServer()
    while True:
        image = server.begin_receive()
        result = server.process_image(image)
        server.send_result(result)
