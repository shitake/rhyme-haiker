# -*- coding: utf-8 -*-

import logging
import MeCab

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())


class MCMC:

    def __init__(self, read_data):
        self.read_data = read_data  # TODO: TextReader からデータを取得するように変更

    def create_chains_list(self):
        """
        入力: 分かち書き後のリスト
        """
        # 先頭の2つの単語からなるリストを
        # construct_chain() へわたす
        chain = self._construct_chain()
        self._insert_chained_words(chain)

        return {
            "word": csv_data[self.WORD],
            "part": csv_data[self.PART],
            "vowel": self.vowel_pronounciation,
            "length": len(self.vowel_pronounciation)
        }

    def _construct_chain_dict(self):
        """
        単語の前後関係を持つ dict を作成．
        """
        text = []
        for line in self._wakatu():  # TODO: 再考
            for word in line:
                text.append(word)
        text_set = list(set(text))

        # 句読点を key としないようにする
        # TODO: 他の記号とかも考慮すべき
        excluded_words = '、。，．'

        chain = {}
        for i in range(len(text_set)):
            candidates = []
            current_key = text_set[i]
            for j in range(len(text) - 1):
                if current_key == text[j] and text[j][-1] not in excluded_words:
                    candidates.append(str(text[j + 1]))
            chain[current_key] = candidates

        return chain

    def _wakatu(self):
        """
        分かち書き後のリストを作成．
        """
        # TODO: ジェネレータ化
        m = MeCab.Tagger('-Owakati')
        return m.parse(self.read_data).split("\n")

    def insert_chained_words(self, word_dict):
        """
        2つの単語からなる dict を
        DB へ登録する．
        """
