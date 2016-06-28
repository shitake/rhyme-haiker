# -*- coding: utf-8 -*-

from poetry.data_constructor.chains_data_constructor import ChainsDataConstructor
import unittest


class TestChainsDataConstructor(unittest.TestCase):

    def test_construct_chains_dict(self):
        cdc = ChainsDataConstructor()

        text_list = ["古池", "や", "蛙", "飛び込む", "水", "の", "音"]
        self.assertEqual(
            cdc._construct_chains_dict(text_list),
            {
                "古池": ["や"],
                "や": ["蛙"],
                "蛙": ["飛び込む"],
                "飛び込む": ["水"],
                "水": ["の"],
                "の": ["音"],
                "音": []
            }
        )

        text_list = ["古池", "あ", "古池", "い", "古池", "う", "蛙", "あ", "蛙", "い"]
        self.assertEqual(
            cdc._construct_chains_dict(text_list),
            {
                "古池": ["あ", "い", "う"],
                "蛙": ["あ", "い"],
                "あ": ["古池", "蛙"],
                "い": ["古池"],
                "う": ["蛙"]
            }
        )

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

    def test_create_next_word_list(self):
        cdc = ChainsDataConstructor()

        current_word = "古池"
        text_list = [
            "古池", "あ", "古池", "い", "古池", "う",
            "蛙", "あ", "蛙", "あ"
        ]

        self.assertEqual(
            cdc._create_next_word_list(
                current_word,
                text_list
            ),
            [
                "あ",
                "い",
                "う"
            ]
        )


if __name__ == '__main__':
    unittest.main()
