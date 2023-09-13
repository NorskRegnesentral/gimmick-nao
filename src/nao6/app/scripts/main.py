#!/usr/bin/env python2
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
import vision_definitions
import os
import qi
import signal
import numpy as np
import cv2
import gimmick_client

class NRGimmickActivity(object):
    "A sample standalone app, that demonstrates simple Python usage"
    APP_ID = "no.nr.gimmick"
    def __init__(self, qiapp):
        self.duration = 0.05
        self.qiapp = qiapp
        self.events = stk.events.EventHelper(qiapp.session)
        self.s = stk.services.ServiceCache(qiapp.session)
        self.logger = stk.logging.get_logger(qiapp.session, self.APP_ID)
        self.gimmick_client = gimmick_client.SimpleGimmickClient()
        signal.signal(signal.SIGINT, self.stop)

    def connectToCamera(self):
        try:
            self.avd = self.s.ALVideoDevice
            camera_num = vision_definitions.kTopCamera
            camera_resolution = vision_definitions.kVGA
            colorspace = vision_definitions.kBGRColorSpace
            fps = 25
            self.client_name = self.avd.subscribeCamera(self.APP_ID,
                                                        camera_num,
                                                        camera_resolution,
                                                        colorspace, fps)
            self.logger.info("Connected to camera")
        except BaseException, err:
            self.logger.error("Could not connect to the camera: {}!".format(err))
        
    def disconnectFromCamera(self):
        try:
            self.avd.unsubscribe(self.client_name)
        except BaseException, err:
            self.logger.error("Could not disconnect from the camera {}!".format(err))

    def getImageFromCamera(self):
        """
        return the image from camera or None on error
        """
        try:
            dataImage = self.avd.getImageRemote(self.client_name)

            if (dataImage != None):
                Image = (
                    np.reshape(
                        np.frombuffer(dataImage[6], dtype='{}uint8'.format( dataImage[2])),
                        (dataImage[1], dataImage[0], dataImage[2]))
                )
                return Image

        except BaseException, err:
            self.logger.error("getImageFromCamera: catching error: {}!".format(err))
        return None;            


    def sendImage(self, image):
#        cv2.imwrite(os.path.join(gimmick_client.SimpleGimmickClient.DIR_PATH, "client_saw.jpg"), image)
        return self.gimmick_client.sendImageData(image)
    
    def blink(self):
        self.s.ALLeds.fadeRGB( "FaceLed0", 0x000000, self.duration, _async=True )
        self.s.ALLeds.fadeRGB( "FaceLed1", 0x000000, self.duration, _async=True )
        self.s.ALLeds.fadeRGB( "FaceLed2", 0xffffff, self.duration, _async=True )
        self.s.ALLeds.fadeRGB( "FaceLed3", 0x000000, self.duration, _async=True )
        self.s.ALLeds.fadeRGB( "FaceLed4", 0x000000, self.duration, _async=True )
        self.s.ALLeds.fadeRGB( "FaceLed5", 0x000000, self.duration, _async=True )
        self.s.ALLeds.fadeRGB( "FaceLed6", 0xffffff, self.duration, _async=True )
        self.s.ALLeds.fadeRGB( "FaceLed7", 0x000000, self.duration, _async=True )
        

    def try_picture(self, *args):
        if args[0] != 0:
            return
        self.s.ALTextToSpeech.setLanguage("English")
        self.s.ALTextToSpeech.say("Click...")
        qi.async(self.blink)
        image = self.getImageFromCamera()
        if not image is None:
            self.logger.info("Sending image...")
            fut = qi.async(self.sendImage, image)
            fut.addCallback(self.future_judge)

    def future_judge(self, fut):
        val = fut.value()
        color = 0xffffff
        if val == "paper":
            color = 0x00ff00
        elif val == "scissors":
            color = 0xff7f00
        elif val == "rock":
            color = 0x0000ff
        else:
            color = 0xff00ff
        self.s.ALLeds.fadeRGB( "FaceLeds", color, self.duration, _async=True )                
        self.s.ALTextToSpeech.setLanguage("English")
        self.s.ALTextToSpeech.say("I thought I saw a {}".format(val))
        self.logger.info("judge said {}".format(val))

    def do_shutdown(self, *args):
        if args[0] != 0:
            return
        self.stop()

    def clearEyes(self):
        self.s.ALLeds.fadeRGB( "FaceLeds", 0xffffff, self.duration, _async=True )

    def swap_stand_sit(self, *args):
        if args[0] != 0:
            return
        self.clearEyes()
        current_posture = self.s.ALRobotPosture.getPostureFamily()
        self.logger.info("current posture is {}".format(current_posture))
        new_posture = "Sit" if current_posture == "Standing" else "Stand"
        self.logger.info("Go to new posture: {}".format(new_posture))
        qi.async(self.s.ALRobotPosture.goToPosture, new_posture, 0.6)
        
    def on_start(self):
        "Ask to be touched, waits, and exits."
        self.connectToCamera()        
        self.events.connect("FrontTactilTouched", self.try_picture)
        self.events.connect("HandRightBackTouched", self.try_picture)
        self.events.connect("RearTactilTouched", self.swap_stand_sit)
        self.clearEyes()

        
    def stop(self):
        self.disconnectFromCamera()
        self.clearEyes()
        self.s.ALTextToSpeech.setLanguage("English")
        self.s.ALTextToSpeech.say("Stopping gimmick")
        self.qiapp.stop()

    def on_stop(self):
        self.logger.info("Application finished.")
        self.events.clear()

if __name__ == "__main__":
    stk.runner.run_activity(NRGimmickActivity)
