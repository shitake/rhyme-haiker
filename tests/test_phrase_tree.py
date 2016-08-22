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
        pt = PhraseTree.define_root()
        pt.next_tree = PhraseTree(current_words=word_tuple)
        self.assertEqual(
            pt.get_text(pt),
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
        next_pt = PhraseTree(next_word_tuple, parent=pt)
        self.assertEqual(
            pt.get_text(next_pt),
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
        pt = PhraseTree.define_root()
        pt.next_tree = PhraseTree(current_words=word_tuple)
        self.assertEqual(
            pt.get_text_list(pt),
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
        next_pt = PhraseTree(next_word_tuple, parent=pt)
        self.assertEqual(
            pt.get_text_list(next_pt),
            ['古池', '蛙', 'あ', 'いい']
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
        pt = PhraseTree.define_root()
        pt.next_tree = PhraseTree(current_words=word_tuple)
        self.assertEqual(
            pt.get_text_vowel(pt),
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
        next_pt = PhraseTree(current_words=next_word_tuple, parent=pt)
        self.assertEqual(
            pt.get_text_vowel(next_pt),
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
            # Words("word": "い",
            #       "vowel": "イ",
            #       "length": 1,
            #       "part": "名詞"),
            # Words("word": "う",
            #       "vowel": "ウ",
            #       "length": 1,
            #       "part": "名詞")
        )
        pt = PhraseTree.define_root()
        pt.next_tree = PhraseTree(current_words=word_tuple)
        self.assertEqual(
            pt.count_phrase_len(pt),
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
            # Words("word": "う",
            #       "vowel": "ウ",
            #       "length": 1,
            #       "part": "名詞")
        )
        next_pt = PhraseTree(next_word_tuple, parent=pt)
        self.assertEqual(
            PhraseTree.count_phrase_len(next_pt),
            10
        )

    # def test_search_dict(self):
    #     words_data = WordsData({ words: })

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
        pt = PhraseTree.define_root()
        next_tree = PhraseTree(current_words=word_tuple)
        pt.next_tree = next_tree
        self.assertEqual(
            pt.get_last_tree(pt),
            next_tree
        )


if __name__ == '__main__':
    unittest.main()
