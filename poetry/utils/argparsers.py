# -*- coding: utf-8 -*-

import argparse
from corpus_reader import CorpusReader
import logging
# from poetry.data_constructor.chains_data_constructor import ChainsDataConstructor
# from poetry.data_constructor.words_data_constructor import WordsDataConstructor


logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())


def cmd_prep(args):
    logger.info("Preprocessing")
    logger.info("Loading -> {0}".format(args.filename))

    cr = CorpusReader()
    read_data = cr.read_file(args.filename)
    print(read_data)


def cmd_compose(args):
    logger.info("compose")
    pass


def main():
    parser = argparse.ArgumentParser(
        description='Haiku composer.'
    )

    parser.add_argument(
        'filename'
    )

    subparsers = parser.add_subparsers()

    # データ作成
    prep_parser = subparsers.add_parser('prep')
    prep_parser.set_defaults(func=cmd_prep)

    # 詠む
    compose_parser = subparsers.add_parser('compose')
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
    # TODO: ファイル名再考，これをコマンドの中心とした名前にする(haiku とか)
