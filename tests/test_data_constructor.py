# -*- coding: utf-8 -*-

from poetry.data_constructor.data_constructor import DataConstructor
import unittest


class TestDataConstructor(unittest.TestCase):

    # def test_construct_parsed_data(self):
    #     dc = DataConstructor()

    #     read_data = "気象庁"
    #     self.assertEqual(
    #         dc._construct_parsed_data(read_data),
    #         [
    #             {
    #                 "word": "気象庁",
    #                 "part": "名詞",
    #                 "vowel": "イオーオー",
    #                 "length": 5
    #             },
    #         ]
    #     )

    #     read_data = "雨が降る"
    #     self.assertEqual(
    #         dc._construct_parsed_data(read_data),
    #         [
    #             {
    #                 "word": "雨",
    #                 "part": "名詞",
    #                 "vowel": "アエ",
    #                 "length": 2
    #             },
    #             {
    #                 "word": "が",
    #                 "part": "助詞",
    #                 "vowel": "ア",
    #                 "length": 1
    #             },
    #             {
    #                 "word": "降る",
    #                 "part": "動詞",
    #                 "vowel": "ウウ",
    #                 "length": 2
    #             },
    #         ]
    #     )

    def test_delimit(self):
        parsed_text = "明日\t名詞,副詞可能,*,*,*,*,明日,アシタ,アシタ\nは\t助詞,係助詞,*,*,*,*,は,ハ,ワ\n雨\t名詞,一般,*,*,*,*,雨,アメ,アメ\nが\t助詞,格助詞,一般,*,*,*,が,ガ,ガ\n降る\t動詞,自立,*,*,五段・ラ行,基本形,降る,フル,フル\nEOS\n"
        dc = DataConstructor()
        self.assertEqual(
            dc._delimit(parsed_text),
            [
                "明日\t名詞,副詞可能,*,*,*,*,明日,アシタ,アシタ",
                "は\t助詞,係助詞,*,*,*,*,は,ハ,ワ",
                "雨\t名詞,一般,*,*,*,*,雨,アメ,アメ",
                "が\t助詞,格助詞,一般,*,*,*,が,ガ,ガ",
                "降る\t動詞,自立,*,*,五段・ラ行,基本形,降る,フル,フル",
                "EOS",
                ""
            ]
        )

    def test_splited_word_data_to_csv_list(self):
        dc = DataConstructor()
        parsed_data = "気象庁\t名詞,固有名詞,組織,*,*,*,気象庁,キショウチョウ,キショーチョー"
        self.assertEqual(
            dc._splited_word_data_to_csv_list(parsed_data),
            [
                "気象庁", "名詞", "固有名詞", "組織", "*",
                "*", "*", "気象庁", "キショウチョウ", "キショーチョー"
            ]
        )

        parsed_data = ""
        self.assertEqual(
            dc._splited_word_data_to_csv_list(parsed_data),
            [""]
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
        dc = DataConstructor()
        self.assertEqual(
            dc._sanitize_data_list(csv_list),
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
        dc = DataConstructor()
        self.assertTrue(dc._can_read(
            [
                "雨", "名詞", "一般", "*", "*", "*", "*", "雨", "アメ", "アメ"
            ]
        ))
        self.assertFalse(dc._can_read(
            [
                "-", "名詞", "サ変接続", "*", "*", "*", "*", "*"
            ]
        ))
        self.assertFalse(dc._can_read(
            [
                "、", "記号", "読点", "*", "*", "*", "*", "、", "、", "、"
            ]
        ))
        self.assertFalse(dc._can_read(
            [
                "．", "記号", "句点", "*", "*", "*", "*", "．", "．", "．"
            ]
        ))
        self.assertFalse(dc._can_read(
            [
                "　", "記号", "空白", "*", "*", "*", "*", "　", "　", "　"
            ]
        ))

if __name__ == '__main__':
    unittest.main()
