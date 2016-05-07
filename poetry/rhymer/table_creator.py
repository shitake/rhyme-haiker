# -*- coding: utf-8 -*-

import re
import MeCab


class TableCreator:

    WORD = 0
    PART = 1
    PRONOUNCIATION = 9

    def read_text(self):
        """
        学習用データ読み込み
        """
        f = open("/Users/pokesu/Downloads/corpus/test.txt")
        return f.read()

    def construct_mecabed_data(self, data):
        """
        Mecab で解析後のデータを返す
        """
        m = MeCab.Tagger()
        mecabed_list = m.parse(data).split("\n")
        return [self._extract_data(line) for line in mecabed_list]

    def _extract_data(self, data):
        """
        単語，品詞，読みの母音，読みの字数のタプルを返す
        """
        csv_text = re.sub('\t', ',', data)
        csv_list = csv_text.split(',')

        if not self._can_read(csv_list):
            print("Unreadable", csv_list)
            return

        # print(csv_list[self.WORD],
        #       csv_list[self.PART],
        #       self._substitute_vowel(csv_list[self.PRONOUNCIATION]),
        #       len(csv_list[self.PRONOUNCIATION]))
        return (csv_list[self.WORD],
                csv_list[self.PART],
                self._substitute_vowel(csv_list[self.PRONOUNCIATION]),
                len(csv_list[self.PRONOUNCIATION]))

    def _can_read(self, csv_list):
        """
        辞書に 読み が登録されている場合，True を返す
        """
        if len(csv_list) <= self.PRONOUNCIATION:
            return False
        else:
            return True

    def _substitute_vowel(self, yomi):
        """
        読み の子音を母音に置換する
        """
        # 拗音をリストの先頭にする
        try:
            substituted_yomi = self._substitute_diphthong(yomi)
            substituted_yomi = self._substitute_straight_syllables(substituted_yomi)
            return substituted_yomi
        except SubstitutionError as e:
            print('Substitution was incompleted.', e.origin, e.value)

    def _substitute_diphthong(self, yomi):
        """
        開拗音を母音に置換する．
        合拗音は無視．
        """
        a = 'ア'
        u = 'ウ'
        o = 'オ'
        a_diphthong = ('キャ', 'シャ', 'チャ', 'ニャ', 'ヒャ', 'ミャ', 'リャ', 'ギャ', 'ジャ', 'ヂャ', 'ビャ', 'ピャ')
        u_diphthong = ('キュ', 'シュ', 'チュ', 'ニュ', 'ヒュ', 'ミュ', 'リュ', 'ギュ', 'ジュ', 'ヂュ', 'ビュ', 'ピュ')
        o_diphthong = ('キョ', 'ショ', 'チョ', 'ニョ', 'ヒョ', 'ミョ', 'リョ', 'ギョ', 'ジョ', 'ヂョ', 'ビョ', 'ピョ')
        vowel_dict = {a: a_diphthong, u: u_diphthong, o: o_diphthong}

        substituted_yomi = yomi

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
        vowel_dict = {a: a_consonants, i: i_consonants, u: u_consonants, e: e_consonants, o: o_consonants}

        substituted_yomi = yomi

        for vowel, consonants in vowel_dict.items():
            for c in consonants:
                substituted_yomi = re.sub(c, vowel, substituted_yomi)

                if self._completed_substitution(yomi, substituted_yomi):
                    return substituted_yomi

        # 置換完了しなかった場合
        raise SubstitutionError(yomi, substituted_yomi)

    def _completed_substitution(self, origin, current):
        """
        母音と子音の置換が終わった場合 True を返す
        """
        # 可換な文字リスト
        substitutable_list = ('カ', 'サ', 'タ', 'ナ', 'ハ', 'マ', 'ヤ', 'ラ', 'ワ', 'ガ', 'ザ', 'ダ', 'バ', 'パ', "ャ",
                              'キ', 'シ', 'チ', 'ニ', 'ヒ', 'ミ',       'リ',       'ギ', 'ジ', 'ヂ', 'ビ', 'ピ',
                              'ク', 'ス', 'ツ', 'ヌ', 'フ', 'ム', 'ユ', 'ル',       'グ', 'ズ', 'ヅ', 'ブ', 'プ', "ュ",
                              'ケ', 'セ', 'テ', 'ネ', 'ヘ', 'メ',       'レ',       'ゲ', 'ゼ', 'デ', 'ベ', 'ペ',
                              'コ', 'ソ', 'ト', 'ノ', 'ホ', 'モ', 'ヨ', 'ロ', 'ヲ', 'ゴ', 'ゾ', 'ド', 'ボ', 'ポ', "ョ")

        for o, c in zip(origin, current):
            if o not in substitutable_list:
                continue
            if o == c:
                return False
        return True

    def create_marcov_table(self):
        """
        現在の単語とそれに続く単語のデータを作成．
        単語ごとの
        読み，品詞，字数
        テーブルを作成．
        """

    def create_words_table(self):
        """
        単語ごとの
        読み，品詞，字数
        テーブルを作成．
        """

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
    tc = TableCreator()
    data = tc.read_text()
    mecabed = tc.construct_mecabed_data(data)
    # print(repr(mecabed))
