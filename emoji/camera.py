from kivy.uix.image import Image
from kivy.clock import Clock
import cv2
from collections import Counter
from emoji.model_creation.photo_processing.processor import prepare_photo
from kivy.graphics.texture import Texture
from emoji.dictionary import emotions, emoji_dict


class EmojiRecognitionCamera(Image):
    def __init__(self, capture, fps, emoji_preview, **kwargs):
        super(EmojiRecognitionCamera, self).__init__(**kwargs)
        self.capture = capture
        self.model = cv2.face.FisherFaceRecognizer_create()
        self.model.read("model-30.xml")
        self.pred = 0
        self.history = None
        self.current_emotion = emotions[3]
        self.frame_count = 0
        self.fps = fps
        self.emoji_preview = emoji_preview
        Clock.schedule_interval(self.update, 1.0 / self.fps)

    def update(self, dt):
        self.frame_count = (self.frame_count + 1) % (self.fps / 10)
        ret, frame = self.capture.read()
        if ret:
            # convert it to texture
            buf1 = cv2.flip(frame, 0)
            buf = buf1.tostring()
            image_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            # display image from the texture
            self.texture = image_texture

            if self.frame_count == 0:
                self.recognize_emotion(frame)
                self.update_emoji_preview()

    def get_history(self):
        quantity = 10
        history = []
        while len(history) < quantity:
            _, frame = self.capture.read()
            gray = prepare_photo(frame)
            try:
                new_pred, _ = self.model.predict(gray)
                history.append(new_pred)
            except:
                continue
        return history

    def recognize_emotion(self, frame):
        if self.history is None:
            self.history = self.get_history()
        # get emoji
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
        gray = prepare_photo(frame)
        try:
            new_pred, _ = self.model.predict(gray)
        except:
            return
        if len(self.history) == 10:
            occ = Counter(self.history)
            self.pred = occ.most_common(1)[0][0]
            self.current_emotion = emotions[self.pred]
            self.history = []
        else:
            self.history.append(new_pred)

    def get_current_emoji(self):
        return emoji_dict[self.current_emotion]

    def update_emoji_preview(self):
        _, self.emoji_preview.source = self.get_current_emoji()
        return
