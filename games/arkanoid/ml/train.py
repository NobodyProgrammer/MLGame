import pickle
import os
import numpy as np
from sklearn.neighbors import KNeighborsClassifier


def openPickle():
    ball_x = []
    ball_y = []
    ball_speed_x = []
    ball_speed_y = []
    direction = []
    platform = []
    my_command = []
    for i in range(6):
        file_path = "../log/"+str(i)+".pickle"
        with open(file_path, 'rb') as f:
            data = pickle.load(f)
        # print(str(data['ml']['scene_info'][0])+"\n")
        scene_info = data['ml']['scene_info']
        command = data['ml']['command']
        ball_x.append(scene_info[0]['ball'][0])
        ball_y.append(scene_info[0]['ball'][1])
        ball_speed_x.append(0)
        ball_speed_y.append(0)
        direction.append(0)
        platform.append(scene_info[0]['platform'][0])
        my_command.append(0)
        for i, s in enumerate(scene_info[1:]):
            ball_x.append(s['ball'][0])
            ball_y.append(s['ball'][1])
            platform.append(s['platform'][0])
            ball_speed_x.append(
                scene_info[i]['ball'][0]-scene_info[i-1]['ball'][0])
            ball_speed_y.append(
                scene_info[i]['ball'][1]-scene_info[i-1]['ball'][1])
            if(ball_speed_x[-1] > 0):
                if(ball_speed_y[-1] > 0):
                    # right down
                    direction.append(0)
                else:
                    # right up
                    direction.append(1)
            else:
                if (ball_speed_y[-1] > 0):
                    # left down
                    direction.append(2)
                else:
                    # left up
                    direction.append(3)

        for c in command[1:]:
            if c == "NONE":
                my_command.append(0)
            elif c == "MOVE_LEFT":
                my_command.append(1)
            else:
                my_command.append(2)
    numpy_data = np.array(
        [ball_x, ball_speed_y, ball_speed_x, ball_speed_y, direction, platform])
    trainData(np.transpose(numpy_data), my_command)


def rePredictCommand(ball_x, ball_y, platform_x):
    return "None"


def trainData(data, command):
    model = KNeighborsClassifier(n_neighbors=3)
    model.fit(data, command)
    with open("my_model.pickle", 'wb') as f:
        pickle.dump(model, f)


if __name__ == "__main__":
    openPickle()
