# -*- coding: utf-8 -*-

import logging
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy import Sequence
from sqlalchemy import UniqueConstraint
from poetry.data_constructor import table_creator
from poetry.data_constructor.table_creator import TableCreator

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())


class ChainsCreator(TableCreator):

    def _definer(self, data):
        """
        Chains テーブルのオブジェクトを返す．
        """
        return Chains(
            data["current_word"],
            data["next_word"]
        )


class Chains(table_creator.Base):
    __tablename__ = 'chains'

    chain_id = Column(Integer, Sequence('chain_id_seq'), primary_key=True)
    current_word = Column(String, ForeignKey("words.word"), nullable=False)
    next_word = Column(String, ForeignKey("words.word"), nullable=False)
    UniqueConstraint('current_word', 'next_word')

    def __init__(self, current_word, next_word):
        self.current_word = current_word
        self.next_word = next_word

    def __repr__(self):
        return "<Chains('%s', '%s')>" % (self.current_word, self.next_word)
