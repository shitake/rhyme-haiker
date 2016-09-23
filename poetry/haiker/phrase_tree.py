# -*- coding: utf-8 -*-

from logging import getLogger
from logging import StreamHandler
from logging import DEBUG

from poetry.data_constructor.words import Words
from poetry.data_constructor.words_data import WordsData

logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)


class PhraseTree(object):

    """
    ルートツリーを current_words = tuple('root') で定義する．
    """
    ROOT = tuple('root')

    def __init__(self, current_words=tuple(), possible_next_words=list(), next_tree=None, parent=None):
        self.current_words = current_words  # Words クラスのタプル
        self.possible_next_words = possible_next_words  # リストのリスト
        self.next_tree = next_tree
        self.parent = parent

    @property
    def current_words(self):
        return self._current_words

    @current_words.setter
    def current_words(self, words_tuple):
        """
        文字列タプルから Words クラスタプルを作成．
        """
        assert words_tuple is not None, 'words_tuple is None'
        if words_tuple == self.ROOT:
            pass
        else:
            words_tuple = tuple(self._dispatch(word) for word in words_tuple)
        self._current_words = words_tuple

    def _dispatch(self, word):
        """
        Words クラスオブジェクトの場合，そのまま返す．
        そうでない場合，Words クラスオブジェクトを返す．
        """
        if isinstance(word, Words):
            return word
        else:
            return Words(self._search_dict(word))

    def _search_dict(self, word):
        """
        単語をもとに，対応する辞書を検索．
        """
        assert WordsData.words_data is not None and WordsData.words_data != [], "WordsData is not given."
        assert isinstance(word, str)
        for word_dict in WordsData.words_data:
            if word_dict["word"] == word:
                return word_dict
        return

    @classmethod
    def define_root(cls, possible_next_words=list()):
        """
        ルートツリーを作成
        """
        return PhraseTree(current_words=cls.ROOT,
                          possible_next_words=possible_next_words)

    @classmethod
    def get_text(cls, phrase_tree):
        """
        現在の文章を返す．
        """
        if cls.is_root(phrase_tree.parent):
            text_list = [word.word for word in phrase_tree.current_words]
            return cls._list2str(text_list)
        else:
            last_word = phrase_tree.current_words[-1].word
            return cls.get_text(phrase_tree.parent) + last_word

    @classmethod
    def get_text_list(cls, phrase_tree):
        """
        現在の文章をリストとして返す．
        """
        if cls.is_root(phrase_tree.parent):
            return [word.word for word in phrase_tree.current_words]
        else:
            last_word = [phrase_tree.current_words[-1].word]
            return cls.get_text_list(phrase_tree.parent) + last_word

    @classmethod
    def get_text_vowel(cls, phrase_tree):
        """
        現在の文章の読みを返す．
        """
        if cls.is_root(phrase_tree.parent):
            vowel_list = [word.vowel for word in phrase_tree.current_words]
            return cls._list2str(vowel_list)
        else:
            last_word_vowel = phrase_tree.current_words[-1].vowel
            return cls.get_text_vowel(phrase_tree.parent) + last_word_vowel

    @classmethod
    def count_phrase_len(cls, phrase_tree):
        """
        現在の文字数を返す．
        phrase_tree.next_tree が None ではないことが前提．
        """
        if cls.is_root(phrase_tree.parent):
            # 先頭3語
            assert phrase_tree is not None, 'phrase_tree is None'
            return sum([word.length for word in phrase_tree.current_words])
        else:
            last_word_length = cls._len_last_word(phrase_tree)
            return cls.count_phrase_len(phrase_tree.parent) + last_word_length

    @classmethod
    def _len_last_word(cls, phrase_tree):
        """
        末尾の要素の読みの長さを返す．
        """
        return phrase_tree.current_words[-1].length

    @classmethod
    def get_last_words(cls, phrase_tree):
        """
        句の末尾3語を返す
        """
        if phrase_tree.next_tree is None:
            return phrase_tree.current_words
        else:
            return cls.get_last_words(phrase_tree.next_tree)

    @classmethod
    def is_root(cls, phrase_tree):
        """
        ツリーがルートの場合，真
        """
        assert phrase_tree is not None
        if phrase_tree.current_words == cls.ROOT:
            return True
        else:
            return False

    @classmethod
    def _list2str(cls, text_list):
        return "".join(text_list)

    @classmethod
    def get_last_tree(cls, phrase_tree):
        """
        最深部のツリーを返す．
        """
        if not phrase_tree.next_tree:
            return phrase_tree
        else:
            return cls.get_last_tree(phrase_tree.next_tree)

    @classmethod
    def disclose(cls, phrase_tree, place):
        """
        デバッグ用
        """
        if not cls.is_root(phrase_tree):
            print("place: ", place)
            print(phrase_tree.current_words[0].word)
            print(phrase_tree.current_words[1].word)
            print(phrase_tree.current_words[2].word)
            print(phrase_tree.possible_next_words)
