# -*- coding: utf-8 -*-

from logging import getLogger
from logging import StreamHandler
from logging import INFO
import MeCab
import re

logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(INFO)
logger.setLevel(INFO)
logger.addHandler(handler)


class DataConstructor:

    WORD = 0
    PART = 1
    PART_SUBTYPE = 2
    PRONOUNCIATION = 9

    DELIMITER = '\n'

    def __init__(self):
        self.yomi = ""
        self.vowel_pronounciation = ""

    def construct_data(self, read_data):
        """
        インターフェイス
        テーブル挿入用データを作成する．
        """
        # TODO: インターフェイス修正
        #       分かち書き後の単語1つを入力データとして受け取る
        #       方がよさそう

        return self._construct_parsed_data(read_data)  # TODO: 修正対象

    def _construct_parsed_data(self, read_data):
        """
        Mecab で解析後のデータを返す
        """
        m = MeCab.Tagger()

        # 1文を改行コードで切る
        parsed_text = m.parse(read_data)
        delimited_list = self._delimit(parsed_text)
        csv_list = [
            self._splited_word_data_to_csv_list(line) for line in delimited_list
        ]
        sanitized_data_list = self._sanitize_data_list(csv_list)
        return self._extract_data(sanitized_data_list)

    def _delimit(self, parsed_text):
        return parsed_text.split(self.DELIMITER)

    def _splited_word_data_to_csv_list(self, splited_word_data):
        """
        分かち書き後のデータリストを csv のリストへ変換．
        """
        # TODO: Utils クラスへ引越
        if not isinstance(splited_word_data, str):
            logger.warning(
                "Input value is not String: %s." % splited_word_data
            )

        csv_text = re.sub('\t', ',', splited_word_data)
        return csv_text.split(',')

    def _sanitize_data_list(self, csv_list):
        """
        csv のリストから不要なデータを除外．
        除外対象
        - 辞書に 読み が登録されていない項目
        - 重複項目
        """
        if not isinstance(csv_list, list):
            logger.warning("Input value is not List: %s." % csv_list)

        sanitized_data_list = []
        unique_word_list = []
        for csv_data in csv_list:
            if not self._can_read(csv_data):
                logger.debug("Unreadable: %s." % csv_data[self.WORD])
            elif csv_data[self.WORD] in unique_word_list:
                logger.debug("Duplicated: %s." % csv_data[self.WORD])
            else:
                sanitized_data_list.append(csv_data)
                unique_word_list.append(csv_data[self.WORD])
        return sanitized_data_list

    def _can_read(self, csv_data):
        """
        辞書に 読み が登録されている場合，True を返す．
        特殊な音(フォ，ウォ など)は登録されている場合といない場合とがあるので注意．
        """
        if not isinstance(csv_data, list):
            logger.warning("Input value is not List: %s." % csv_data)

        logger.debug("--------------------------------------")
        logger.debug(csv_data)
        if len(csv_data) <= self.PRONOUNCIATION:
            return False
        elif csv_data[self.PART] == u'記号':
            return False
        elif csv_data[self.PART] is '名詞' and \
                csv_data[self.PART_SUBTYPE is 'サ変接続']:
            return False
        else:
            return True

    def _extract_data(self, csv_data_list):
        """
        出力したいデータごとに構築された辞書を返す．
        子クラスでオーバーライドして使う．
        """
        raise NotImplementedError
