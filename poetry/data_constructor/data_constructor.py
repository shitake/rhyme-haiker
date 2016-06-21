# -*- coding: utf-8 -*-

from logging import getLogger
from logging import StreamHandler
from logging import DEBUG
import MeCab
import re

logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)


class DataConstructor:

    WORD = 0
    PART = 1
    PART_SUBTYPE = 2
    PRONOUNCIATION = 9

    def __init__(self):
        self.read_data = ""  # TODO: _read_text() を削除してここの初期化も削除
        self.yomi = ""
        self.vowel_pronounciation = ""

    def construct_table_data(self):
        """
        インターフェイス
        テーブル挿入用データを作成する．
        """
        # TODO: インターフェイス修正
        #       分かち書き後の単語1つを入力データとして受け取る
        #       方がよさそう
        self._read_text()
        return self._construct_mecabed_data()  # TODO: 修正対象

    # TODO: poetry/utils/text_reader.py に組み込む
    def _read_text(self):
        """
        学習用データ読み込み
        """
        with open("/Users/pokesu/Downloads/corpus/test.txt") as f:
            self.read_data = f.read()

    def _construct_mecabed_data(self):
        """
        Mecab で解析後のデータを返す
        """
        m = MeCab.Tagger()

        mecabed_list = m.parse(self.read_data).split("\n")
        csv_list = [self._splited_word_data_to_csv_list(line) for line in mecabed_list]
        sanitized_data_list = self._sanitize_data_list(csv_list)

        return [self._extract_data(line) for line in sanitized_data_list]

    def _splited_word_data_to_csv_list(self, splited_word_data):
        """
        分かち書き後のデータリストを csv のリストへ変換．
        """
        if not isinstance(splited_word_data, str):
            logger.warning("Input value is not String: %s." % splited_word_data)

        csv_text = re.sub('\t', ',', splited_word_data)
        return csv_text.split(',')

    def _sanitize_data_list(self, csv_list):
        """
        csv のリストから不要なデータを除外．
        除外対象
        - 辞書に 読み が登録されていない項目
        - 重複項目
        """
        if not isinstance(csv_list, list):
            logger.warning("Input value is not List: %s." % csv_list)

        sanitized_data_list = []
        unique_word_list = []
        for csv_data in csv_list:
            if not self._can_read(csv_data):
                logger.warning("Unreadable: %s." % csv_data[self.WORD])
            elif csv_data[self.WORD] in unique_word_list:
                logger.warning("Duplicated: %s." % csv_data[self.WORD])
            else:
                sanitized_data_list.append(csv_data)
                unique_word_list.append(csv_data[self.WORD])
        return sanitized_data_list

    def _can_read(self, csv_data):
        """
        辞書に 読み が登録されている場合，True を返す．
        特殊な音(フォ，ウォ など)は登録されている場合といない場合とがあるので注意．
        """
        if not isinstance(csv_data, list):
            logger.warning("Input value is not List: %s." % csv_data)

        logger.debug("--------------------------------------")
        logger.debug(csv_data)
        if len(csv_data) <= self.PRONOUNCIATION:
            return False
        elif csv_data[self.PART] == u'記号':
            return False
        elif csv_data[self.PART] is '名詞' and csv_data[self.PART_SUBTYPE is 'サ変接続']:
            print("aaaaaaaaaaaaaaaaaaaaaaaa")
            return False
        else:
            return True

    def _extract_data(self, csv_data):
        """
        単語，品詞，読みの母音，読みの字数の辞書を返す
        """
        if not isinstance(csv_data, list):
            logger.warning("Input value is not List: %s." % csv_data)

        self.yomi = csv_data[self.PRONOUNCIATION]
        self._substitute_vowel()

        # print(csv_data[self.WORD],
        #       csv_data[self.PART],
        #       self._substitute_vowel(csv_data[self.PRONOUNCIATION]),
        #       len(csv_data[self.PRONOUNCIATION]))
        return {
            "word": csv_data[self.WORD],
            "part": csv_data[self.PART],
            "vowel": self.vowel_pronounciation,
            "length": len(self.vowel_pronounciation)
        }

    def _substitute_vowel(self):
        """
        読み の子音を母音に置換する
        """
        # 拗音をリストの先頭にする
        try:
            substituted_yomi = self._substitute_diphthong()
            self.vowel_pronounciation = self._substitute_straight_syllables(substituted_yomi)
        except SubstitutionError as e:
            print('Substitution was incompleted.', e.origin, e.value)

    def _substitute_diphthong(self):
        """
        拗音を母音に置換する．
        拗音と定義されていない特殊な音も置換．
        ローマ字変換を参考．
        """
        a = 'ア'
        i = 'イ'
        u = 'ウ'
        e = 'エ'
        o = 'オ'
        a_diphthong = (
            'キャ', 'シャ', 'チャ', 'ニャ', 'ヒャ', 'ミャ', 'リャ', 'ギャ', 'ジャ', 'ヂャ', 'ビャ', 'ピャ',
            'クァ', 'クヮ', 'グヮ',                         'ツァ', 'テャ', 'デャ', 'ファ', 'フャ', 'ブャ', 'ウァ', 'ヴァ', 'ブァ'
        )
        i_diphthong = (
            'クィ',         'グィ', 'ジィ', 'チィ', 'ヂィ', 'ツィ', 'ティ', 'ディ', 'フィ',                 'ウィ', 'ヴィ', 'ブィ'
        )
        u_diphthong = (
            'キュ', 'シュ', 'チュ', 'ニュ', 'ヒュ', 'ミュ', 'リュ', 'ギュ', 'ジュ', 'ヂュ', 'ビュ', 'ピュ',
            'クゥ',         'グゥ',                                 'テュ', 'デュ',         'フュ', 'ブュ'
        )
        e_diphthong = (
            'クェ', 'グェ', 'シェ', 'ジェ', 'チェ', 'ヂェ', 'ツェ', 'テェ', 'デェ', 'フェ',                 'ウェ', 'ヴェ', 'ブェ'
        )
        o_diphthong = (
            'キョ', 'ショ', 'チョ', 'ニョ', 'ヒョ', 'ミョ', 'リョ', 'ギョ', 'ジョ', 'ヂョ', 'ビョ', 'ピョ',
            'クォ',         'グォ',                         'ツォ', 'テョ', 'デョ', 'フォ', 'フョ', 'ブョ', 'ウォ', 'ヴォ', 'ブォ'
        )
        vowel_dict = {
            a: a_diphthong,
            i: i_diphthong,
            u: u_diphthong,
            e: e_diphthong,
            o: o_diphthong
        }

        substituted_yomi = self.yomi

        for vowel, consonants in vowel_dict.items():
            for c in consonants:
                substituted_yomi = re.sub(c, vowel, substituted_yomi)
        return substituted_yomi

    def _substitute_straight_syllables(self, yomi):
        """
        直音を母音に置換する．
        """
        a = 'ア'
        i = 'イ'
        u = 'ウ'
        e = 'エ'
        o = 'オ'
        a_consonants = ('カ', 'サ', 'タ', 'ナ', 'ハ', 'マ', 'ヤ', 'ラ', 'ワ', 'ガ', 'ザ', 'ダ', 'バ', 'パ', "ャ")
        i_consonants = ('キ', 'シ', 'チ', 'ニ', 'ヒ', 'ミ',       'リ',       'ギ', 'ジ', 'ヂ', 'ビ', 'ピ')
        u_consonants = ('ク', 'ス', 'ツ', 'ヌ', 'フ', 'ム', 'ユ', 'ル',       'グ', 'ズ', 'ヅ', 'ブ', 'プ', "ュ")
        e_consonants = ('ケ', 'セ', 'テ', 'ネ', 'ヘ', 'メ',       'レ',       'ゲ', 'ゼ', 'デ', 'ベ', 'ペ')
        o_consonants = ('コ', 'ソ', 'ト', 'ノ', 'ホ', 'モ', 'ヨ', 'ロ', 'ヲ', 'ゴ', 'ゾ', 'ド', 'ボ', 'ポ', "ョ")
        vowel_dict = {
            a: a_consonants,
            i: i_consonants,
            u: u_consonants,
            e: e_consonants,
            o: o_consonants
        }

        substituted_yomi = yomi

        for vowel, consonants in vowel_dict.items():
            for c in consonants:
                substituted_yomi = re.sub(c, vowel, substituted_yomi)

                if self._completed_substitution(substituted_yomi):
                    return substituted_yomi

        # 置換完了しなかった場合
        raise SubstitutionError(yomi, substituted_yomi)

    def _completed_substitution(self, current_yomi):
        """
        拗音が全て置換済みであることが前提条件．
        母音と子音の置換が終わった場合 True を返す
        """
        if not isinstance(current_yomi, str):
            logger.warning("Input value is not String: %s." % current_yomi)

        # 可換な文字リスト
        substitutable_list = (
            'カ', 'サ', 'タ', 'ナ', 'ハ', 'マ', 'ヤ', 'ラ', 'ワ', 'ガ', 'ザ', 'ダ', 'バ', 'パ', "ャ",
            'キ', 'シ', 'チ', 'ニ', 'ヒ', 'ミ',       'リ',       'ギ', 'ジ', 'ヂ', 'ビ', 'ピ',
            'ク', 'ス', 'ツ', 'ヌ', 'フ', 'ム', 'ユ', 'ル',       'グ', 'ズ', 'ヅ', 'ブ', 'プ', "ュ",
            'ケ', 'セ', 'テ', 'ネ', 'ヘ', 'メ',       'レ',       'ゲ', 'ゼ', 'デ', 'ベ', 'ペ',
            'コ', 'ソ', 'ト', 'ノ', 'ホ', 'モ', 'ヨ', 'ロ', 'ヲ', 'ゴ', 'ゾ', 'ド', 'ボ', 'ポ', "ョ"
        )

        origin_yomi = current_yomi

        for o, c in zip(origin_yomi, current_yomi):
            if o not in substitutable_list:
                continue
            if o == c:
                return False
        return True

    def generate_first5(self):
        """
        最初の5文字のデータを作成
        """

    def generate_center7(self):
        """
        真ん中の7文字のデータを作成
        """

    def generate_last5(self):
        """
        最後の5文字のデータを作成
        """


class SubstitutionError(Exception):

    def __init__(self, origin, value):
        self.origin = origin
        self.value = value

    def __str__(self):
        return repr(self.origin, self.value)


if __name__ == '__main__':
    dc = DataConstructor()
    mecabed = dc.construct_table_data()
    print(repr(mecabed))
