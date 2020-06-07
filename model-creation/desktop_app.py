from collections import Counter
from processor import prepare_photo
import cv2


def get_history(cap, model):
    quantity = 10
    history = []
    while len(history) < quantity:
        _, frame = cap.read()
        gray = prepare_photo(frame)
        try:
            new_pred, _ = model.predict(gray)
            history.append(new_pred)
        except:
            continue
    return history


def main():
    emotions = ["anger", "disgust", "fear", "happy",
                "neutral", "sadness", "surprise"]
    model = cv2.face.FisherFaceRecognizer_create()
    model.read("..\\model-30.xml")

    cap = cv2.VideoCapture(0)
    pred = 0
    history = get_history(cap, model)

    while True:
        # Update history - remove oldest, add new
        # _, frame = cap.read()
        # gray = prepare_photo(frame)
        # try:
        #     new_pred, _ = model.predict(gray)
        #     history.pop(0)
        #     history.append(new_pred)
        #     occ = Counter(history)
        #     pred = occ.most_common(1)[0][0]
        # except:
        #     continue

        # Renew history - replace last group with new one
        _, frame = cap.read()
        gray = prepare_photo(frame)
        try:
            new_pred, _ = model.predict(gray)
        except:
            continue
        if len(history) == 10:
            occ = Counter(history)
            pred = occ.most_common(1)[0][0]
            history = []
        else:
            history.append(new_pred)

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
