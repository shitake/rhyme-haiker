# -*- coding: utf-8 -*-

from poetry.haiker.haiker import Haiker
from poetry.haiker.haiker import ConstructionError
import unittest


class TestHaiker(unittest.TestCase):

    def test_construct_first_five(self):
        haiker = Haiker(
            "",
            {
                "古池": ["あ", "い", "う"],
                "蛙": ["あ", "い"],
                "あ": ["古池", "蛙"],
                "い": ["古池"],
                "う": ["蛙"]
            }
        )
        self.assertIsInstance(
            haiker.construct_first_five(),
            str
        )
        self.assertEqual(
            len(haiker.construct_first_five()),
            5
        )

        # haiker = Haiker(
        #     "",
        #     {
        #         "a": ["i", "u"],
        #         "i": [],
        #     }
        # )
        # self.assertNotEqual(
        #     len(haiker.construct_first_five()),
        #     5
        # )

        haiker = Haiker(
            "",
            {}
        )
        self.assertEqual(
            haiker.construct_first_five(),
            None
        )

        haiker = Haiker(
            "",
            {
                "a": ["i"]
            }
        )
        self.assertEqual(
            haiker.construct_first_five(),
            None
        )

    def test_is_n_char(self):
        haiker = Haiker("", {})

        self.assertTrue(
            haiker._is_n_char(5, "aiueo")
        )
        self.assertTrue(
            haiker._is_n_char(5, "フルイケヤ")
        )
        self.assertTrue(
            haiker._is_n_char(7, "カワズトビコム")
        )

        self.assertFalse(
            haiker._is_n_char(5, "カワズトビコム")
        )

    def test_is_less_than_n_char(self):
        haiker = Haiker("", {})

        self.assertTrue(
            haiker._is_less_than_n_char(5, "aiue")
        )
        self.assertTrue(
            haiker._is_less_than_n_char(5, "フルイケ")
        )
        self.assertTrue(
            haiker._is_less_than_n_char(7, "カワズトビコ")
        )

        self.assertFalse(
            haiker._is_less_than_n_char(5, "フルイケヤ")
        )

    def test_construct_seven(self):
        haiker = Haiker(
            "",
            {
                "古池": ["あ", "い", "う"],
                "蛙": ["あ", "い"],
                "あ": ["古池", "蛙"],
                "い": ["古池"],
                "う": ["蛙"]
            }
        )
        haiker.construct_first_five()
        self.assertEqual(
            len(haiker.construct_seven()),
            7
        )

        # 最初の5字の最後の単語が登録されていない場合，例外を返すことを確認
        haiker = Haiker(
            "",
            {}
        )
        haiker.construct_first_five()
        with self.assertRaises(ConstructionError):
            haiker.construct_seven()

    def test_construct_last_five(self):
        haiker = Haiker(
            "",
            {
                "古池": ["あ", "い", "う"],
                "蛙": ["あ", "い"],
                "あ": ["古池", "蛙"],
                "い": ["古池"],
                "う": ["蛙"]
            }
        )
        haiker.construct_first_five()
        haiker.construct_seven()
        self.assertEqual(
            len(haiker.construct_last_five()),
            5
        )

        # 7字の最後の単語が登録されていない場合，例外を返すことを確認
        haiker = Haiker(
            "",
            {
                "あ": ["い"],
                "い": ["あ"]
            }
        )
        haiker.construct_first_five()
        haiker.construct_seven()
        haiker.last_word_of_seven = ""
        with self.assertRaises(ConstructionError):
            haiker.construct_last_five()

    def test_compose(self):
        haiker = Haiker(
            "",
            {
                "古池": ["あ", "い", "う"],
                "蛙": ["あ", "い"],
                "あ": ["古池", "蛙"],
                "い": ["古池"],
                "う": ["蛙"]
            }
        )
        self.assertTrue(
            haiker.compose()
        )


if __name__ == '__main__':
    unittest.main()
