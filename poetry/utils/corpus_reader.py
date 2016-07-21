# -*- coding: utf-8 -*-

import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())


class CorpusReader:

    def read_file(self, addr):
        """
        学習用データ読み込み
        """
        with open(addr) as f:
            return f.read()
