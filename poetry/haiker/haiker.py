# -*- coding: utf-8 -*-

from logging import getLogger
from logging import StreamHandler
from logging import DEBUG
import random

from poetry.data_constructor.chains_data import ChainsData
from poetry.data_constructor.words_data import WordsData
from poetry.haiker.phrase import Phrase
from poetry.haiker.phrase_tree import PhraseTree
from poetry.rhymer.rhymer import Rhymer

logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)


class Haiker:

    FIVE = 5
    SEVEN = 7
    TWELVE = 12
    VOWEL = "vowel"
    WORD = "word"
    words = None

    def compose(self):
        """
        俳句を詠む．
        """
        first_loop_limit = 500
        first_current_loop = 0
        while True:
            logger.debug('+++ current loop: {} +++'.format(first_current_loop))

            first_current_loop += 1
            if first_current_loop == first_loop_limit:
                return "***** だめでした *****"

            try:
                root = PhraseTree.define_root(possible_next_words=self._get_word_list())
                first_phrase_tree = self.construct_syllable(root, self.FIVE)
                first_text_list = Phrase.text_list
                PhraseTree.disclose(first_phrase_tree, "first -------------")
            except ValueError:
                logger.debug('***** first ValueError *****')
                continue

            try:
                root = PhraseTree.define_root(possible_next_words=first_phrase_tree.possible_next_words)
                second_phrase_tree = self.construct_syllable(root, self.SEVEN)
                second_last_vowel = Phrase.last_vowel
                second_text_list = Phrase.text_list
                PhraseTree.disclose(second_phrase_tree, "second -------------")
            except ValueError:
                logger.debug('***** second ValueError *****')
                continue

            try:
                root = PhraseTree.define_root(possible_next_words=second_phrase_tree.possible_next_words)
                third_phrase_tree = self.construct_syllable(root, self.FIVE)
                third_last_vowel = Phrase.last_vowel
                third_text_list = Phrase.text_list
                PhraseTree.disclose(third_phrase_tree, "third -------------")
            except ValueError:
                logger.debug('***** third ValueError *****')
                continue

            if Rhymer.is_rhymed(second_last_vowel, third_last_vowel):
                haiku = "".join(first_text_list + second_text_list + third_text_list)
                logger.debug("[Haiku] >>> {}".format(haiku))

                return haiku

    def property_initializer(func):
        """
        5, 7, 5 の各句を詠む前の初期化処理を行うためのデコレータ．
        """

        def wrapper(self, phrase_tree, expected_vowel_len):
            logger.debug("[Initialized]")
            ret = func(self, phrase_tree, expected_vowel_len)
            return ret

        return wrapper

    @property_initializer
    def construct_syllable(self, phrase_tree, expected_vowel_len, noun=False):
        """
        最初の音節を作成する．

        Args:
          phrase_tree: PhraseTree クラスオブジェクト
          expected_vowel_len: 音節の読みの長さ
        Returns:
          音節
        """
        # phrase_tree には，current と next が格納済み
        while True:
            if self._is_empty_first_node(phrase_tree):
                raise ConstructionError('First node has become empty.')
            while True:
                # 単語タプルをランダムに1つ取得
                try:
                    PhraseTree.disclose(phrase_tree, "construct ---------")
                    phrase_tree, phrase_tree.next_tree = self._get_word(phrase_tree)
                    PhraseTree.disclose(phrase_tree, "construct 2 ---------")
                except ValueError:
                    logger.info('*** Cnstruction failed ***')
                    raise
                if phrase_tree.next_tree is None:
                    break

                text_vowel_len = PhraseTree.count_phrase_len(phrase_tree.next_tree)

                if phrase_tree.possible_next_words == list():
                    try:
                        phrase_tree = self._back_prev_word_list(phrase_tree)
                    except ValueError:
                        logger.info('*** Cnstruction failed ***')
                        raise
                elif self._is_n_char(expected_vowel_len, text_vowel_len):
                    assert phrase_tree is not None, "phrase_tree is None"
                    self._post_proc(phrase_tree.next_tree)
                    return phrase_tree.next_tree
                elif self._is_less_than_n_char(expected_vowel_len, text_vowel_len):
                    # 次の単語タプルを取得する前の処理
                    phrase_tree = phrase_tree.next_tree
                    assert phrase_tree is not None, "phrase_tree is None"
                    break
                else:
                    # 5文字より長くなったら別の単語を取得しなおす
                    # 現在の next_tree を破棄する
                    pass

    def _post_proc(self, phrase_tree):
        """
        句生成完了後の処理．
        - 最後の3語を保持
        - 生成した句の読みを保持
        - 生成した句をリストとして保持

        - 生成した句を保持

        Args:
          最後の PhraseTree インスタンス
        Returns:
          Phrase インスタンス
        """
        assert phrase_tree is not None
        assert not PhraseTree.is_root(phrase_tree), "phrase_tree is not root"
        Phrase.text_list = PhraseTree.get_text_list(phrase_tree)
        Phrase.last_words = PhraseTree.get_last_words(phrase_tree)
        Phrase.last_vowel = PhraseTree.get_text_vowel(phrase_tree)

    def _get_word_list(self):
        """単語リストの取得"""
        return list(ChainsData.chains_data.keys())

    def _is_empty_first_node(self, phrase_tree):
        """
        最初のノードが空の場合真
        """
        if phrase_tree.current_words is None \
                and phrase_tree.possible_next_words == list():
            return True
        else:
            return False

    def _get_word(self, phrase_tree, seed=None, max_iterations=100):
        """
        単語リストからランダムに1つ取得．
        next_tree を取得的ない場合，None が代入される．
        """
        next_tree = None
        for index in range(max_iterations):
            if not phrase_tree.possible_next_words:
                # possible_next_words が None, []
                if PhraseTree.is_root(phrase_tree):
                    raise ValueError("Impossible to get word cause of Root Tree doesn't have any possible next words")
                return phrase_tree.parent, None
            else:
                if seed is None:
                    random.shuffle(phrase_tree.possible_next_words)
                    seed = phrase_tree.possible_next_words[-1]  # if 文外で remove するため pop ではない
                phrase_tree.possible_next_words.remove(seed)

                if seed in self._get_word_list() and \
                   ChainsData.chains_data[seed] != [None]:
                    if ChainsData.chains_data[seed] == [None]:
                        # この時点では，seed は文字列のタプルであり，Words クラスのタプルではない
                        pass
                    assert ChainsData.chains_data[seed] != [None], "ChainsData.chains_data: {}".format(ChainsData.chains_data)
                    next_tree = PhraseTree(current_words=seed,
                                           possible_next_words=ChainsData.chains_data[seed],
                                           parent=phrase_tree)
                    break
            seed = None

        assert phrase_tree is not None, "phrase_tree is None"
        return phrase_tree, next_tree

    def _get_vowel(self, word):
        """
        単語の読みを返す
        """
        for word_dict in WordsData.words_data:
            if word_dict[self.WORD] == word:
                return word_dict[self.VOWEL]
        raise ValueError('Vowel does not exist. WordsData is broken.')

    def _back_prev_word_list(self, phrase_tree):
        """
        単語リストが空になったら，前の単語リストに戻る
        """
        if PhraseTree.is_root(phrase_tree):
            raise ValueError('Impossible to back prev word list')
        return phrase_tree.parent

    def _is_n_char(self, n, text_vowel_len):
        """
        与えられた文章(発音)が n 文字であれば真．

        Args:
          n: 文字数．int．
          text: 文章(発音)．
        """
        if text_vowel_len == n:
            return True
        else:
            return False

    def _is_less_than_n_char(self, n, text_vowel_len):
        """
        与えられた文章が，n文字未満であれば真
        """
        if text_vowel_len < n:
            return True
        else:
            return False


class ConstructionError(Exception):

    def __init__(self, last_five, last_seven):
        self.last_five = last_five
        self.last_seven = last_seven

    def __str__(self):
        return repr(self.last_five, self.last_seven)
