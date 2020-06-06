import cv2
import glob

faceDet = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
faceDet_two = cv2.CascadeClassifier("haarcascade_frontalface_alt2.xml")
faceDet_three = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")
faceDet_four = cv2.CascadeClassifier("haarcascade_frontalface_alt_tree.xml")
# emotions = ["anger", "contempt", "disgust", "fear", "happy",
#             "sadness", "surprise"]  # Define emotions
emotions = ["contempt"]


def detect_faces(emotion):
    files = glob.glob(
        "sorted_set\\%s\\*" % emotion)  # Get list of all images with emotion
    file_number = 0
    for f in files:
        frame = cv2.imread(f)  # Open image
        gray = cv2.cvtColor(frame,
                            cv2.COLOR_BGR2GRAY)  # Convert image to grayscale
        # Detect face using 4 different classifiers
        face = faceDet.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=10,
                                        minSize=(5, 5),
                                        flags=cv2.CASCADE_SCALE_IMAGE)
        face_two = faceDet_two.detectMultiScale(gray, scaleFactor=1.1,
                                                minNeighbors=10,
                                                minSize=(5, 5),
                                                flags=cv2.CASCADE_SCALE_IMAGE)
        face_three = faceDet_three.detectMultiScale(gray, scaleFactor=1.1,
                                                    minNeighbors=10,
                                                    minSize=(5, 5),
                                                    flags=cv2.CASCADE_SCALE_IMAGE)
        face_four = faceDet_four.detectMultiScale(gray, scaleFactor=1.1,
                                                  minNeighbors=10,
                                                  minSize=(5, 5),
                                                  flags=cv2.CASCADE_SCALE_IMAGE)
        # Go over detected faces, stop at first detected face, return empty if no face.
        if len(face) == 1:
            face_features = face
        elif len(face_two) == 1:
            face_features = face_two
        elif len(face_three) == 1:
            face_features = face_three
        elif len(face_four) == 1:
            face_features = face_four
        else:
            face_features = ""
        # Cut and save face
        for (x, y, w,
             h) in face_features:  # get coordinates and size of rectangle
            # containing face
            print("face found in file: %s" % f)
            gray = gray[y:y + h, x:x + w]  # Cut the frame to size
            try:
                out = cv2.resize(gray, (
                    48, 48))  # Resize face so all images have same size
                print("wriring file to dataset\\%s\\%s.jpg" % (emotion, file_number))
                cv2.imwrite("./dataset/%s/%s.jpg" % (emotion, file_number),
                            out)  # Write image
            except:
                pass  # If error, pass file
        file_number += 1  # Increment image number


for em in emotions:
    detect_faces(em)  # Call function
