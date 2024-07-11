# Robot Controller
# An attempt to make the some of the robot parts be by itself by itself

import stk.services
import qi

class RobotController(object):
    __posture_speed = 0.6
    __blink_duration = 0.05

    def __init__(self, event_helper, service_cache: stk.services.ServiceCache, logger):
        self.events = event_helper
        self.s = service_cache
        self.logger = logger

    def readyRobot(self):
        self.s.ALAutonomousLife.setState("solitary");
        # self.go_sit();
        
        self.logger.info("connected and ready!")

    def connectEvent(self, eventName, method):
        self.events.connect(eventName, method)

    def blink(self):
        self.s.ALLeds.fadeRGB( "FaceLed0", 0x000000, RobotController.__blink_duration, _async=True )
        self.s.ALLeds.fadeRGB( "FaceLed1", 0x000000, RobotController.__blink_duration, _async=True )
        self.s.ALLeds.fadeRGB( "FaceLed2", 0xffffff, RobotController.__blink_duration, _async=True )
        self.s.ALLeds.fadeRGB( "FaceLed3", 0x000000, RobotController.__blink_duration, _async=True )
        self.s.ALLeds.fadeRGB( "FaceLed4", 0x000000, RobotController.__blink_duration, _async=True )
        self.s.ALLeds.fadeRGB( "FaceLed5", 0x000000, RobotController.__blink_duration, _async=True )
        self.s.ALLeds.fadeRGB( "FaceLed6", 0xffffff, RobotController.__blink_duration, _async=True )
        self.s.ALLeds.fadeRGB( "FaceLed7", 0x000000, RobotController.__blink_duration, _async=True )
        
    def clearEyes(self):
        self.s.ALLeds.fadeRGB( "FaceLeds", 0xffffff, RobotController.__blink_duration, _async=True )

    def changeEyeColor(self, color):
        self.s.ALLeds.fadeRGB( "FaceLeds", color, RobotController.__blink_duration, _async=True )

    def swap_stand_sit(self, *args):
        if args[0] != 0:
            return
        self.clearEyes()
        current_posture = self.get_posture()
        self.logger.info("current posture is {}".format(current_posture))
        new_posture = "Sit" if current_posture == "Standing" else "Stand"
        self.logger.info("Go to new posture: {}".format(new_posture))
        qi.runAsync(self.s.ALRobotPosture.goToPosture, new_posture, RobotController.__posture_speed)

    def go_sit(self):
        return qi.runAsync(self.s.ALRobotPosture.goToPosture, "Sit", RobotController.__posture_speed)


    def get_posture(self):
        return self.s.ALRobotPosture.getPostureFamily()

    def go_stand(self):
        return qi.runAsync(self.s.ALRobotPosture.goToPosture, "Stand", RobotController.__posture_speed)
        
