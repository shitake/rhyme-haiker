# -*- coding: utf-8 -*-

from poetry.data_constructor.words_data_constructor import WordsDataConstructor
import unittest

import MeCab


class TestWordsDataConstructor(unittest.TestCase):

    def test_construct_parsed_data(self):
        wdc = WordsDataConstructor()

        read_data = "気象庁"
        self.assertEqual(
            wdc._construct_parsed_data(read_data),
            [
                {
                    "word": "気象庁",
                    "part": "名詞",
                    "vowel": "イオーオー",
                    "length": 5
                },
            ]
        )

        read_data = "雨が降る"
        self.assertEqual(
            wdc._construct_parsed_data(read_data),
            [
                {
                    "word": "雨",
                    "part": "名詞",
                    "vowel": "アエ",
                    "length": 2
                },
                {
                    "word": "が",
                    "part": "助詞",
                    "vowel": "ア",
                    "length": 1
                },
                {
                    "word": "降る",
                    "part": "動詞",
                    "vowel": "ウウ",
                    "length": 2
                },
            ]
        )

    def test_extract_data(self):
        import re
        m = MeCab.Tagger()
        mecabed_list = m.parse("さしすせそ").split("\n")[0]
        mecabed_csv_list = [re.sub('\t', ',', mecabed_list).split(',')]
        wdc = WordsDataConstructor()
        self.assertEqual(
            wdc._extract_data(mecabed_csv_list),
            [
                {
                    "word": "さ",
                    "part": "副詞",
                    "vowel": "ア",
                    "length": 1
                }
            ]
        )

    def test_substitute_vowel(self):
        wdc = WordsDataConstructor()
        wdc.yomi = "カキクケコ"
        wdc._substitute_vowel(),
        self.assertEqual(
            wdc.vowel_pronounciation,
            "アイウエオ"
        )
        wdc.yomi = "キショーチョー"
        wdc._substitute_vowel(),
        self.assertEqual(
            wdc.vowel_pronounciation,
            "イオーオー"
        )

    def test_substitute_diphthong(self):
        wdc = WordsDataConstructor()
        wdc.yomi = "キショーチョー"  # 気象庁
        self.assertEqual(
            wdc._substitute_diphthong(),
            "キオーオー"
        )
        wdc.yomi = "ヒャフォウォー"
        self.assertEqual(
            wdc._substitute_diphthong(),
            "アオオー"
        )

    def test_substitute_straight_syllables(self):
        wdc = WordsDataConstructor()
        yomi = "サシスセソ"
        self.assertEqual(
            wdc._substitute_straight_syllables(yomi),
            "アイウエオ"
        )

    def test_completed_substitution(self):
        complete_yomi = "アイウエオ"
        incomplete_yomi = "カイウエオ"

        wdc = WordsDataConstructor()
        wdc.yomi = "アイウエオ"
        self.assertTrue(wdc._completed_substitution(complete_yomi))
        wdc.yomi = "カキクケコ"
        self.assertFalse(wdc._completed_substitution(incomplete_yomi))

if __name__ == '__main__':
    unittest.main()
