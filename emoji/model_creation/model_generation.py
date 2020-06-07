import glob
import random
import cv2
import numpy as np
from photo_processing.processor import prepare_dataset


def process_images(emotions):
    prepare_dataset(emotions)


def get_training_prediction_set(category):
    print("Listing files for: " + category)
    files = glob.glob("images\\processed_images\\%s\\*" % category)
    random.shuffle(files)
    training = files[:int(len(files) * 0.8)]
    prediction = files[-int(len(files) * 0.2):]
    return training, prediction


def prepare_data(categorises):
    print("Preparing data...")
    training_data = []
    training_labels = []
    prediction_data = []
    prediction_labels = []
    for category in categorises:
        print("Category: " + category)
        training, prediciton = get_training_prediction_set(category)
        print("Training set...")
        for item in training:
            image = cv2.imread(item)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            training_data.append(image)
            training_labels.append(categorises.index(category))
        print("Predictions set...")
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
    print("Training model...")
    fishface.train(training_data, np.asarray(training_labels))

    print("Assessing model...")
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
    print("Correctness: {}".format((100 * correct) / (correct + incorrect)))
    return fishface


def main():
    emotions = ["anger", "disgust", "fear", "happy",
                "neutral", "sadness", "surprise"]
    process_images(emotions)
    model = get_model(emotions)
    model.write("..\\model.xml")


if __name__ == "__main__":
    main()
