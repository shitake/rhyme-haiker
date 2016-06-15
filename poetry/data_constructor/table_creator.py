# -*- coding: utf-8 -*-

import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())


class TableCreator:

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

    def _construct_obj_list(self, data):
        """
        データをテーブルに合わせて整形し，
        そのリストを返す
        """
        # sanitized_data_list = self._sanitize(data)
        return [self._definer(d) for d in data if d]

    def _definer(self, data):
        """
        テーブルごとのオブジェクトを定義する．
        子クラスでオーバーライドする．
        """

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
