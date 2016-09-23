# -*- coding: utf-8 -*-

import logging

from poetry.data_constructor.data_constructor import DataConstructor
from poetry.utils.markov import Markov

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())


class ChainsDataConstructor(DataConstructor):

    N = 3  # N-gram の N
    SENTENCE_LEN_MIN = 3

    def _extract_data(self, csv_data_list):
        """
        親クラスのメソッドをオーバーライド．
        文章から単語の前後関係を抽出する．
        """
        markov = Markov()
        text_list = [data[self.WORD] for data in csv_data_list]
        if len(text_list) < self.SENTENCE_LEN_MIN:
            return dict()
        else:
            return markov.build_model(text_list, self.N)
