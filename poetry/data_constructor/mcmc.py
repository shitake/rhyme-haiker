# -*- coding: utf-8 -*-

import logging
import MeCab

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())


class MCMC:

    def __init__(self):
        # self.read_data = read_data  # TODO: TextReader からデータを取得するように変更
        self.read_data = ""

    def create_chains_list(self, read_data):
        """
        文章から単語の前後関係を抽出する．

        Args:
          read_data: 未加工の文章
        """
        self.read_data = read_data
        text_list = self._wakatu()
        chain = self._create_chain_dict(text_list)
        # self._insert_chained_words(chain)

        return chain  # TODO: words データ作成側と同じような出力型にする

    def _wakatu(self):
        """
        分かち書き後のリストを作成．
        """
        # TODO: ジェネレータ化
        m = MeCab.Tagger('-Owakati')
        return m.parse(self.read_data).split()

    def _create_chain_dict(self, text_list):
        """
        単語の前後関係を持つ dict を作成．

        Args:
          text_list: 分かち書き後のリスト
        """
        unique_text_list = list(set(text_list))

        chain = {}
        for current_key in unique_text_list:
            chain[current_key] = self._create_next_word_list(
                current_key,
                text_list
            )

        return chain

    def _create_next_word_list(self, current_word, text_list):
        """
        指定した単語に続く単語のリストを
        文章中から作成する．

        Args:
          current_word: 指定した単語
          text_list: 文章を分かち書きした後のリスト
        """
        # 句読点を key としないようにする
        # TODO: 他の記号とかも考慮すべき
        # TODO: is で比較すべき？
        excluded_words = '、。，．'

        next_word_list = []

        for i in range(len(text_list) - 1):
            last_char = text_list[i][-1]

            if text_list[i] == current_word and \
                    last_char not in excluded_words:

                next_word = str(text_list[i + 1])
                next_word_list.append(next_word)

        return next_word_list

    # def _create_text_set(self):
    #     """
    #     単語の set を作成
    #     """
    #     text = []
    #     for line in self._wakatu():  # TODO: 再考
    #         for word in line:
    #             text.append(word)
    #     return list(set(text))

    # def insert_chained_words(self, word_dict):
    #     """
    #     2つの単語からなる dict を
    #     DB へ登録する．
    #     """
