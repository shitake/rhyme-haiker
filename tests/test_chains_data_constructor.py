# -*- coding: utf-8 -*-

from poetry.data_constructor.chains_data_constructor import ChainsDataConstructor
import unittest


class TestChainsDataConstructor(unittest.TestCase):

    def test_extract_data(self):
        cdc = ChainsDataConstructor()

        csv_data_list = [
            ["古池", "名詞", "固有名詞", "地域", "一般", "*", "*", "古池", "フルイケ", "フルイケ"],
            ["や", "助詞", "並立助詞", "*", "*", "*", "*", "や", "ヤ", "ヤ"],
            ["蛙", "名詞", "一般", "*", "*", "*", "*", "蛙", "カエル", "カエル"],
            ["飛び込む", "動詞", "自立", "*", "*", "五段・マ行", "基本形", "飛び込む", "トビコム", "トビコム"],
            ["水", "名詞", "一般", "*", "*", "*", "*", "水", "ミズ", "ミズ"],
            ["の", "助詞", "連体化", "*", "*", "*", "*", "の", "ノ", "ノ"],
            ["音", "名詞", "一般", "*", "*", "*", "*", "音", "オト", "オト"]
        ]
        self.assertEqual(
            cdc._extract_data(csv_data_list),
            {
                ("古池", "や", "蛙"): [
                    "飛び込む"
                ],
                ("や", "蛙", "飛び込む"): [
                    "水"
                ],
                ("蛙", "飛び込む", "水"): [
                    "の"
                ],
                ("飛び込む", "水", "の"): [
                    "音"
                ],
                ("水", "の", "音"): [
                    None
                ],
            }
        )

        # TODO: リストの大きさが3未満の場合

    # def test_construct_chains_dict(self):
    #     cdc = ChainsDataConstructor()

    #     text_list = ["古池", "や", "蛙", "飛び込む", "水", "の", "音"]
    #     self.assertEqual(
    #         cdc._construct_chains_dict(text_list),
    #         {
    #             "古池": ["や"],
    #             "や": ["蛙"],
    #             "蛙": ["飛び込む"],
    #             "飛び込む": ["水"],
    #             "水": ["の"],
    #             "の": ["音"],
    #             "音": []
    #         }
    #     )

    #     text_list = ["古池", "あ", "古池", "い", "古池", "う", "蛙", "あ", "蛙", "い"]
    #     self.assertEqual(
    #         cdc._construct_chains_dict(text_list),
    #         {
    #             "古池": ["あ", "い", "う"],
    #             "蛙": ["あ", "い"],
    #             "あ": ["古池", "蛙"],
    #             "い": ["古池"],
    #             "う": ["蛙"]
    #         }
    #     )

    # def test_wakatu(self):
    #     cdc = ChainsDataConstructor()
    #     read_data = "古池や蛙飛び込む水の音"
    #     self.assertEqual(
    #         cdc._wakatu(),
    #         [
    #             "古池",
    #             "や",
    #             "蛙",
    #             "飛び込む",
    #             "水",
    #             "の",
    #             "音"
    #         ]
    #     )

    # def test_create_next_word_list(self):
    #     cdc = ChainsDataConstructor()

    #     current_word = "古池"
    #     text_list = [
    #         "古池", "あ", "古池", "い", "古池", "う",
    #         "蛙", "あ", "蛙", "あ"
    #     ]

    #     self.assertEqual(
    #         cdc._create_next_word_list(
    #             current_word,
    #             text_list
    #         ),
    #         [
    #             "あ",
    #             "い",
    #             "う"
    #         ]
    #     )


if __name__ == '__main__':
    unittest.main()
