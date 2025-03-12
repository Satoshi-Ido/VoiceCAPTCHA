import whisper
import Levenshtein
import MeCab

def main(voice, questionString):
    # whisperのモデル決め
    model = whisper.load_model('base')
    anserString = model.transcribe(voice, language="ja",fp16=False)['text']
    anserString = chengeHira(anserString)

    chars_to_remove = ['。','、', ' ']
    for char in chars_to_remove:
        questionString = questionString.replace(char, '')
    # print(f'Question:{questionString}')
    # print(f'answer:{anserString}')

    # Levenshtein(レーベンシュタイン) 距離を計算
    # 一方の文字列を他方に変換するために必要な操作の最小数（挿入、削除、置換）を示す。
    distance = Levenshtein.distance(questionString, anserString)
    # 文字列の最大長で割って一致度を計算（1から距離の割合を引く）
    max_len = max(len(questionString), len(anserString))
    # パーセンテージに変換
    similarity = (1 - distance / max_len) * 100  
    return similarity 

# 漢字をひらがなに変換する
def chengeHira(text):
    # インスタンスを作成
    mecab = MeCab.Tagger('-Ochasen')

    # テキストを形態素解析し、それぞれの単語をひらがなに変換
    parsed = mecab.parse(text)

    result = parsed.split('\n')

    hiragana_text = []
    for line in result:
        if line == 'EOS' or line == '':
            break
        parts = line.split('\t')
        if len(parts) > 3:
            # parts[1]は読み仮名
            hiragana_word = parts[1]
            hiragana_text.append(hiragana_word)

    hiragana_text = ''.join(hiragana_text)
    hiragana_text = ''.join(
        chr(ord(char) - 0x60) if 'ァ' <= char <= 'ン' else char for char in hiragana_text
    )

    # 。と、を削除する
    chars_to_remove = ['。','、']
    for char in chars_to_remove:
        hiragana_text = hiragana_text.replace(char, '')
    
    return hiragana_text

if __name__ == '__main__':
    main()