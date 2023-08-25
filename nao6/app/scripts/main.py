"""
A sample showing how to make a Python script as an app.
"""

__version__ = "0.0.8"

__copyright__ = "Copyright 2023, Norsk Regnesentral"
__author__ = 'Trenton Schulz'
__email__ = 'trenton@nr.no'

import stk.runner
import stk.events
import stk.services
import stk.logging
import numpy as np
import cv2

class NRGimmickActivity(object):
    "A sample standalone app, that demonstrates simple Python usage"
    APP_ID = "no.nr.gimmick"
    def __init__(self, qiapp):
        self.qiapp = qiapp
        self.events = stk.events.EventHelper(qiapp.session)
        self.s = stk.services.ServiceCache(qiapp.session)
        self.logger = stk.logging.get_logger(qiapp.session, self.APP_ID)

    def connectToCamera(self):
        try:
            self.avd = self.s.ALVideoDevice
            camera_num = 0 # Camera on the Top (AL::kTopCamera)
            camera_resolution = 2 # 640x480 (AL:kVGA)
            colorspace = 13 # BGR (AL::kBGRColorSpace)
            fps = 5 # We'll start low for now.
            self.client_name = self.avd.subscribeCamera(self.APP_ID,
                                                        camera_num,
                                                        camera_resolution,
                                                        colorspace, fps)
            self.logger.info("Connected to camera")
        except BaseException, err:
            self.logger.error("Could not connect to the camera: %s!" % err)
        
    def disconnectFromCamera(self):
        try:
            self.avd.unsubscribe(self.client_name)
        except BaseException, err:
            self.logger.error("Could not disconnect from the camera %s!" % err)

    def getImageFromCamera(self):
        """
        return the image from camera or None on error
        """
        try:
            dataImage = self.avd.getImageRemote(self.client_name)

            if (dataImage != None):
                Image = (
                    np.reshape(
                        np.frombuffer(dataImage[6], dtype='%iuint8' % dataImage[2]),
                        (dataImage[1], dataImage[0], dataImage[2]))
                )
                return Image

        except BaseException, err:
            self.logger.error("getImageFromCamera: catching error: %s!" % err)
        return None;            

    def try_picture(self, *args):
        if args[0] != 0:
            return
        self.s.ALTextToSpeech.say("Click...")
        x = self.getImageFromCamera()
        if not x is None:
            cv2.imwrite("test-image.jpg", x)


    def do_shutdown(self, *args):
        if args[0] != 0:
            return
        self.stop()
        
    def on_start(self):
        "Ask to be touched, waits, and exits."
        # Two ways of waiting for events
        # 1) block until it's called

        self.s.ALTextToSpeech.setLanguage("English")
        self.s.ALTextToSpeech.say("Starting gimmick.")


        self.events.connect("FrontTactilTouched", self.try_picture)
        self.events.connect("HandRightBackTouched", self.try_picture)
        self.events.connect("RearTactilTouched", self.do_shutdown)
        self.connectToCamera()        

    def stop(self):
        self.disconnectFromCamera()
        self.s.ALTextToSpeech.say("Stopping gimmick")
        "Standard way of stopping the application."
        self.qiapp.stop()

    def on_stop(self):
        "Cleanup"
        self.logger.info("Application finished.")
        self.events.clear()

if __name__ == "__main__":
    stk.runner.run_activity(NRGimmickActivity)
