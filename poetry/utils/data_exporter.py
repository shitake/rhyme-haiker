# -*- coding: utf-8 -*-

import json
from logging import getLogger
from logging import StreamHandler
from logging import DEBUG

import poetry

logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)


class DataExporter:

    OUTPUT_DIR = poetry.__path__[0] + '/../output/'
    CHAINS_FILE_NAME = "chains.json"
    WORDS_FILE_NAME = "words.json"

    def __init__(self, chains_data, words_data):
        self.chains_data = json.dumps(chains_data, ensure_ascii=False)
        self.words_data = json.dumps(words_data, ensure_ascii=False)

    def export_json(self):
        """
        json に出力．
        """
        with open(
                self.OUTPUT_DIR + DataExporter.CHAINS_FILE_NAME,
                mode='w',
        ) as f:
            f.write(self.chains_data)
        with open(
                self.OUTPUT_DIR + DataExporter.WORDS_FILE_NAME,
                mode='w',
        ) as f:
            f.write(self.words_data)
