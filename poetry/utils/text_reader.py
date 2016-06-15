# -*- coding: utf-8 -*-

import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())


class TextReader:

    def __init__(self):
        self.read_data = ""

    def read_text(self):
        """
        学習用データ読み込み
        """
        with open("/Users/pokesu/Downloads/corpus/test.txt") as f:
            self.read_data = f.read()
