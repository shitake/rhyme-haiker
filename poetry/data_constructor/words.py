# -*- coding: utf-8 -*-

from logging import getLogger
from logging import StreamHandler
from logging import DEBUG

logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)


class Words(object):

    WORD = 'word'
    VOWEL = 'vowel'
    LENGTH = 'length'
    PART = 'part'
    words = None

    def __init__(self, word_dict):
        self.word = word_dict[self.WORD]
        self.vowel = word_dict[self.VOWEL]
        self.length = word_dict[self.LENGTH]
        self.part = word_dict[self.PART]
