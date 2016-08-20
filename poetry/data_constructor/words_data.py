# -*- coding: utf-8 -*-

from logging import getLogger
from logging import StreamHandler
from logging import DEBUG

logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)


class WordsData(list):

    """
    単語の情報を網羅したデータクラス．
    WordsData のリスト．
    """

    words_list = list()
