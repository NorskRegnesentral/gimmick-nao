# GameController
# An attempt to make the "game mechanics" by itself

import stk.services
import qi

import random
import translator
# import vision_definitions
import numpy as np
import gimmick_model.recognitionmodel
import robotcontroller

class GameController(object):
    APP_ID = "no.nr.gimmick"
    decision_translations = ["lose_game", "win_game", "tie_game", "unknown_game"]
    
    # Given how the indices are selected we can determine the
    # winner/loser/tie by subtracting the indexes from each
    # other. The basics are: Player wins: -1 or 2 Computer
    # wins: 1 or -2 Tie: 0 This can be verified with a truth
    # table built out of the indices and subtraction.
    # |              | Rock (index 0) | Paper (index 1) | Scissors (index 2) |
    # | Rock (0)     |              0 |              -1 |                 -2 |
    # | Paper (1)    |              1 |               0 |                 -1 |
    # | Scissors (2) |              2 |               1 |                  0 |

    game_states_to_translation = {-100: 3,  # unknown
                                  -2: 0,  # Computer wins
                                  -1: 1,  # Player wins
                                  0: 2,  # Tie
                                  1: 0,  # Computer wins
                                  2: 1}  # Player wins

    def __init__(self, translator, robot_controller, service_cache, logger):
        # type: (translator.Translator, robotcontroller.RobotController, stk.services.ServiceCache, qi.logging.Logger)
        self.translator = translator
        self.robot_controller = robot_controller
        self.choices = ["rock", "paper", "scissors"]
        self._current_choice = ""
        self._currently_playing = False
        self.s = service_cache
        self.logger = logger
        self.gimmick_model = gimmick_model.recognitionmodel.RecognitionModel()

    def get_robot_choice(self):
        #type: -> str
        return self._current_choice

    def set_robot_choice(self, new_choice):
        # type: (str)
        self._current_choice = new_choice

    robot_choice = property(get_robot_choice, set_robot_choice)

    def get_currently_playing(self):
        # type: -> bool
        return self._currently_playing
    
    currently_playing = property(get_currently_playing)
    
    def connectToCamera(self):
        try:
            self.avd = self.s.ALVideoDevice
            camera_num = 0 # vision_definitions.kTopCamera
            camera_resolution = 1 # vision_definitions.kVGA
            colorspace = 13 # vision_definitions.kBGRColorSpace
            fps = 25
            self.client_name = self.avd.subscribeCamera(GameController.APP_ID,
                                                        camera_num,
                                                        camera_resolution,
                                                        colorspace, fps)
            self.logger.info("Connected to camera")
        except BaseException as err:
            self.logger.error("Could not connect to the camera: {}!".format(err))
        
    def disconnectFromCamera(self):
        try:
            self.avd.unsubscribe(self.client_name)
        except BaseException as err:
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

        except BaseException as err:
            self.logger.error("getImageFromCamera: catching error: {}!".format(err))
        return None;         


    def predictImage(self, image):
        # type: () -> str
        _, result, _ = self.gimmick_model.predict((image,), draw_landmarks=False)
        return result
    

    def try_picture(self, *args):
        if args[0] != 0:
            return
        self.translator.translated_say("click")
        qi.runAsync(self.robot_controller.blink)
        self.take_picture()

    def take_picture(self, *args):
        self.logger.info("Taking picture...")
        image = self.getImageFromCamera()
        if not image is None:
            self.logger.info("Sending image...")
            qi.runAsync(self.predictImage, image).addCallback(self.future_judge)
            qi.runAsync(self.translator.translated_say, "lets_see")

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

        result = -100
        if color != 0xff00ff and len(self.current_choice) > 0:
            choice_index = self.choices.index(self.current_choice)
            player_index = self.choices.index(val)
            result = choice_index - player_index
            self.logger.info("Got result {} Robot {} player {}".format(result, self.choices[choice_index], val))
            
        self.robot_controller.changeEyeColor(color)
        qi.runAsync(self.say_result, val, result)

    def say_result(self, player_choice, result):
        result_string = self.translator.get_string("say_result").format(
            self.translator.get_string(player_choice), self.translator.get_string(self.current_choice))
        self.translator.straight_say(result_string)
        result_string = self.translator.get_string(
            GameController.decision_translations[GameController.game_states_to_translation[result]])
        self.translator.straight_say(result_string)
        qi.runAsync(self.ask_to_play_again, delay=1300000)

    def ask_to_play_again(self):
        self.translator.translated_say("play_again")
        self._currently_playing = False

    def play_round(self):
        self.robot_controller.clearEyes()
        self._currently_playing = True
        self.current_choice = random.choice(self.choices)
        behavior_name = ""
        if self.current_choice == self.choices[0]:
            behavior_name = "rps_rock"
        elif self.current_choice == self.choices[1]:
            behavior_name = "rps_paper"
        elif self.current_choice == self.choices[2]:
            behavior_name = "rps_scissors"

        final_behavior = "no_nr_rps/" + behavior_name
        self.logger.info("Running {}".format(final_behavior))
        qi.runAsync(self.s.ALBehaviorManager.runBehavior, final_behavior)
        qi.runAsync(self.robot_controller.blink, delay=5200000)
        qi.runAsync(self.take_picture, delay=5200000)
        
