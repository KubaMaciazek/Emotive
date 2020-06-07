import glob
import random
import cv2
import numpy as np

faceDet = cv2.CascadeClassifier(
    "photo-processing/haarcascade_frontalface_default.xml")
faceDet_two = cv2.CascadeClassifier(
    "photo-processing/haarcascade_frontalface_alt2.xml")
faceDet_three = cv2.CascadeClassifier(
    "photo-processing/haarcascade_frontalface_alt.xml")
faceDet_four = cv2.CascadeClassifier(
    "photo-processing/haarcascade_frontalface_alt_tree.xml")
face_detectors = [faceDet, faceDet_two, faceDet_three, faceDet_four]


def find_face(grayscale_photo):
    for detector in face_detectors:
        face = detector.detectMultiScale(grayscale_photo,
                                         scaleFactor=1.1,
                                         minNeighbors=10,
                                         minSize=(5, 5),
                                         flags=cv2.CASCADE_SCALE_IMAGE)
        if len(face) == 1:
            return face


def prepare_photo(photo):
    grayscale_photo = cv2.cvtColor(photo,
                                   cv2.COLOR_BGR2GRAY)
    face = find_face(grayscale_photo)
    if face is not None:
        # print('Face not found')
        # else:
        # print("Face found")
        for (x, y, width,
             height) in face:  # get coordinates and size of rectangle
            cropped_photo = grayscale_photo[y:y + height,
                            x:x + width]  # Cut the frame to size
            resized_photo = cv2.resize(cropped_photo, (
                48, 48))  # Resize face so all images have same size
            return resized_photo  # Write image


def detect_faces(emotion):
    files = glob.glob(
        "images/raw_images/%s/*" % emotion)  # Get list of all images with emotion
    count = 0
    for f in files:
        photo = cv2.imread(f)  # Open image
        # processed_photo = prepare_photo(photo)
        processed_photo = photo
        if processed_photo is None:
            pass
        else:
            # print("writing to images/processed_images/%s/%s.jpg" % (
            # emotion, count))
            cv2.imwrite("images/processed_images/%s/%s.jpg" % (emotion, count),
                        processed_photo)  # Write image
            count += 1  # Increment image number


def prepare_dataset(emotions):
    # emotions = ["anger", "contempt", "disgust", "fear", "happy",
    #             "sadness", "surprise"]
    for em in emotions:
        detect_faces(em)


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
    directory = "./images"
    # emotions = ["anger", "contempt", "disgust", "fear",
    #             "happy", "sadness", "surprise"]
    emotions = ["anger", "disgust", "fear", "happy",
                "neutral", "sadness", "surprise"]
    process_images()
    model = get_model(emotions)
    model.write("..\\model.xml")



if __name__ == "__main__":
    main()
