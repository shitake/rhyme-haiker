# -*- coding: utf-8 -*-

import json
from logging import getLogger
from logging import StreamHandler
from logging import DEBUG

from poetry.data_constructor.data_constructor import DataConstructor

logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)


class DataExporter:

    CHAINS_FILE_NAME = "chains.json"
    WORDS_FILE_NAME = "words.json"

    def __init__(self, chains_data, words_data):
        self.chains_data = chains_data
        self.words_data = words_data

    def export_json(self):
        """
        json に出力．
        """
        with open(DataExporter.CHAINS_FILE_NAME) as f:
            json.dump(self.chains_data, f)
        with open(DataExporter.WORDS_FILE_NAME) as f:
            json.dump(self.words_data, f)

if __name__ == '__main__':
    dc = DataConstructor()
    mecabed = dc.construct_data()
    de = DataExporter(
        chains_data=
        words_data=mecabed
    )
    de.export_json()
