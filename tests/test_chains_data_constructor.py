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


if __name__ == '__main__':
    unittest.main()
