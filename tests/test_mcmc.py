# -*- coding: utf-8 -*-

from poetry.data_constructor.mcmc import MCMC
import unittest


class TestMCMC(unittest.TestCase):

    def test_create_chains_list(self):
        mcmc = MCMC()

        text = "古池や蛙飛び込む水の音"
        self.assertEqual(
            mcmc.create_chains_list(text),
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

        text = "古池あ古池い古池う蛙あ蛙い"
        self.assertEqual(
            mcmc.create_chains_list(text),
            {
                "古池": ["あ", "い", "う"],
                "蛙": ["あ", "い"],
                "あ": ["古池", "蛙"],
                "い": ["古池"],
                "う": ["蛙"]
            }
        )

    def test_wakatu(self):
        mcmc = MCMC()
        mcmc.read_data = "古池や蛙飛び込む水の音"
        self.assertEqual(
            mcmc._wakatu(),
            [
                "古池",
                "や",
                "蛙",
                "飛び込む",
                "水",
                "の",
                "音"
            ]
        )

    def test_create_next_word_list(self):
        mcmc = MCMC()

        current_word = "古池"
        text_list = [
            "古池", "あ", "古池", "い", "古池", "う",
            "蛙", "あ", "蛙", "あ"
        ]

        self.assertEqual(
            mcmc._create_next_word_list(
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
