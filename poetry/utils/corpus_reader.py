# -*- coding: utf-8 -*-

import argparse
import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())


class CorpusReader:

    def read_file(self, addr):
        """
        学習用データ読み込み
        """
        # with open("/Users/pokesu/Downloads/corpus/test.txt") as f:
        with open(addr) as f:
            # self.read_data = f.read()
            return f.read()

    def main(self):
        parser = argparse.ArgumentParser(description='Input some text file.')
        parser.add_argument(
            'text',
            metavar='T',
            type=str,
            help='Japanese text for data construction'
        )
        parser.add_argument(
            dest='read',

        )

        args = parser.parse_args()
        print(args.a)
