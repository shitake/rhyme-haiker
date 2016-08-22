# -*- coding: utf-8 -*-

from logging import getLogger
from logging import StreamHandler
from logging import DEBUG

logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)


class Phrase(object):

    """
    text_list: これまでに生成した句のリスト
    last_words: 最後の3単語
    last_vowel: 最後の読み
    """

    text_list = list()
    last_words = tuple()
    last_vowel = list()

    def __init__(self):
        self.text_list = list()
        self.last_words = tuple()
        self.last_vowel = list()

    @property
    def last_vowel(self):
        return self._last_vowel

    @last_vowel.setter
    def last_vowel(self, vowel):
        """
        韻の踏み具合を文字数で評価．
        """
        self._last_vowel = vowel[-2:]
