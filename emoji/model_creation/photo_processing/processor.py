import cv2
import glob

faceDet = cv2.CascadeClassifier(
    "emoji/model_creation/photo_processing/haarcascade_frontalface_default.xml")
faceDet_two = cv2.CascadeClassifier(
    "emoji/model_creation/photo_processing/haarcascade_frontalface_alt2.xml")
faceDet_three = cv2.CascadeClassifier(
    "emoji/model_creation/photo_processing/haarcascade_frontalface_alt.xml")
faceDet_four = cv2.CascadeClassifier(
    "emoji/model_creation/photo_processing/haarcascade_frontalface_alt_tree.xml")
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
    if face is None:
        print('Face not found')
    else:
        for (x, y, width,
             height) in face:  # get coordinates and size of rectangle
            cropped_photo = grayscale_photo[y:y + height,
                            x:x + width]  # Cut the frame to size
            resized_photo = cv2.resize(cropped_photo, (
                48, 48))  # Resize face so all images have same size
            return resized_photo  # Write image


def detect_faces(emotion):
    files = glob.glob(
        "sorted_set/%s//*" % emotion)  # Get list of all images with emotion
    count = 0
    for f in files:
        photo = cv2.imread(f)  # Open image
        processed_photo = prepare_photo(photo)
        if processed_photo is None:
            pass
        else:
            print("writing to dataset/%s/%s.jpg" % (emotion, count))
            cv2.imwrite("dataset/%s/%s.jpg" % (emotion, count),
                        processed_photo)  # Write image
            count += 1  # Increment image number


def prepare_dataset(emotions):
    for em in emotions:
        detect_faces(em)
