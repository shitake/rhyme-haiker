# -*- coding: utf-8 -*-

import json
from logging import getLogger
from logging import StreamHandler
from logging import DEBUG
import pickle

import poetry

logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)


class DataExporter:

    OUTPUT_DIR = poetry.__path__[0] + '/../output/'
    CHAINS_FILE_NAME = "chains.pickle"
    WORDS_FILE_NAME = "words.pickle"

    def __init__(self, chains_data, words_data):
        self.chains_data = chains_data
        self.words_data = words_data

    def export_json(self):
        """
        json に出力．
        """
        self._export(json.dumps(self.chains_data, ensure_ascii=False),
                     json.dumps(self.words_data, ensure_ascii=False))

    def export_pickle(self):
        """
        Pickle で保存．
        """
        self._export(pickle.dumps(self.chains_data),
                     pickle.dumps(self.words_data))

    def _export(self, chains_data, words_data):
        with open(self.OUTPUT_DIR + DataExporter.CHAINS_FILE_NAME,
                  mode='wb'
                  ) as f:
            f.write(chains_data)
        with open(self.OUTPUT_DIR + DataExporter.WORDS_FILE_NAME,
                  mode='wb'
                  ) as f:
            f.write(words_data)
