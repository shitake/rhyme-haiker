# -*- coding: utf-8 -*-
import random


class Markov(object):

    def build_model(self, tokens, n):
        """
        トークン(形態素)のリストからマルコフモデルを作成する．
        Args:
          tokens:
          n: n-gram
        Returns:
          単語の組をキー，次に続く単語を値とする辞書
        """
        model = dict()
        if len(tokens) < n:
            return model
        for i in range(len(tokens) - n):
            gram = tuple(tokens[i:i + n])
            next_token = tokens[i + n]
            model = self._append_token_to_model(model, gram, next_token=next_token)

        final_gram = tuple(tokens[len(tokens) - n:])
        model = self._append_token_to_model(model, final_gram)
        return model

    def _append_token_to_model(self, model, gram, next_token=None):
        """
        形態素リストを gram をキーとするモデルへ追加する．

        Args:
          model: 単語のタプルをキー，次に続く単語のリストを値とした辞書．
          gram: 単語のタプル
          next_token: gram に続く単語リスト．
                      デフォルト None．
        """
        if gram in model:
            model[gram].append(next_token)
        else:
            model[gram] = [next_token]
        return model

    def generate(self, model, n, seed=None, max_iterations=100):
        """
        model から n-gram モデルを生成する．
        Args:
          model: 単語のタプルをキー，次に続く単語のリストを値とした辞書．
          n: n-gram
          seed: 初期値
          max_iterations: 無限ループを防ぐためのループ回数上限．
        Returns:
          生成された単語のリスト
        """
        if seed is None:
            seed = random.choice(list(model.keys()))
        output = list(seed)
        current_tuple = tuple(seed)
        for i in range(max_iterations):
            if current_tuple in model:
                possible_next_tokens = model[current_tuple]  # リストのリスト
                next_token = random.choice(possible_next_tokens)
                if next_token is None:
                    break
                output.append(next_token)
                current_tuple = tuple(output[-n:])
            else:
                break
        return output

    def merge_models(self, models):
        pass

    def generate_from_token_lists(self, token_lines, n, count=14):
        pass

if __name__ == '__main__':
    m = Markov()
    n = 3
    tokens = ["古池", "あ", "古池", "い", "古池", "う", "蛙", "あ", "蛙", "い"]
    model = m.build_model(tokens, n)
    print(model)
    generated = m.generate(model, n)
    print(generated)
