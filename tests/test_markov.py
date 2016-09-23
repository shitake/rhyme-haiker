# -*- coding: utf-8 -*-

from poetry.utils.markov import Markov
import unittest


class TestMarkov(unittest.TestCase):

    def test_build_model(self):
        m = Markov()
        n = 3

        tokens = ["古池", "あ", "古池", "い", "古池", "う", "蛙", "あ", "蛙", "い"]
        self.assertEqual(
            m.build_model(tokens, n),
            {
                ("古池", "あ", "古池"): [
                    "い"
                ],
                ("あ", "古池", "い"): [
                    "古池"
                ],
                ("古池", "い", "古池"): [
                    "う"
                ],
                ("い", "古池", "う"): [
                    "蛙"
                ],
                ("古池", "う", "蛙"): [
                    "あ"
                ],
                ("う", "蛙", "あ"): [
                    "蛙"
                ],
                ("蛙", "あ", "蛙"): [
                    "い"
                ],
                ("あ", "蛙", "い"): [
                    None
                ]
            }
        )

        tokens = ["あ", "い", "あ", "い", "あ"]
        self.assertEqual(
            m.build_model(tokens, n),
            {
                ("あ", "い", "あ"): [
                    "い",
                    None
                ],
                ("い", "あ", "い"): [
                    "あ"
                ]
            }
        )


if __name__ == '__main__':
    unittest.main()
