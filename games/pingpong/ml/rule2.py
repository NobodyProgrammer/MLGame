"""
The template of the script for the machine learning process in game pingpong
"""

import pickle
import os
import math
import random


class MLPlay:
    def __init__(self, side):
        """
        Constructor

        @param side A string "1P" or "2P" indicates that the `MLPlay` is used by
               which side.
        """
        self.ball_served = False
        self.side = side
        self.ball_last_x = 100
        self.ball_last_y = 420

    def update(self, scene_info):
        """
        Generate the command according to the received scene information
        """
        if scene_info["status"] != "GAME_ALIVE":
            print("ball_x=", scene_info.get("ball")[0])
            # \\return "RESET"

        if not self.ball_served:
            self.ball_served = True
            return "SERVE_TO_LEFT"
        else:
            command = ""
            ball_x = (scene_info.get('ball')[0])
            ball_y = (scene_info.get('ball')[1])
            p2_x = (scene_info.get('platform_2P')[0])
            block_x = 0

            if(ball_y-self.ball_last_y < 0):

                predict_x = self.predict(ball_x, ball_y, block_x)
                if(p2_x > predict_x-random.randint(10, 20)):
                    command = "MOVE_LEFT"
                elif(p2_x < predict_x-random.randint(30, 40)):
                    command = "MOVE_RIGHT"
                else:
                    command = "NONE"

                # print(scene_info.get('ball_speed'))
            else:
                if(p2_x > 100):
                    command = "MOVE_LEFT"
                elif(p2_x < 90):
                    command = "MOVE_RIGHT"
                else:
                    command = "NONE"
            self.ball_last_x = ball_x
            self.ball_last_y = ball_y
            # print(scene_info.get('ball_speed'))
            return command

    def predict(self, x, y, block_x):
        slope = (y-self.ball_last_y)/(x-self.ball_last_x)
        while True:
            if(slope > 0):
                dx = x
                dy = abs(dx*slope)
            else:
                dx = 195-x
                dy = abs(dx*slope)
            if(y-dy <= 80):
                break
            else:
                # rebound here
                y -= dy
                if(slope > 0):
                    x = 0
                else:
                    x = 195
                slope = -slope
        predict_x = (80-y)/slope+x
        # print(predict_x)
        return predict_x

    def reset(self):
        """
        Reset the status
        """
        self.ball_served = False
