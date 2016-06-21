# -*- coding: utf-8 -*-

import copy
from logging import getLogger
from logging import StreamHandler
from logging import DEBUG
import random

logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)


class Haiker:

    def __init__(self, words, chains):
        self.words = words
        self.chains = chains

        self.word = ""
        self.word_list = []
        self.text = ""
        self.text_list = []
        self.nodes = {}
        self.current_depth = 0

    def construct_first_five(self):
        """
        最初の5字を作成する．
        """
        # first_five_list = []
        # key_list = list((self.data).keys())

        # 5字作成ループ
        # for word in random.choice(key_list):
        #     first_five_list.append(word)

        #     first_five = ''.join(first_five_list)
        #     if self._is_five_char(first_five):
        #         return first_five_list

        #     # key に続く val を取得

        # return None

        # 単語リスト取得
        self.word_list = self._get_word_list()
        # これまでの単語リスト
        self.nodes[self.current_depth] = copy.copy(self.word_list)

        while True:
            if self._is_empty_first_node():
                return None  # TODO: 作成失敗時にエラーを返すようにする

            logger.debug("-----------start: " + self.text)
            logger.debug("----- outer_word_list: " + repr(self.word_list))

            while True:
                # 単語1つ取得
                self._get_word()
                logger.debug("----- inner_word_list: " + repr(self.word_list))

                if not self.word:
                    self.word_list = self._back_prev_word_list()
                    logger.debug("======================== back: " + repr(self.word_list))
                elif self._is_five_char(self.text + self.word):
                    return self._return_completed_text()
                elif len(self.text + self.word) < 5:
                    # 5文字未満なら次の単語を取得する
                    self.text = self.text + self.word
                    self.text_list.append(self.word)
                    break
                else:
                    # 5文字より長くなったら別の単語を取得しなおす
                    logger.debug(
                        "----- else" +
                        self.text +
                        self.word +
                        repr(self.word_list) +
                        self.current_depth +
                        repr(self.nodes)
                    )
                    pass

            # 単語をkeyに単語リスト取得
            self._get_next_word_list()
            self.word_list = self.nodes[self.current_depth]

    def _get_word_list(self):
        """単語リストの取得"""
        return list((self.chains).keys())

    def _get_word(self):
        """単語をランダムに1つ取得"""
        if not self.word_list:
            self.word = ""
        else:
            random.shuffle(self.word_list)
            self.word = self.word_list.pop()  # , self.word_list

    def _back_prev_word_list(self):
        """単語リストが空になったら，前の単語リストに戻る"""
        self.current_depth -= 1
        return self.nodes[self.current_depth]

    def _return_completed_text(self):
        """完成形の文章を返す"""
        logger.debug("[Completed]: " + self.text + self.word)
        return self.text + self.word

    def _is_n_char(self, n, pronunciation):
        """
        与えられた文章の発音が n 文字であれば真．

        Args:
          n: 文字数．int．
          pronunciation: 発音．
        """
        if len(pronunciation) == n:
            return True
        else:
            return False

    def _is_five_char(self, word):
        """文字数チェック"""
        if len(word) == 5:
            return True
        else:
            return False

    def _get_next_word_list(self):
        """単語を key に単語リストを取得"""
        self.current_depth += 1
        keys = (self.chains).keys()
        # data に key が存在しない場合，
        # ランダムに取得する
        if self.word not in keys:
            logger.debug("-----: " + self.word + "not in")
            self.word = random.choice(list(keys))
            logger.debug("----- new word:" + self.word)
        self.nodes[self.current_depth] = self.chains[self.word]

    def _is_empty_first_node(self):
        """最初のノードが空の場合真"""
        if self.nodes[0] == []:
            return True
        else:
            return False

    def construct_seven(self, last_word):
        """
        真ん中の7字を作成する．

        Args:
          last_word: 最初の5字における最後の単語
        """
        # return seven_list

    def construct_last_five(self, last_word):
        """
        最後の5字を作成する．
        """
        # return last_five_list
