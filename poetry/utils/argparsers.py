# -*- coding: utf-8 -*-

import argparse
from logging import getLogger
from logging import StreamHandler
from logging import DEBUG

import poetry
from poetry.data_constructor.chains_data import ChainsData
from poetry.data_constructor.chains_data_constructor import ChainsDataConstructor
from poetry.data_constructor.words_data import WordsData
from poetry.data_constructor.words_data_constructor import WordsDataConstructor
from poetry.haiker.haiker import Haiker
from poetry.utils.data_reader import DataReader
from poetry.utils.data_exporter import DataExporter


logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)

OUTPUT_DIR = poetry.__path__[0] + '/../output/'
WORDS_FILE_NAME = 'words.pickle'
CHAINS_FILE_NAME = 'chains.pickle'


def cmd_prep(args):
    logger.info("Preprocessing")
    logger.info("Loading <- {0}".format(args.filename))

    read_data = DataReader.read_file(args.filename)

    cdc = ChainsDataConstructor()
    chains_data = cdc.construct_data(read_data)

    wdc = WordsDataConstructor()
    words_data = wdc.construct_data(read_data)

    de = DataExporter(chains_data=chains_data,
                      words_data=words_data)
    de.export_pickle()

    logger.info("Exported")


def cmd_compose(args):
    logger.info("Compose")

    WordsData.words_data = DataReader.read_pickled_file(OUTPUT_DIR + WORDS_FILE_NAME)
    ChainsData.chains_data = DataReader.read_pickled_file(OUTPUT_DIR + CHAINS_FILE_NAME)

    haiker = Haiker()
    haiku = haiker.compose()

    logger.info(haiku)


def main():
    parser = argparse.ArgumentParser(description='Haiku composer.')

    subparsers = parser.add_subparsers()

    # データ作成
    prep_parser = subparsers.add_parser('prep',
                                        help='Preprocessing for corpus.')
    prep_parser.add_argument('filename',
                             type=str,
                             help='Corpus file name.')
    prep_parser.set_defaults(func=cmd_prep)

    # 詠む
    compose_parser = subparsers.add_parser('compose',
                                           help='Compose rhyming haiku.')
    compose_parser.set_defaults(func=cmd_compose)

    args = parser.parse_args()

    try:
        # args.db = db
        if hasattr(args, 'func'):
            args.func(args)
        else:
            parser.print_help()
    finally:
        # db.close()
        pass


if __name__ == '__main__':
    main()
