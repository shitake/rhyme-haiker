# -*- coding: utf-8 -*-

import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())


class TableCreator:

    def __init__(self):
        # self.data = data  # TODO: データが不正でないことのチェック
        self.Base = object

    def db_session_creator(func):
        """
        作成したデータをテーブルへ格納するための
        前後の処理を書いたデコレータ．
        """

        def wrapper(self, *args):
            session = self._init_db_conf()
            # テーブルが存在するか確認，ないなら作成
            # データ挿入

            # オブジェクトの新規追加
            func(self, *args, session=session)

            session.commit()
            logger.info("Commit.")

        return wrapper

    def _init_db_conf(self):
        """
        DB接続設定を初期化し，
        セッションを返す．
        """
        engine = create_engine(
            'postgresql+psycopg2://pochi:pochi@localhost:5432/haiku',
            echo=True
        )

        Base.metadata.drop_all(engine, checkfirst=True)  # TODO: 削除せずに，upsert できるようにしたい
        Base.metadata.create_all(engine, checkfirst=True)
        # セッションの作成
        Session = sessionmaker(bind=engine)
        return Session()

    @db_session_creator
    def create_table(self, table_data, session):
        """
        テーブルへ挿入したいデータリストを入力とし，
        データ整形後，挿入を行う．
        """
        session.add_all(
            self._construct_obj_list(
                table_data,
            )
        )

    # @db_session_creator
    # def create_words_table(self, words_table_data, session):
    #     """
    #     単語ごとの
    #     読み，品詞，字数
    #     テーブルを作成．
    #     """
    #     session.add_all(
    #         self._construct_obj_list(
    #             words_table_data,
    #             self._define_words_obj
    #         )
    #     )  # TODO: upsert したい

    # @db_session_creator
    # def create_chains_table(self, chains_table_data, session):
    #     """
    #     現在の単語とそれに続く単語
    #     のテーブルを作成．
    #     """
    #     session.add_all(
    #         self._construct_obj_list(
    #             chains_table_data,
    #         )
    #     )

    def _construct_obj_list(self, data):
        """
        データをテーブルに合わせて整形し，
        そのリストを返す
        """
        # sanitized_data_list = self._sanitize(data)
        return [self._definer(d) for d in data if d]

    def _definer(self, data):
        """
        子クラスでオーバーライドする
        """

    # def _define_words_obj(self, data):
    #     """
    #     Words テーブルのオブジェクトを返す．
    #     """
    #     return Words(
    #         data["word"],
    #         data["part"],
    #         data["vowel"],
    #         data["length"]
    #     )

    # def _define_chains_obj(self, data):
    #     """
    #     Chains テーブルのオブジェクトを返す．
    #     """
    #     return Chains(
    #         data["current_word"],
    #         data["next_word"]
    #     )

    def _exists_table(self):
        """
        テーブルが存在する場合 True を返す．
        """

    def _sanitize(self, words_table_data):
        """
        入力データに不正値が含まれていないか確認
        """
        # TODO: None を弾く
        # TODO: 重複データを弾く
        return [d for d in words_table_data if d]


# テーブル生成とクラスマッピング
Base = declarative_base()


# class Words(Base):
#     __tablename__ = 'words'
#
#     word_id = Column(Integer, Sequence('word_id_seq'), primary_key=True)
#     word = Column(String, nullable=False, unique=True)
#     vowel = Column(String, nullable=False)
#     length = Column(Integer, nullable=False)
#     part = Column(String, nullable=False)
#
#     def __init__(self, word, part, vowel, length):
#         # self.word_id = word_id
#         self.word = word
#         self.part = part
#         self.vowel = vowel
#         self.length = length
#
#     def __repr__(self):
#         return "<Words('%s', '%s', '%s', '%s')>" % (self.word, self.part, self.vowel, self.length)


# class Chains(Base):
#     __tablename__ = 'chains'
#
#     chain_id = Column(Integer, Sequence('chain_id_seq'), primary_key=True)
#     current_word = Column(String, ForeignKey("words.word"), nullable=False)
#     next_word = Column(String, ForeignKey("words.word"), nullable=False)
#     UniqueConstraint('current_word', 'next_word')
#
#     def __init__(self, current_word, next_word):
#         self.current_word = current_word
#         self.next_word = next_word
#
#     def __repr__(self):
#         return "<Chains('%s', '%s')>" % (self.current_word, self.next_word)


if __name__ == '__main__':
    # data = [{'vowel': 'ウウ', 'word': 'する', 'length': 2, 'part': '動詞'}]
    data = [{'vowel': 'オンエウ', 'word': '今月', 'length': 4, 'part': '名詞'}, {'vowel': 'イイ', 'word': '１', 'length': 2, 'part': '名詞'}, {'vowel': 'オン', 'word': '４', 'length': 2, 'part': '名詞'}, {'vowel': 'イイ', 'word': '日', 'length': 2, 'part': '名詞'}, {'vowel': 'イ', 'word': 'に', 'length': 1, 'part': '助詞'}, {'vowel': 'ウアオオ', 'word': '熊本', 'length': 4, 'part': '名詞'}, {'vowel': 'エン', 'word': '県', 'length': 2, 'part': '名詞'}, {'vowel': 'エ', 'word': 'で', 'length': 1, 'part': '助詞'}, {'vowel': 'インオ', 'word': '震度', 'length': 3, 'part': '名詞'}, {'vowel': 'アア', 'word': '７', 'length': 2, 'part': '名詞'}, {'vowel': 'オ', 'word': 'の', 'length': 1, 'part': '助詞'}, {'vowel': 'アエイイ', 'word': '激しい', 'length': 4, 'part': '形容詞'}, {'vowel': 'ウエ', 'word': '揺れ', 'length': 2, 'part': '名詞'}, {'vowel': 'オ', 'word': 'を', 'length': 1, 'part': '助詞'}, {'vowel': 'アンオウ', 'word': '観測', 'length': 4, 'part': '名詞'}, {'vowel': 'イ', 'word': 'し', 'length': 1, 'part': '動詞'}, {'vowel': 'ア', 'word': 'た', 'length': 1, 'part': '助動詞'}, {'vowel': 'イイン', 'word': '地震', 'length': 3, 'part': '名詞'}, {'vowel': 'ア', 'word': 'が', 'length': 1, 'part': '助詞'}, {'vowel': 'オイ', 'word': '起き', 'length': 2, 'part': '動詞'}, {'vowel': 'エ', 'word': 'て', 'length': 1, 'part': '助詞'}, {'vowel': 'イオー', 'word': '以降', 'length': 3, 'part': '名詞'}, {'vowel': 'オ', 'word': 'と', 'length': 1, 'part': '助詞'}, {'vowel': 'オーイア', 'word': '大分', 'length': 4, 'part': '名詞'}, {'vowel': 'ア', 'word': 'は', 'length': 1, 'part': '助詞'}, {'vowel': 'アッアウ', 'word': '活発', 'length': 4, 'part': '名詞'}, {'vowel': 'ア', 'word': 'な', 'length': 1, 'part': '助動詞'}, {'vowel': 'アウオー', 'word': '活動', 'length': 4, 'part': '名詞'}, {'vowel': 'ウウイ', 'word': '続き', 'length': 3, 'part': '動詞'}, {'vowel': 'イオー', 'word': '以上', 'length': 3, 'part': '名詞'}, {'vowel': 'アイウー', 'word': '回数', 'length': 4, 'part': '名詞'}, {'vowel': 'アイ', 'word': '８', 'length': 2, 'part': '名詞'}, {'vowel': 'エオ', 'word': '０', 'length': 2, 'part': '名詞'}, {'vowel': 'アイ', 'word': '回', 'length': 2, 'part': '名詞'}, {'vowel': 'オエ', 'word': '超え', 'length': 2, 'part': '動詞'}, {'vowel': 'イ', 'word': 'い', 'length': 1, 'part': '動詞'}, {'vowel': 'アウ', 'word': 'ます', 'length': 2, 'part': '助動詞'}, {'vowel': 'イアイ', 'word': '被災', 'length': 3, 'part': '名詞'}, {'vowel': 'イ', 'word': '地', 'length': 1, 'part': '名詞'}, {'vowel': 'イオイ', 'word': '広い', 'length': 3, 'part': '形容詞'}, {'vowel': 'アンイ', 'word': '範囲', 'length': 3, 'part': '名詞'}, {'vowel': 'アエ', 'word': '雨', 'length': 2, 'part': '名詞'}, {'vowel': 'ウッ', 'word': '降っ', 'length': 2, 'part': '動詞'}, {'vowel': 'イオーオー', 'word': '気象庁', 'length': 5, 'part': '名詞'}, {'vowel': 'イイウウイ', 'word': '引き続き', 'length': 5, 'part': '副詞'}, {'vowel': 'オオアウ', 'word': '伴う', 'length': 4, 'part': '動詞'}, {'vowel': 'ア', 'word': 'や', 'length': 1, 'part': '助詞'}, {'vowel': 'イオウ', 'word': 'による', 'length': 3, 'part': '助詞'}, {'vowel': 'オア', 'word': '土砂', 'length': 2, 'part': '名詞'}, {'vowel': 'アイアイ', 'word': '災害', 'length': 4, 'part': '名詞'}, {'vowel': 'エイアイ', 'word': '警戒', 'length': 4, 'part': '名詞'}, {'vowel': 'ウウ', 'word': 'する', 'length': 2, 'part': '動詞'}, {'vowel': 'オー', 'word': 'よう', 'length': 2, 'part': '名詞'}, {'vowel': 'オイアエ', 'word': '呼びかけ', 'length': 4, 'part': '動詞'}, {'vowel': 'オウ', 'word': '夜', 'length': 2, 'part': '名詞'}, {'vowel': 'アイイ', 'word': '益城', 'length': 3, 'part': '名詞'}, {'vowel': 'アイ', 'word': '町', 'length': 2, 'part': '名詞'}, {'vowel': 'アッエイ', 'word': '発生', 'length': 4, 'part': '名詞'}, {'vowel': 'アオ', 'word': 'あと', 'length': 2, 'part': '名詞'}, {'vowel': 'ウーアン', 'word': '週間', 'length': 4, 'part': '名詞'}, {'vowel': 'アエ', 'word': '前', 'length': 2, 'part': '名詞'}, {'vowel': 'オウ', 'word': '６', 'length': 2, 'part': '名詞'}, {'vowel': 'イエイ', 'word': '未明', 'length': 3, 'part': '名詞'}, {'vowel': 'イイアア', 'word': '西原', 'length': 4, 'part': '名詞'}, {'vowel': 'ウア', 'word': '村', 'length': 2, 'part': '名詞'}, {'vowel': 'アイ', 'word': 'まし', 'length': 2, 'part': '助動詞'}, {'vowel': 'イ', 'word': '２', 'length': 1, 'part': '名詞'}, {'vowel': 'オ', 'word': 'も', 'length': 1, 'part': '助詞'}, {'vowel': 'オオ', 'word': '午後', 'length': 2, 'part': '名詞'}, {'vowel': 'イ', 'word': '時', 'length': 1, 'part': '名詞'}, {'vowel': 'ウン', 'word': '分', 'length': 2, 'part': '名詞'}, {'vowel': 'オオ', 'word': 'ごろ', 'length': 2, 'part': '名詞'}, {'vowel': 'イオー', 'word': '地方', 'length': 3, 'part': '名詞'}, {'vowel': 'インエン', 'word': '震源', 'length': 4, 'part': '名詞'}, {'vowel': 'アウイウーオ', 'word': 'マグニチュード', 'length': 6, 'part': '名詞'}, {'vowel': 'アン', 'word': '３', 'length': 2, 'part': '名詞'}, {'vowel': '．', 'word': '．', 'length': 1, 'part': '名詞'}, {'vowel': 'アイ', 'word': 'あり', 'length': 2, 'part': '動詞'}, {'vowel': 'イ', 'word': '市', 'length': 1, 'part': '名詞'}, {'vowel': 'イイ', 'word': '西', 'length': 2, 'part': '名詞'}, {'vowel': 'ウ', 'word': '区', 'length': 1, 'part': '名詞'}]
    tc = TableCreator()
    tc.create_words_table(data)
