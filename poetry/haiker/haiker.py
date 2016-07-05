# -*- coding: utf-8 -*-

import copy
import json
from logging import getLogger
from logging import StreamHandler
from logging import DEBUG
import random

from poetry.rhymer.rhymer import Rhymer

logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)


class Haiker:

    FIVE = 5
    SEVEN = 7
    VOWEL = "vowel"
    WORD = "word"

    def __init__(self, words, chains):
        self.words = json.loads(json.dumps(words))
        self.chains = json.loads(json.dumps(chains))

        self.word_list = []

        self.word = ""
        self.vowel = ""
        self.text = ""
        self.text_vowel = ""
        self.text_list = []
        self.vowel_list = []
        self.nodes = {}
        self.current_depth = 0

        self.last_word_of_first_five = ""
        self.last_word_of_seven = ""

        self.first_five = ""
        self.seven = ""
        self.last_five = ""
        self.haiku = ""

        self.first_five_list = []
        self.seven_list = []
        self.last_five_list = []

        self.first_five_vowel = ""
        self.seven_vowel = ""
        self.last_five_vowel = ""

    def compose(self):
        """
        俳句を詠む．
        """
        self.construct_first_five()
        self.construct_seven()

        # TODO: ここで押韻チェックしてだめなら再処理
        loop_limit = 200
        current_loop = 1
        rhymer = Rhymer()
        while True:
            print(current_loop)
            self.construct_last_five()
            if rhymer.is_rhymed(self.seven_vowel, self.last_five_vowel) or \
                    rhymer.is_rhymed(self.first_five_vowel, self.last_five_vowel):
                break
            current_loop += 1
            if current_loop == loop_limit:
                self.haiku = "***** だめでした *****"
                break

        logger.debug("[Haiku] >>> " + self.haiku)

        return self.haiku

    def property_initializer(func):
        """
        5, 7, 5 の各句を詠む前の初期化処理を行うためのデコレータ．
        """

        def wrapper(self):
            self.word = ""
            self.vowel = ""
            self.text = ""
            self.text_vowel = ""
            self.text_list = []
            self.vowel_list = []
            self.nodes = {}
            self.current_depth = 0
            logger.debug("[Initialized]")

            ret = func(self)

            self.haiku = self.first_five + self.seven + self.last_five

            return ret

        return wrapper

    @property_initializer
    def construct_first_five(self):
        """
        最初の5字を作成する．
        """
        self._get_word_list()
        # これまでの単語リスト
        self.nodes[self.current_depth] = copy.copy(self.word_list)

        while True:
            if self._is_empty_first_node():
                return None  # TODO: 作成失敗時にエラーを返すようにする

            logger.debug("-----------start 5: " + self.text)
            logger.debug("----- outer_word_list: " + repr(self.word_list))

            while True:
                # 単語1つ取得
                self._get_word()
                logger.debug("----- inner_word_list: " + repr(self.word_list))

                if not self.word:
                    self._back_prev_word_list()
                    logger.debug(
                        "======================== back: " +
                        repr(self.word_list)
                    )
                elif self._is_n_char(
                    Haiker.FIVE,
                    self.text_vowel + self.vowel
                ):
                    self.last_word_of_first_five = self.word
                    self.first_five, self.first_five_vowel = self._create_completed_text()
                    self.first_five_list = self.text_list
                    return self.first_five
                elif self._is_less_than_n_char(
                    Haiker.FIVE,
                    self.text_vowel + self.vowel
                ):
                    self._preproc_getting_next_word()
                    break
                else:
                    # 5文字より長くなったら別の単語を取得しなおす
                    logger.debug(
                        "----- else" +
                        repr(self.text) +
                        repr(self.word) +
                        repr(self.word_list) +
                        repr(self.current_depth) +
                        repr(self.nodes)
                    )
                    pass

            # 単語をkeyに単語リスト取得
            self._preproc_getting_next_word_list()

    def _get_word_list(self):
        """単語リストの取得"""
        self.word_list = list((self.chains).keys())

    def _is_empty_first_node(self):
        """最初のノードが空の場合真"""
        if self.nodes[0] == []:
            return True
        else:
            return False

    def _get_word(self):
        """単語をランダムに1つ取得"""
        if not self.word_list:
            self.word = ""
        else:
            random.shuffle(self.word_list)
            self.word = self.word_list.pop()

            # self.vowel = self.words[self.word][Haiker.VOWEL]
            for d in self.words:
                if d[Haiker.WORD] == self.word:
                    self.vowel = d[Haiker.VOWEL]

    def _back_prev_word_list(self):
        """単語リストが空になったら，前の単語リストに戻る"""
        if self.current_depth == 0:
            return None  # TODO: 例外をなげる
        self.current_depth -= 1
        self.word_list = self.nodes[self.current_depth]

    def _create_completed_text(self):
        """完成形の文章を返す"""
        logger.debug("[Completed]: " + self.text + self.word)
        return self.text + self.word, self.text_vowel + self.vowel

    def _is_n_char(self, n, text):
        """
        与えられた文章(発音)が n 文字であれば真．

        Args:
          n: 文字数．int．
          text: 文章(発音)．
        """
        if len(text) == n:
            return True
        else:
            return False

    def _is_less_than_n_char(self, n, text):
        """
        与えられた文章が，n文字未満であれば真
        """
        if len(text) < n:
            return True
        else:
            return False

    def _preproc_getting_next_word(self):
        """
        次の単語を取得するための前処理．
        """
        self.text += self.word
        self.text_list.append(self.word)
        self.text_vowel += self.vowel
        self.vowel_list.append(self.vowel)

    def _preproc_getting_next_word_list(self):
        """単語を key に単語リストを取得"""
        keys = self.nodes[0]
        # data に key が存在しない場合，
        # ランダムに取得する
        if self.word not in keys:
            if not self.word:
                self.word = "[Empty]"
            logger.debug("-----: " + self.word + " not in")
            if not keys:
                return None  # TODO: 例外を返すようにする
            # ランダム取得されたキーも初期キーから削除する
            self.word = random.choice(keys)
            keys.remove(self.word)
            logger.debug("----- new word: " + self.word)
        else:
            self.current_depth += 1
        self.nodes[self.current_depth] = copy.copy(self.chains[self.word])
        self.word_list = self.nodes[self.current_depth]

    @property_initializer
    def construct_seven(self):
        """
        真ん中の7字を作成する．
        """
        if not self.last_word_of_first_five:
            raise ConstructionError(
                self.last_word_of_first_five,
                self.last_word_of_seven
            )
        logger.debug(
            "----- last_word_of_first_five: " + self.last_word_of_first_five
        )

        self.word = self.last_word_of_first_five
        self._get_word_list()
        # これまでの単語リスト初期化
        self.nodes[self.current_depth] = copy.copy(self.word_list)

        while True:
            if self._is_empty_first_node():
                return None  # TODO: 作成失敗時にエラーを返すようにする

            # 単語をkeyに単語リスト取得
            self._preproc_getting_next_word_list()

            logger.debug("-----------start 7: " + self.text)
            logger.debug("----- outer_word_list: " + repr(self.word_list))

            while True:
                # 単語1つ取得
                self._get_word()
                logger.debug("----- inner_word_list: " + repr(self.word_list))

                if not self.word:
                    self._back_prev_word_list()
                    logger.debug(
                        "======================== back: " +
                        repr(self.word_list)
                    )
                elif self._is_n_char(
                    Haiker.SEVEN,
                    self.text_vowel + self.vowel
                ):
                    self.last_word_of_seven = self.word
                    self.seven, self.seven_vowel = self._create_completed_text()
                    self.seven_list = self.text_list
                    return self.seven
                elif self._is_less_than_n_char(
                    Haiker.SEVEN,
                    self.text_vowel + self.vowel
                ):
                    self._preproc_getting_next_word()
                    break
                else:
                    # 5文字より長くなったら別の単語を取得しなおす
                    logger.debug(
                        "----- else: " +
                        repr(self.text) +
                        repr(self.word) +
                        repr(self.word_list) +
                        repr(self.current_depth) +
                        repr(self.nodes)
                    )
                    pass

    @property_initializer
    def construct_last_five(self):
        """
        最後の5字を作成する．
        """
        if not self.last_word_of_seven:
            raise ConstructionError(
                self.last_word_of_first_five,
                self.last_word_of_seven
            )
        logger.debug(
            "----- last_word_of_seven: " + self.last_word_of_seven
        )

        self.word = self.last_word_of_seven
        self._get_word_list()
        # これまでの単語リスト初期化
        self.nodes[self.current_depth] = copy.copy(self.word_list)

        while True:
            if self._is_empty_first_node():
                return None  # TODO: 作成失敗時にエラーを返すようにする

            # 単語をkeyに単語リスト取得
            self._preproc_getting_next_word_list()

            logger.debug("-----------start 5: " + self.text)
            logger.debug("----- outer_word_list: " + repr(self.word_list))

            while True:
                # 単語1つ取得
                self._get_word()
                logger.debug("----- inner_word_list: " + repr(self.word_list))

                if not self.word:
                    self._back_prev_word_list()
                    logger.debug(
                        "<<<<<<<<<<<<<<<<<<<<<<<< back: " +
                        repr(self.word_list)
                    )
                elif self._is_n_char(
                    Haiker.FIVE,
                    self.text_vowel + self.vowel
                ):
                    self.last_word_of_last_five = self.word
                    self.last_five, self.last_five_vowel = self._create_completed_text()
                    self.last_five_list = self.text_list
                    return self.last_five
                elif self._is_less_than_n_char(
                    Haiker.FIVE,
                    self.text_vowel + self.vowel
                ):
                    self._preproc_getting_next_word()
                    break
                else:
                    # 5文字より長くなったら別の単語を取得しなおす
                    logger.debug(
                        "----- else: " +
                        repr(self.text) +
                        repr(self.word) +
                        repr(self.word_list) +
                        repr(self.current_depth) +
                        repr(self.nodes)
                    )
                    pass


class ConstructionError(Exception):

    def __init__(self, last_five, last_seven):
        self.last_five = last_five
        self.last_seven = last_seven

    def __str__(self):
        return repr(self.last_five, self.last_seven)
