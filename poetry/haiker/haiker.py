# -*- coding: utf-8 -*-

from logging import getLogger
from logging import StreamHandler
from logging import DEBUG
import random

from poetry.data_constructor.words_data import WordsData
from poetry.rhymer.rhymer import Rhymer

logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)


class Haiker:

    FIVE = 5
    SEVEN = 7
    TWELVE = 12
    VOWEL = "vowel"
    WORD = "word"
    words = None

    def compose(self):
        """
        俳句を詠む．
        """
        rhyming_num = random.choice([1, 2, 3])
        logger.debug('韻: {}'.format(rhyming_num))

        # get 5
        first_sentence = self._get_n_char_sentence(5)
        first_words = WordsData.get_words(first_sentence)
        print("5: ", first_words)
        # get 7
        second_sentence = self._get_n_char_sentence(7)
        second_words = WordsData.get_words(second_sentence)
        second_last_vowel = WordsData.get_n_char_vowel(second_sentence, rhyming_num)
        print("7: ", second_words)
        print(second_last_vowel)
        # get 5 and rhyming
        first_loop_limit = 500
        first_current_loop = 0
        while True:
            first_current_loop += 1
            if first_current_loop == first_loop_limit:
                return "***** だめでした *****"

            try:
                third_sentence = self._get_n_char_sentence(5)
            except IndexError:
                logger.info('*** pop from empty list ***')
                break
            third_last_vowel = WordsData.get_n_char_vowel(third_sentence, rhyming_num)
            if Rhymer.is_rhymed(second_last_vowel, third_last_vowel):
                third_words = WordsData.get_words(third_sentence)
                print("5*: ", third_words)
                print(third_last_vowel)
                print(first_words, second_words, third_words)
                break

    def _get_n_char_sentence(self, n):
        """
        n 文字の文章を取得
        """
        if n == 5:
            random.shuffle(WordsData.words_five_list)
            try:
                return WordsData.words_five_list.pop()
            except IndexError:
                raise
        elif n == 7:
            random.shuffle(WordsData.words_seven_list)
            try:
                return WordsData.words_seven_list.pop()
            except IndexError:
                raise
        else:
            logger.info('*** Invalid number: {} ***'.format(n))
            raise ValueError
