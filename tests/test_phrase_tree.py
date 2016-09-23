# -*- coding: utf-8 -*-

import unittest

from poetry.data_constructor.words import Words
from poetry.data_constructor.words_data import WordsData
from poetry.haiker.phrase_tree import PhraseTree


class TestPhraseTree(unittest.TestCase):

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

    def test_get_text(self):
        WordsData(self.WORDS)
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
        root = PhraseTree.define_root(possible_next_words=list(self.SUCCESS_CHAINS.keys()))
        second_tree = PhraseTree(current_words=word_tuple,
                                 parent=root)
        root.next_tree = second_tree
        self.assertEqual(
            PhraseTree.get_text(second_tree),
            '古池蛙あ'
        )

        next_word_tuple = (
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
            ),
            Words(
                {
                    "word": "い",
                    "vowel": "イ",
                    "length": 1,
                    "part": "名詞"
                }
            )
        )
        third_tree = PhraseTree(current_words=next_word_tuple,
                                possible_next_words=list(self.SUCCESS_CHAINS.keys()),
                                parent=second_tree)
        second_tree.next_tree = third_tree
        self.assertEqual(
            PhraseTree.get_text(third_tree),
            '古池蛙あい'
        )

    def test_get_text_list(self):
        WordsData(self.WORDS)
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
        root = PhraseTree.define_root(possible_next_words=list(self.SUCCESS_CHAINS.keys()))
        second_tree = PhraseTree(current_words=word_tuple,
                                 parent=root)
        root.next_tree = second_tree
        self.assertEqual(
            PhraseTree.get_text_list(second_tree),
            ['古池', '蛙', 'あ']
        )

        next_word_tuple = (
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
            ),
            Words(
                {
                    "word": "いい",
                    "vowel": "イイ",
                    "length": 2,
                    "part": "名詞"
                }
            )
        )
        third_tree = PhraseTree(current_words=next_word_tuple,
                                possible_next_words=list(self.SUCCESS_CHAINS.keys()),
                                parent=second_tree)
        second_tree.next_tree = third_tree
        self.assertEqual(
            PhraseTree.get_text_list(third_tree),
            ['古池', '蛙', 'あ', 'いい']
        )

    def test_get_text_list_first_and_last(self):
        """
        最初のツリー(root の次)に対して
        """
        WordsData.words_data = self.SUCCESS_WORDS_TWELVE
        root = PhraseTree.define_root(possible_next_words=list(self.SUCCESS_CHAINS_TWELVE.keys()))
        word_tuple = (
            Words(
                {
                    "word": "ああああ",
                    "vowel": "アアアア",
                    "length": 4,
                    "part": "名詞"
                }
            ),
            Words(
                {
                    "word": "いいいい",
                    "vowel": "イイイイ",
                    "length": 4,
                    "part": "名詞"
                }
            ),
            Words(
                {
                    "word": "うううう",
                    "vowel": "ウウウウ",
                    "length": 4,
                    "part": "名詞"
                }
            )
        )
        next_pt = PhraseTree(current_words=word_tuple,
                             possible_next_words=list(self.SUCCESS_CHAINS_TWELVE.keys()),
                             parent=root)
        root.next_tree = next_pt
        self.assertEqual(
            root.get_text_list(next_pt),
            ['ああああ', 'いいいい', 'うううう']
        )

    def test_get_text_vowel(self):
        WordsData(self.WORDS)
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
        root = PhraseTree.define_root(possible_next_words=list(self.SUCCESS_CHAINS.keys()))
        second_tree = PhraseTree(current_words=word_tuple,
                                 parent=root)
        root.next_tree = second_tree
        self.assertEqual(
            root.get_text_vowel(second_tree),
            'ウウイエアエウア'
        )

        next_word_tuple = (
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
            ),
            Words(
                {
                    "word": "いい",
                    "vowel": "イイ",
                    "length": 2,
                    "part": "名詞"
                }
            )
        )
        third_tree = PhraseTree(current_words=next_word_tuple,
                                possible_next_words=list(self.SUCCESS_CHAINS.keys()),
                                parent=second_tree)
        second_tree.next_tree = third_tree
        self.assertEqual(
            root.get_text_vowel(third_tree),
            'ウウイエアエウアイイ'
        )

    def test_count_phrase_len(self):
        WordsData(self.WORDS)
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
        root = PhraseTree.define_root(possible_next_words=list(self.SUCCESS_CHAINS.keys()))
        second_tree = PhraseTree(current_words=word_tuple,
                                 parent=root)
        root.next_tree = second_tree
        self.assertEqual(
            root.count_phrase_len(second_tree),
            8
        )

        next_word_tuple = (
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
            ),
            Words(
                {
                    "word": "いい",
                    "vowel": "イイ",
                    "length": 2,
                    "part": "名詞"
                }
            )
        )
        third_tree = PhraseTree(next_word_tuple,
                                parent=second_tree)
        self.assertEqual(
            PhraseTree.count_phrase_len(third_tree),
            10
        )

    def test_get_last_words(self):
        WordsData(self.WORDS)
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
        pt = PhraseTree(word_tuple)

        next_word_tuple = (
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
            ),
            Words(
                {
                    "word": "い",
                    "vowel": "イ",
                    "length": 1,
                    "part": "名詞"
                }
            )
        )
        next_pt = PhraseTree(next_word_tuple, parent=pt)
        pt.next_tree = next_pt

        self.assertEqual(
            PhraseTree.get_last_words(pt),
            next_word_tuple
        )

    def test_get_last_tree(self):
        WordsData(self.WORDS)
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
        root = PhraseTree.define_root(possible_next_words=list(self.SUCCESS_CHAINS.keys()))
        next_tree = PhraseTree(current_words=word_tuple)
        root.next_tree = next_tree
        self.assertEqual(
            root.get_last_tree(root),
            next_tree
        )


if __name__ == '__main__':
    unittest.main()
