import MeCab
import re

#すべてひらがなに変換する
def change_to_hiragana(text_array):
    # MeCabのインスタンスを作成
    mecab = MeCab.Tagger('-Ochasen')

    # 日本語のみを抽出するための正規表現パターン
    jp_pattern = re.compile(r'[\u3040-\u30FF\u4E00-\u9FFF]+')

    def process_text(text):
        # 空のテキストは無視
        if not text:
            return ''
        
        try:
            # テキストを形態素解析し、それぞれの単語をひらがなに変換
            parsed = mecab.parse(text)
            if parsed is None:
                print(f"MeCab解析に失敗しました: '{text}'")  # デバッグメッセージ
                return ''  # 解析に失敗した場合は空文字列を返す
            
            result = parsed.split('\n')

            hiragana_text = []
            for line in result:
                if line == 'EOS' or line == '':
                    continue
                parts = line.split('\t')
                if len(parts) > 3:
                    word = parts[0]  # 元の単語
                    reading = parts[1]  # 読み仮名（カタカナ）
                    
                    # 日本語の単語のみを処理（ひらがな・カタカナ・漢字に限定）
                    if jp_pattern.match(word):
                        # カタカナをひらがなに変換
                        hiragana_word = ''.join(
                            chr(ord(char) - 0x60) if 'ァ' <= char <= 'ン' else char for char in reading
                        )
                        hiragana_text.append(hiragana_word)

            hiragana_text = ''.join(hiragana_text)

            # 。と、を削除する
            chars_to_remove = ['。', '、']
            for char in chars_to_remove:
                hiragana_text = hiragana_text.replace(char, '')

            return hiragana_text

        except Exception as e:
            print(f"Error processing text '{text}': {e}")
            return ''  # エラーが発生した場合も空文字列を返す

    # 配列内の各テキストを処理
    return [process_text(text) for text in text_array if text]

if __name__ == '__main__':
    string = ['一番', '考える', '魑魅魍魎']
    print(change_to_hiragana(string))