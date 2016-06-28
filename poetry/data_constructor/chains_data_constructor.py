# -*- coding: utf-8 -*-

import logging
import MeCab

from poetry.data_constructor.data_constructor import DataConstructor

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())


class ChainsDataConstructor(DataConstructor):

    def _extract_data(self, csv_data_list):
        """
        親クラスのメソッドをオーバーライド．
        文章から単語の前後関係を抽出する．
        """
        text_list = self._wakatu(csv_data_list)
        return self._construct_chains_dict(text_list)

    def _wakatu(self, csv_data_list):
        """
        分かち書き後のリストを作成．
        """
        # TODO: ジェネレータ化
        m = MeCab.Tagger('-Owakati')
        return m.parse(csv_data_list).split()

    def _construct_chains_dict(self, text_list):
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
