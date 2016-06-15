# -*- coding: utf-8 -*-

import logging
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Sequence
from poetry.data_constructor import table_creator
from poetry.data_constructor.table_creator import TableCreator

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())


class WordsCreator(TableCreator):

    def _definer(self, data):
        """
        Words テーブルのオブジェクトを返す．
        """
        return Words(
            data["word"],
            data["part"],
            data["vowel"],
            data["length"]
        )


class Words(table_creator.Base):
    __tablename__ = 'words'

    word_id = Column(Integer, Sequence('word_id_seq'), primary_key=True)
    word = Column(String, nullable=False, unique=True)
    vowel = Column(String, nullable=False)
    length = Column(Integer, nullable=False)
    part = Column(String, nullable=False)

    def __init__(self, word, part, vowel, length):
        # self.word_id = word_id
        self.word = word
        self.part = part
        self.vowel = vowel
        self.length = length

    def __repr__(self):
        return "<Words('%s', '%s', '%s', '%s')>" % (self.word, self.part, self.vowel, self.length)

if __name__ == '__main__':
    # data = [{'vowel': 'ウウ', 'word': 'する', 'length': 2, 'part': '動詞'}]
    data = [{'vowel': 'オンエウ', 'word': '今月', 'length': 4, 'part': '名詞'}, {'vowel': 'イイ', 'word': '１', 'length': 2, 'part': '名詞'}, {'vowel': 'オン', 'word': '４', 'length': 2, 'part': '名詞'}, {'vowel': 'イイ', 'word': '日', 'length': 2, 'part': '名詞'}, {'vowel': 'イ', 'word': 'に', 'length': 1, 'part': '助詞'}, {'vowel': 'ウアオオ', 'word': '熊本', 'length': 4, 'part': '名詞'}, {'vowel': 'エン', 'word': '県', 'length': 2, 'part': '名詞'}, {'vowel': 'エ', 'word': 'で', 'length': 1, 'part': '助詞'}, {'vowel': 'インオ', 'word': '震度', 'length': 3, 'part': '名詞'}, {'vowel': 'アア', 'word': '７', 'length': 2, 'part': '名詞'}, {'vowel': 'オ', 'word': 'の', 'length': 1, 'part': '助詞'}, {'vowel': 'アエイイ', 'word': '激しい', 'length': 4, 'part': '形容詞'}, {'vowel': 'ウエ', 'word': '揺れ', 'length': 2, 'part': '名詞'}, {'vowel': 'オ', 'word': 'を', 'length': 1, 'part': '助詞'}, {'vowel': 'アンオウ', 'word': '観測', 'length': 4, 'part': '名詞'}, {'vowel': 'イ', 'word': 'し', 'length': 1, 'part': '動詞'}, {'vowel': 'ア', 'word': 'た', 'length': 1, 'part': '助動詞'}, {'vowel': 'イイン', 'word': '地震', 'length': 3, 'part': '名詞'}, {'vowel': 'ア', 'word': 'が', 'length': 1, 'part': '助詞'}, {'vowel': 'オイ', 'word': '起き', 'length': 2, 'part': '動詞'}, {'vowel': 'エ', 'word': 'て', 'length': 1, 'part': '助詞'}, {'vowel': 'イオー', 'word': '以降', 'length': 3, 'part': '名詞'}, {'vowel': 'オ', 'word': 'と', 'length': 1, 'part': '助詞'}, {'vowel': 'オーイア', 'word': '大分', 'length': 4, 'part': '名詞'}, {'vowel': 'ア', 'word': 'は', 'length': 1, 'part': '助詞'}, {'vowel': 'アッアウ', 'word': '活発', 'length': 4, 'part': '名詞'}, {'vowel': 'ア', 'word': 'な', 'length': 1, 'part': '助動詞'}, {'vowel': 'アウオー', 'word': '活動', 'length': 4, 'part': '名詞'}, {'vowel': 'ウウイ', 'word': '続き', 'length': 3, 'part': '動詞'}, {'vowel': 'イオー', 'word': '以上', 'length': 3, 'part': '名詞'}, {'vowel': 'アイウー', 'word': '回数', 'length': 4, 'part': '名詞'}, {'vowel': 'アイ', 'word': '８', 'length': 2, 'part': '名詞'}, {'vowel': 'エオ', 'word': '０', 'length': 2, 'part': '名詞'}, {'vowel': 'アイ', 'word': '回', 'length': 2, 'part': '名詞'}, {'vowel': 'オエ', 'word': '超え', 'length': 2, 'part': '動詞'}, {'vowel': 'イ', 'word': 'い', 'length': 1, 'part': '動詞'}, {'vowel': 'アウ', 'word': 'ます', 'length': 2, 'part': '助動詞'}, {'vowel': 'イアイ', 'word': '被災', 'length': 3, 'part': '名詞'}, {'vowel': 'イ', 'word': '地', 'length': 1, 'part': '名詞'}, {'vowel': 'イオイ', 'word': '広い', 'length': 3, 'part': '形容詞'}, {'vowel': 'アンイ', 'word': '範囲', 'length': 3, 'part': '名詞'}, {'vowel': 'アエ', 'word': '雨', 'length': 2, 'part': '名詞'}, {'vowel': 'ウッ', 'word': '降っ', 'length': 2, 'part': '動詞'}, {'vowel': 'イオーオー', 'word': '気象庁', 'length': 5, 'part': '名詞'}, {'vowel': 'イイウウイ', 'word': '引き続き', 'length': 5, 'part': '副詞'}, {'vowel': 'オオアウ', 'word': '伴う', 'length': 4, 'part': '動詞'}, {'vowel': 'ア', 'word': 'や', 'length': 1, 'part': '助詞'}, {'vowel': 'イオウ', 'word': 'による', 'length': 3, 'part': '助詞'}, {'vowel': 'オア', 'word': '土砂', 'length': 2, 'part': '名詞'}, {'vowel': 'アイアイ', 'word': '災害', 'length': 4, 'part': '名詞'}, {'vowel': 'エイアイ', 'word': '警戒', 'length': 4, 'part': '名詞'}, {'vowel': 'ウウ', 'word': 'する', 'length': 2, 'part': '動詞'}, {'vowel': 'オー', 'word': 'よう', 'length': 2, 'part': '名詞'}, {'vowel': 'オイアエ', 'word': '呼びかけ', 'length': 4, 'part': '動詞'}, {'vowel': 'オウ', 'word': '夜', 'length': 2, 'part': '名詞'}, {'vowel': 'アイイ', 'word': '益城', 'length': 3, 'part': '名詞'}, {'vowel': 'アイ', 'word': '町', 'length': 2, 'part': '名詞'}, {'vowel': 'アッエイ', 'word': '発生', 'length': 4, 'part': '名詞'}, {'vowel': 'アオ', 'word': 'あと', 'length': 2, 'part': '名詞'}, {'vowel': 'ウーアン', 'word': '週間', 'length': 4, 'part': '名詞'}, {'vowel': 'アエ', 'word': '前', 'length': 2, 'part': '名詞'}, {'vowel': 'オウ', 'word': '６', 'length': 2, 'part': '名詞'}, {'vowel': 'イエイ', 'word': '未明', 'length': 3, 'part': '名詞'}, {'vowel': 'イイアア', 'word': '西原', 'length': 4, 'part': '名詞'}, {'vowel': 'ウア', 'word': '村', 'length': 2, 'part': '名詞'}, {'vowel': 'アイ', 'word': 'まし', 'length': 2, 'part': '助動詞'}, {'vowel': 'イ', 'word': '２', 'length': 1, 'part': '名詞'}, {'vowel': 'オ', 'word': 'も', 'length': 1, 'part': '助詞'}, {'vowel': 'オオ', 'word': '午後', 'length': 2, 'part': '名詞'}, {'vowel': 'イ', 'word': '時', 'length': 1, 'part': '名詞'}, {'vowel': 'ウン', 'word': '分', 'length': 2, 'part': '名詞'}, {'vowel': 'オオ', 'word': 'ごろ', 'length': 2, 'part': '名詞'}, {'vowel': 'イオー', 'word': '地方', 'length': 3, 'part': '名詞'}, {'vowel': 'インエン', 'word': '震源', 'length': 4, 'part': '名詞'}, {'vowel': 'アウイウーオ', 'word': 'マグニチュード', 'length': 6, 'part': '名詞'}, {'vowel': 'アン', 'word': '３', 'length': 2, 'part': '名詞'}, {'vowel': '．', 'word': '．', 'length': 1, 'part': '名詞'}, {'vowel': 'アイ', 'word': 'あり', 'length': 2, 'part': '動詞'}, {'vowel': 'イ', 'word': '市', 'length': 1, 'part': '名詞'}, {'vowel': 'イイ', 'word': '西', 'length': 2, 'part': '名詞'}, {'vowel': 'ウ', 'word': '区', 'length': 1, 'part': '名詞'}]
    wc = WordsCreator()
    wc.create_table(data)
