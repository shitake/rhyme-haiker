# -*- coding: utf-8 -*-

from poetry.haiker.haiker import Haiker
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
if __name__ == '__main__':
    unittest.main()
