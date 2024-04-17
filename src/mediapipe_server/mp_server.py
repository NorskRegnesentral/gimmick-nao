#!/usr/bin/env python3

import fnmatch
import os
import cv2
import time
import numpy as np
import zmq
import gimmick_model.recognitionmodel

class GimmickServer():
    BASE_DIR = os.path.join(os.path.sep, "var", "run", "user", str(os.getuid()))
    DIR_PATH = os.path.join(BASE_DIR, "no.nr.gimmick") if os.path.exists(BASE_DIR) else os.path.join(os.path.sep, "tmp", "no.nr.gimmick")

    def __init__(self):
        """
        Initialize the server and get ready for getting images
        """
        self.test_and_make_dir()
        self.recognitionModel = gimmick_model.recognitionmodel.RecognitionModel()
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        self.socket.bind("ipc://" + os.path.join(GimmickServer.DIR_PATH, "gimmick_local_socket"))

    def receive_image(self, flags = 0, copy = True, track = False) -> np.ndarray:
        metadata = self.socket.recv_json(flags=flags)
        blob = self.socket.recv(flags=flags, copy=copy, track=track)
        image = np.frombuffer(bytes(memoryview(blob)), dtype=metadata['dtype'])
        image = image.reshape(metadata['shape'])
        return image
        
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
        _, result_str, _  = self.recognitionModel.get_hand_landmarks((image,), draw_landmarks=False)
        return result_str

    def send_result(self, result: str) -> None:
        self.socket.send_string(result)
        

def save_picture(image: np.ndarray):
    DateMask = "%Y-%m-%dT%H_%M"
    MachineName = os.uname().nodename
    timestr = time.strftime(DateMask)
    filename = f"gimmick-{MachineName}-{timestr}.jpg"
    file_path = os.path.join(GimmickServer.DIR_PATH, filename)
    dup_count = 1
    while os.path.exists(file_path):
        file_name = f"gimmick-{MachineName}-{timestr}-{dup_count}.jpg"
        file_path = os.path.join(GimmickServer.DIR_PATH, file_name)
        dup_count += 1

    cv2.imwrite(file_path, image)


if __name__ == "__main__":
    server = GimmickServer()
    save_pictures = False

    while True:
        image = server.receive_image()
        result = server.process_image(image)
        server.send_result(result)
        if save_pictures:
            save_picture(image)
