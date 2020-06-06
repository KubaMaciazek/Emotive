from emoji.dictionary import emoji_dict


class Parser:
    def __init__(self):
        return

    def get_emoji_from_photo(self, photo):
        return '\U0001f600'

    def get_emoji_png(self, emoji_code):
        return emoji_dict[emoji_code]
