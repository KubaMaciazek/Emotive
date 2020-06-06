import glob
import random
import cv2
import numpy as np


def process_images():
    # ToDo: process source images:
    #   find face in each of source pictures,
    #   cut square containing it out,
    #   converte it to grayscale,
    #   resize and save in corresponding emotion
    #   directory in processed_images.
    #   Make sure all images have the same size.
    pass


def get_training_prediction_set(category):
    files = glob.glob("images\\processed_images\\%s\\*" % category)
    random.shuffle(files)
    training = files[:int(len(files) * 0.8)]
    prediction = files[-int(len(files) * 0.2):]
    return training, prediction


def prepare_data(categorises):
    training_data = []
    training_labels = []
    prediction_data = []
    prediction_labels = []
    for category in categorises:
        training, prediciton = get_training_prediction_set(category)
        for item in training:
            image = cv2.imread(item)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            training_data.append(image)
            training_labels.append(categorises.index(category))
        for item in prediciton:
            image = cv2.imread(item)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            prediction_data.append(image)
            prediction_labels.append(categorises.index(category))
    return training_data, training_labels, prediction_data, prediction_labels


def get_model(categories):
    training_data, training_labels, prediction_data, \
        prediction_labels = prepare_data(categories)
    fishface = cv2.face.FisherFaceRecognizer_create()
    fishface.train(training_data, np.asarray(training_labels))

    cnt = 0
    correct = 0
    incorrect = 0
    for image in prediction_data:
        pred, _ = fishface.predict(image)
        if pred == prediction_labels[cnt]:
            correct += 1
            cnt += 1
        else:
            incorrect += 1
            cnt += 1
    print("Correctness: {}".format((100*correct)/(correct + incorrect)))
    return fishface


def main():
    directory = "./images"
    emotions = ["anger", "contempt", "disgust", "fear",
                "happy", "sadness", "surprise"]
    reduced = ["anger", "disgust", "happy",
               "surprise"]
    process_images()
    model = get_model(emotions)
    model.save("..\\model.xml")

if __name__ == "__main__":
    main()
