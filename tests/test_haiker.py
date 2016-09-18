# -*- coding: utf-8 -*-

from poetry.data_constructor.chains_data import ChainsData
from poetry.data_constructor.words import Words
from poetry.data_constructor.words_data import WordsData
from poetry.haiker.haiker import Haiker
from poetry.haiker.phrase import Phrase
from poetry.haiker.phrase_tree import PhraseTree
import unittest


class TestHaiker(unittest.TestCase):

    SUCCESS_WORDS = [
        {
            "word": "あああ",
            "vowel": "アアア",
            "length": 3,
            "part": "名詞"
        },
        {
            "word": "いいい",
            "vowel": "イイイ",
            "length": 3,
            "part": "名詞"
        },
        {
            "word": "ううう",
            "vowel": "ウウウ",
            "length": 3,
            "part": "名詞"
        }
    ]
    SUCCESS_CHAINS = {
        ('あああ', 'いいい', 'ううう'): [
            'あああ'
        ],
        ('いいい', 'ううう', 'あああ'): [
            'いいい'
        ],
        ('ううう', 'あああ', 'いいい'): [
            'ううう'
        ]
    }
    SUCCESS_WORDS_TWELVE = [
        {
            "word": "ああああ",
            "vowel": "アアアア",
            "length": 4,
            "part": "名詞"
        },
        {
            "word": "いいいい",
            "vowel": "イイイイ",
            "length": 4,
            "part": "名詞"
        },
        {
            "word": "うううう",
            "vowel": "ウウウウ",
            "length": 4,
            "part": "名詞"
        }
    ]
    SUCCESS_CHAINS_TWELVE = {
        ('ああああ', 'いいいい', 'うううう'): [
            'ああああ'
        ],
        ('いいいい', 'うううう', 'ああああ'): [
            'いいいい'
        ],
        ('うううう', 'ああああ', 'いいいい'): [
            'うううう'
        ]
    }
    WORDS = [
        {
            "word": "古池",
            "vowel": "ウウイエ",
            "length": 4,
            "part": "名詞"
        },
        {
            "word": "蛙",
            "vowel": "アエウ",
            "length": 3,
            "part": "名詞"
        },
        {
            "word": "あ",
            "vowel": "ア",
            "length": 1,
            "part": "名詞"
        },
        {
            "word": "い",
            "vowel": "イ",
            "length": 1,
            "part": "名詞"
        },
        {
            "word": "う",
            "vowel": "ウ",
            "length": 1,
            "part": "名詞"
        }
    ]
    CHAINS = {
        ('あ', '古池', 'い'): [
            '古池'
        ],
        ('あ', '蛙', 'い'): [
            None
        ],
        ('い', '古池', 'う'): [
            '蛙'
        ],
        ('古池', 'あ', '古池'): [
            'い'
        ],
        ('古池', 'う', '蛙'): [
            'あ'
        ],
        ('古池', 'い', '古池'): [
            'う'
        ],
        ('蛙', 'あ', '蛙'): [
            'い'
        ],
        ('う', '蛙', 'あ'): [
            '蛙'
        ]
    }
    EMPTY_TEXT = ''
    EMPTY_LIST = []
    EMPTY_DICT = {}

    TWELVE = 12

    def test_construct_syllable(self):
        WordsData.words_data = self.SUCCESS_WORDS_TWELVE
        ChainsData.chains_data = self.SUCCESS_CHAINS_TWELVE
        haiker = Haiker()
        root = PhraseTree.define_root(possible_next_words=list(self.SUCCESS_CHAINS_TWELVE.keys()))

        self.assertIsInstance(haiker.construct_syllable(root, self.TWELVE),
                              PhraseTree)

        pt = haiker.construct_syllable(root, self.TWELVE)
        self.assertEqual(PhraseTree.count_phrase_len(pt),
                         self.TWELVE)

        # haiker = Haiker(
        #     "",
        #     {
        #         "a": ["i", "u"],
        #         "i": [],
        #     }
        # )
        # self.assertNotEqual(
        #     len(haiker.construct_first_five()),
        #     5
        # )

    def test_construct_syllable_initialize_empty(self):
        """
        生成中，単語の候補リストが空担った場合
        """
        WordsData.words_data = self.EMPTY_LIST
        ChainsData.chains_data = self.EMPTY_DICT
        haiker = Haiker()
        root = PhraseTree.define_root(possible_next_words=list(ChainsData.chains_data.keys()))

        with self.assertRaises(ValueError):
            haiker.construct_syllable(root, self.TWELVE)

    def test_construct_syllable_failure(self):
        WordsData.words_data = [
            {
                "word": "あ",
                "vowel": "ア",
                "length": 1,
                "part": "名詞"
            },
            {
                "word": "い",
                "vowel": "イ",
                "length": 1,
                "part": "名詞"
            }
        ]
        ChainsData.chains_data = {"あ": ["い"]}
        haiker = Haiker()
        root = PhraseTree.define_root(possible_next_words=list(ChainsData.chains_data.keys()))
        with self.assertRaises(ValueError):
            haiker.construct_syllable(root, self.TWELVE)

    def test_post_proc(self):
        """
        Phrase クラスが関連するテストは
        Phrase のメンバ変数を初期化してから行う．
        """
        WordsData.words_data = self.SUCCESS_WORDS
        ChainsData.chains_data = self.SUCCESS_CHAINS
        haiker = Haiker()
        word_tuple = (
            Words(
                {
                    "word": "古池",
                    "vowel": "ウウイエ",
                    "length": 4,
                    "part": "名詞"
                }
            ),
            Words(
                {
                    "word": "蛙",
                    "vowel": "アエウ",
                    "length": 3,
                    "part": "名詞"
                }
            ),
            Words(
                {
                    "word": "あ",
                    "vowel": "ア",
                    "length": 1,
                    "part": "名詞"
                }
            )
        )
        root = PhraseTree.define_root(possible_next_words=list(ChainsData.chains_data.keys()))
        second_tree = PhraseTree(current_words=word_tuple,
                                 parent=root)
        root.next_tree = second_tree

        # Phrase 初期状態
        # self.assertEqual(
        #     Phrase.text_list,
        #     list()
        # )
        # self.assertEqual(
        #     Phrase.last_words,
        #     tuple()
        # )
        # self.assertIsInstance(
        #     Phrase.last_vowel,
        #     property
        # )

        # 中間処理
        haiker._post_proc(second_tree)

        # Phrase 代入済み
        self.assertNotEqual(
            Phrase.text_list,
            list()
        )
        self.assertNotEqual(
            Phrase.last_words,
            tuple()
        )
        self.assertIsInstance(
            Phrase.last_vowel,
            str
        )

    def test_get_word(self):
        pass

    def test_get_vowel(self):
        WordsData.words_data = (
            [
                {
                    "word": "あ",
                    "vowel": "ア",
                    "length": 1,
                    "part": "名詞"
                }
            ]
        )
        ChainsData.chains_data = self.SUCCESS_CHAINS
        haiker = Haiker()
        self.assertEqual(
            haiker._get_vowel("あ"),
            "ア"
        )

    def test_is_n_char(self):
        WordsData.words_data = self.EMPTY_LIST
        ChainsData.chains_data = self.EMPTY_DICT
        haiker = Haiker()

        self.assertTrue(
            haiker._is_n_char(5, 5)
        )

        self.assertFalse(
            haiker._is_n_char(5, 7)
        )

    def test_is_less_than_n_char(self):
        WordsData.words_data = self.EMPTY_LIST
        ChainsData.chains_data = self.EMPTY_DICT
        haiker = Haiker()

        self.assertTrue(
            haiker._is_less_than_n_char(5, 3)
        )
        self.assertTrue(
            haiker._is_less_than_n_char(7, 6)
        )

        self.assertFalse(
            haiker._is_less_than_n_char(5, 5)
        )

    # def test_compose(self):
    #     haiker = Haiker(
    #         words=TestHaiker.WORDS,
    #         chains=TestHaiker.CHAINS
    #     )
    #     self.assertTrue(
    #         haiker.compose()
    #     )


if __name__ == '__main__':
    unittest.main()
