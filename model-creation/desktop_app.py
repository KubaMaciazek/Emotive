from collections import Counter

import cv2
# import glob
#
# faceDet = cv2.CascadeClassifier(
#     "photo-processing/haarcascade_frontalface_default.xml")
# faceDet_two = cv2.CascadeClassifier(
#     "photo-processing/haarcascade_frontalface_alt2.xml")
# faceDet_three = cv2.CascadeClassifier(
#     "photo-processing/haarcascade_frontalface_alt.xml")
# faceDet_four = cv2.CascadeClassifier(
#     "photo-processing/haarcascade_frontalface_alt_tree.xml")
# face_detectors = [faceDet, faceDet_two, faceDet_three, faceDet_four]
#
#
# def find_face(grayscale_photo):
#     for detector in face_detectors:
#         face = detector.detectMultiScale(grayscale_photo,
#                                          scaleFactor=1.1,
#                                          minNeighbors=10,
#                                          minSize=(5, 5),
#                                          flags=cv2.CASCADE_SCALE_IMAGE)
#         if len(face) == 1:
#             return face
#
#
# def prepare_photo(photo):
#     grayscale_photo = cv2.cvtColor(photo,
#                                    cv2.COLOR_BGR2GRAY)
#     face = find_face(grayscale_photo)
#     if face is None:
#         print('Face not found')
#     else:
#         for (x, y, width,
#              height) in face:  # get coordinates and size of rectangle
#             cropped_photo = grayscale_photo[y:y + height,
#                             x:x + width]  # Cut the frame to size
#             resized_photo = cv2.resize(cropped_photo, (
#                 48, 48))  # Resize face so all images have same size
#             return resized_photo  # Write image
#
#
# def detect_faces(emotion):
#     files = glob.glob(
#         "sorted_set/%s//*" % emotion)  # Get list of all images with emotion
#     count = 0
#     for f in files:
#         photo = cv2.imread(f)  # Open image
#         processed_photo = prepare_photo(photo)
#         if processed_photo is None:
#             pass
#         else:
#             print("writing to dataset/%s/%s.jpg" % (emotion, count))
#             cv2.imwrite("dataset/%s/%s.jpg" % (emotion, count),
#                         processed_photo)  # Write image
#             count += 1  # Increment image number
#
#
# def prepare_dataset():
#     emotions = ["anger", "contempt", "disgust", "fear", "happy",
#                 "sadness", "surprise"]
#     for em in emotions:
#         detect_faces(em)


def main():
    emotions = ["anger", "disgust", "fear", "happy",
                "neutral", "sadness", "surprise"]
    model = cv2.face.FisherFaceRecognizer_create()
    model.read("..\\model-30.xml")

    cap = cv2.VideoCapture(0)
    pred = 0
    counter = 0
    preds = []
    while True:
        _, frame = cap.read()
        gray = prepare_photo(frame)
        try:
            new_pred, _ = model.predict(gray)
        except:
            continue

        if len(preds) == 10:
            occ = Counter(preds)
            pred = occ.most_common(1)[0][0]
            x = []
            preds = []
        else:
            preds.append(new_pred)

        font = cv2.FONT_HERSHEY_SCRIPT_COMPLEX
        cv2.putText(frame, emotions[pred], (10, 450), font, 3, (0, 255, 0),
                    2, cv2.LINE_AA)
        cv2.imshow("Emotive", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
