#!/usr/bin/env python3
"""
A sample showing how to make a Python script as an app.
"""

__version__ = "0.5"

__copyright__ = "Copyright 2024, Norsk Regnesentral"
__author__ = 'Trenton Schulz'
__email__ = 'trenton@nr.no'

import stk.runner
import stk.events
import stk.services
import stk.logging
import functools
import qi
import translator
import gamecontroller
import robotcontroller


class NRGimmickActivity(object):
    "A sample standalone app, that demonstrates simple Python usage"
    APP_ID = "no.nr.gimmick"

    def __init__(self, qiapp):
        self.qiapp = qiapp
        self.memory_service = qiapp.session.service("ALMemory")
        service_cache = stk.services.ServiceCache(qiapp.session)
        self.logger = stk.logging.get_logger(qiapp.session, self.APP_ID)
        self.translator = translator.Translator(service_cache.ALTextToSpeech,
                                                ['en', 'nb'], 'nb')
        self.robot_controller = robotcontroller.RobotController(
            stk.events.EventHelper(qiapp.session), service_cache, self.logger)
        self.game_controller = gamecontroller.GameController(
            self.translator, self.robot_controller, service_cache, self.logger)
        self.left_arm_pressed = False
        self.front_head_pressed = False

    def onTouched(self, strVarName, values):
        for part in values:
            if part[0] == "Head/Touch/Front":
                self.front_head_pressed = part[1]
            elif part[0] == "LArm":
                self.left_arm_pressed = part[1]

        if self.left_arm_pressed and self.front_head_pressed:
            self.stop(0)

    def on_start(self):
        self.game_controller.connectToCamera()
        self.robot_controller.readyRobot()
        self.touch = self.memory_service.subscriber("TouchChanged")
        self.id = self.touch.signal.connect(functools.partial(self.onTouched,
                                                              "TouchChanged"))

        self.robot_controller.connectEvent(
            "RearTactilTouched",
            self.robot_controller.swap_stand_sit)
        self.robot_controller.connectEvent("MiddleTactilTouched",
                                           self.swap_languages)
        self.robot_controller.connectEvent("RightBumperPressed", self.play_rps)

        self.robot_controller.blink()
        self.robot_controller.clearEyes()
        self.translator.translated_say("started")

    def play_rps(self, *args):
        if args[0] != 0 or self.game_controller.currently_playing:
            return
        if self.robot_controller.get_posture() != "Standing":
            self.translator.translated_say("must_stand")
            self.robot_controller.go_stand().wait()
        self.translator.translated_say("lets_play")
        self.game_controller.play_round()

    def swap_languages(self, *args):
        if args[0] != 0:
            return

        if self.translator.language == 'en':
            self.translator.language = 'nb'
        else:
            self.translator.language = 'en'

        qi.runAsync(self.translator.translated_say, "change_language")

    def stop(self, *args):
        if args[0] != 0:
            return
        self.logger.info("User initiated stop")
        self.translator.translated_say('stopping')
        self.qiapp.stop()

    def on_stop(self):
        "Cleanup"
        self.game_controller.disconnectFromCamera()
        self.robot_controller.clearEyes()
        self.logger.info("Application finished.")
        self.events.clear()


if __name__ == "__main__":
    stk.runner.run_activity(NRGimmickActivity)
