import pickle
import os
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.cluster import KMeans
from sklearn import metrics
from sklearn.decomposition import PCA
from matplotlib import pyplot as plt


def openPickle():
    ball_x = []
    ball_y = []
    ball_speed_x = []
    ball_speed_y = []
    direction = []
    platform = []
    my_command = []
    for i in range(48):
        file_path = "../log/"+str(i)+".pickle"
        with open(file_path, 'rb') as f:
            data = pickle.load(f)
        # print(str(data['ml']['scene_info'][0])+"\n")
        scene_info = data['ml']['scene_info']
        command = data['ml']['command']

        slope =
        filteData(s['ball'][0], s['ball'][1])
        for i, s in enumerate(scene_info[1:]):
            # if command[i] == "NONE":
            #     continue
            # else:
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
            # if(ball_speed_y[i] > 0 and ball_y[i] > 150):
            #     slope = ball_speed_y[i]/ball_speed_x[i]
            #     cmd = rePredictCommand(
            #         slope, s['ball'][0], s['ball'][1], s['platform'][0])
            #     my_command.append(cmd)
            # else:
            if command[i] == "MOVE_LEFT":
                my_command.append(1)
            elif command[i] == "MOVE_RIGHT":
                my_command.append(2)
            elif command[i] == "NONE":
                my_command.append(0)
            else:
                continue

    numpy_data = np.array(
        [ball_x, ball_y, ball_speed_x, ball_speed_y, direction, platform])

    trainData(np.transpose(numpy_data), my_command)
    # KMeanTrain(np.transpose(numpy_data), my_command)


def KMeanTrain(data, command):
    kmeans = KMeans(n_clusters=3)
    kmeans.fit(data)
    print(command, "\n")
    print(kmeans.labels_)
    pca = PCA(n_components=2).fit(data)
    pca_2d = pca.transform(data)
    # Plot based on Class
    for i in range(0, pca_2d.shape[0]):
        if kmeans.labels_[i] == 0:
            c1 = plt.scatter(pca_2d[i, 0], pca_2d[i, 1], c='r', marker='+')
        elif kmeans.labels_[i] == 1:
            c2 = plt.scatter(pca_2d[i, 0], pca_2d[i, 1], c='g', marker='o')
        elif kmeans.labels_[i] == 2:
            c3 = plt.scatter(pca_2d[i, 0], pca_2d[i, 1], c='b', marker='*')

    plt.legend([c1, c2, c3], ['Cluster 1', 'Cluster 2', 'Cluster 3'])
    plt.show()

    with open("my_model.pickle", 'wb') as f:
        pickle.dump(kmeans, f)


def filteData(x, y, slope, now_cmd):
    while True:
        if(slope > 0):
            dx = 200-x
            dy = abs(dx*slope)
        else:
            dx = x
            dy = abs(dx*slope)
        if(y+dy >= 400):
            break
        else:
            # rebound
            y += dy
            if (slope > 0):
                x = 200
            else:
                x = 0
            slope = -slope
    predict_x = (400-y)/slope+x
    print(predict_x)


def trainData(data, command):
    # split the train and test data
    data_train, data_test, cmd_train, cmd_test = train_test_split(
        data, command, test_size=0.2, random_state=9)
    model = KNeighborsClassifier(n_neighbors=3)
    model.fit(data_train, cmd_train)
    #predict_y = model.predict(data_test)
    # print(model.score(data_test, cmd_test))
    # pca = PCA(n_components=2).fit(data_test)
    # pca_2d = pca.transform(data_test)
    # print(pca_2d.shape[0])
    # for i in range(0, pca_2d.shape[0]):
    #     if predict_y[i] == 0:
    #         c1 = plt.scatter(pca_2d[i, 0], pca_2d[i, 1], c='r', marker='+')
    #     elif predict_y[i] == 1:
    #         c2 = plt.scatter(pca_2d[i, 0], pca_2d[i, 1], c='g', marker='o')
    #     elif predict_y[i] == 2:
    #         c3 = plt.scatter(pca_2d[i, 0], pca_2d[i, 1], c='b', marker='*')

    # plt.legend([c1, c2, c3], ['Cluster 1', 'Cluster 2', 'Cluster 3'])
    # plt.show()
    with open("my_model.pickle", 'wb') as f:
        pickle.dump(model, f)


if __name__ == "__main__":
    openPickle()
