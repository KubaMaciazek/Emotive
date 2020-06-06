import cv2
from time import sleep

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
                                   cv2.COLOR_BGR2GRAY)  # Convert image to grayscale
    # Detect face using 4 different classifiers
    face = find_face(grayscale_photo)
    if face is None:
        # print('Face not found')
        pass
    else:
        # print("Face found")
        for (x, y, width,
             height) in face:  # get coordinates and size of rectangle
            cropped_photo = grayscale_photo[y:y + height,
                            x:x + width]  # Cut the frame to size
            try:
                resized_photo = cv2.resize(cropped_photo, (
                    48, 48))  # Resize face so all images have same size
                return resized_photo # Write image
            except:
                pass  # If error, pass file


def main():
    emotions = ["anger", "contempt", "disgust", "fear",
                "happy", "sadness", "surprise"]
    model = cv2.face.FisherFaceRecognizer_create()
    model.read("..\\model.xml")

    cap = cv2.VideoCapture(0)
    pred = 0
    while True:
        _, frame = cap.read()
        gray = prepare_photo(frame)
        try:
            pred, _ = model.predict(gray)
        except:
            pass

        # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        font = cv2.FONT_HERSHEY_SCRIPT_COMPLEX
        cv2.putText(frame, emotions[pred], (10, 450), font, 3, (0, 255, 0),
                    2, cv2.LINE_AA)
        cv2.imshow("Emotive", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        # sleep(1)
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()