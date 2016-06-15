# -*- coding: utf-8 -*-

from poetry.data_constructor.data_constructor import DataConstructor
import unittest

import MeCab


class TestDataConstructor(unittest.TestCase):

    def test_construct_mecabed_data(self):
        tc = DataConstructor()

        tc.read_data = "気象庁"
        self.assertEqual(
            tc._construct_mecabed_data(),
            [
                {
                    "word": "気象庁",
                    "part": "名詞",
                    "vowel": "イオーオー",
                    "length": 5
                },
            ]
        )

        tc.read_data = "雨が降る"
        self.assertEqual(
            tc._construct_mecabed_data(),
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

    def test_splited_word_data_to_csv_list(self):
        mecabed_data = "気象庁\t名詞,固有名詞,組織,*,*,*,気象庁,キショウチョウ,キショーチョー"
        tc = DataConstructor()
        self.assertEqual(
            tc._splited_word_data_to_csv_list(mecabed_data),
            [
                "気象庁", "名詞", "固有名詞", "組織", "*",
                "*", "*", "気象庁", "キショウチョウ", "キショーチョー"
            ]
        )

    def test_sanitize_data_list(self):
        csv_list = [
            [
                "気象庁", "名詞", "固有名詞", "組織", "*",
                "*", "*", "気象庁", "キショウチョウ", "キショーチョー"
            ],
            [
                "雨", "名詞", "一般", "*", "*", "*", "*", "雨", "アメ", "アメ"
            ],
            [
                "-", "名詞", "サ変接続", "*", "*", "*", "*", "*"
            ]
        ]
        tc = DataConstructor()
        self.assertEqual(
            tc._sanitize_data_list(csv_list),
            [
                [
                    "気象庁", "名詞", "固有名詞", "組織", "*",
                    "*", "*", "気象庁", "キショウチョウ", "キショーチョー"
                ],
                [
                    "雨", "名詞", "一般", "*", "*", "*", "*", "雨", "アメ", "アメ"
                ],
            ]
        )

    def test_can_read(self):
        tc = DataConstructor()
        self.assertTrue(tc._can_read(
            [
                "雨", "名詞", "一般", "*", "*", "*", "*", "雨", "アメ", "アメ"
            ]
        ))
        self.assertFalse(tc._can_read(
            [
                "-", "名詞", "サ変接続", "*", "*", "*", "*", "*"
            ]
        ))
        self.assertFalse(tc._can_read(
            [
                "、", "記号", "読点", "*", "*", "*", "*", "、", "、", "、"
            ]
        ))
        self.assertFalse(tc._can_read(
            [
                "．", "記号", "句点", "*", "*", "*", "*", "．", "．", "．"
            ]
        ))
        self.assertFalse(tc._can_read(
            [
                "　", "記号", "空白", "*", "*", "*", "*", "　", "　", "　"
            ]
        ))

    def test_extract_data(self):
        import re
        m = MeCab.Tagger()
        mecabed_list = m.parse("さしすせそ").split("\n")[0]
        mecabed_csv = re.sub('\t', ',', mecabed_list).split(',')
        tc = DataConstructor()
        self.assertEqual(
            tc._extract_data(mecabed_csv),
            {
                "word": "さ",
                "part": "副詞",
                "vowel": "ア",
                "length": 1
            }
        )

    def test_substitute_vowel(self):
        tc = DataConstructor()
        tc.yomi = "カキクケコ"
        tc._substitute_vowel(),
        self.assertEqual(
            tc.vowel_pronounciation,
            "アイウエオ"
        )
        tc.yomi = "キショーチョー"
        tc._substitute_vowel(),
        self.assertEqual(
            tc.vowel_pronounciation,
            "イオーオー"
        )

    def test_substitute_diphthong(self):
        tc = DataConstructor()
        tc.yomi = "キショーチョー"  # 気象庁
        self.assertEqual(
            tc._substitute_diphthong(),
            "キオーオー"
        )
        tc.yomi = "ヒャフォウォー"
        self.assertEqual(
            tc._substitute_diphthong(),
            "アオオー"
        )

    def test_substitute_straight_syllables(self):
        tc = DataConstructor()
        yomi = "サシスセソ"
        self.assertEqual(
            tc._substitute_straight_syllables(yomi),
            "アイウエオ"
        )

    def test_completed_substitution(self):
        complete_yomi = "アイウエオ"
        incomplete_yomi = "カイウエオ"

        tc = DataConstructor()
        tc.yomi = "アイウエオ"
        self.assertTrue(tc._completed_substitution(complete_yomi))
        tc.yomi = "カキクケコ"
        self.assertFalse(tc._completed_substitution(incomplete_yomi))

if __name__ == '__main__':
    unittest.main()
