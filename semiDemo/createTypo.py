import google.generativeai as genai
import MeCab
import random
import fiveTypo
import time

# 文節で分書をする
def bunsetsuWakachi(text):
    m = MeCab.Tagger('') #mecabのtagger objectの宣言

    m_result = m.parse(text).splitlines()
    m_result = m_result[:-1] #最後の1行は不要な行なので除く
    break_pos = ['名詞','動詞','接頭詞','副詞','感動詞','形容詞','形容動詞','連体詞'] #文節の切れ目を検出するための品詞リスト
    wakachi = [''] #分かち書きのリスト
    afterPrepos = False #接頭詞の直後かどうかのフラグ
    afterSahenNoun = False #サ変接続名詞の直後かどうかのフラグ
    for v in m_result:
        if '\t' not in v: continue
        surface = v.split('\t')[0] #表層系
        pos = v.split('\t')[1].split(',') #品詞など
        pos_detail = ','.join(pos[1:4]) #品詞細分類（各要素の内部がさらに'/'で区切られていることがあるので、','でjoinして、inで判定する)
        #この単語が文節の切れ目とならないかどうかの判定
        noBreak = pos[0] not in break_pos
        noBreak = noBreak or '接尾' in pos_detail
        noBreak = noBreak or (pos[0]=='動詞' and 'サ変接続' in pos_detail)
        noBreak = noBreak or '非自立' in pos_detail #非自立な名詞、動詞を文節の切れ目としたい場合はこの行をコメントアウトする
        noBreak = noBreak or afterPrepos
        noBreak = noBreak or (afterSahenNoun and pos[0]=='動詞' and pos[4]=='サ変・スル')
        if noBreak == False:
            wakachi.append("")
        wakachi[-1] += surface
        afterPrepos = pos[0]=='接頭詞'
        afterSahenNoun = 'サ変接続' in pos_detail
    if wakachi[0] == '': wakachi = wakachi[1:] #最初が空文字のとき削除する

    return wakachi

#すべてひらがなに変換する
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

# Geminiに文章の要求をする
def requestGemini():
    #google_api_key
    google_key='API-key'
    genai.configure(api_key=google_key)

    model = genai.GenerativeModel('gemini-1.5-pro')
    response = model.generate_content('々を含まない17字程度の一文をください')

    return response.text

# 誤記を入れる単語を決める
def typoPotion(hira_list, typo_position):
    place = int(len(hira_list)/3)
    typoPointFront, maxFront = 0, 0
    typoPointCenter, maxCenter = 0, 0
    typoPointBack, maxBack = 0, 0
    for i in range(len(hira_list)):
        if 0 <=  i <= place-1:
            if len(hira_list[i]) > maxFront:
                maxFront = len(hira_list[i])
                typoPointFront = i
        if place <= i <= place*2-1:
            if len(hira_list[i]) > maxCenter:
                maxCenter = len(hira_list[i])
                typoPointCenter = i
        if place*2 <= i <= len(hira_list)-1:
            if len(hira_list[i]) > maxBack:
                maxBack = len(hira_list[i])
                typoPointBack = i
    
    if typo_position == 0:
        return typoPointFront
    elif typo_position == 1:
        return typoPointCenter
    elif typo_position == 2:
        return typoPointBack

# 誤記を入れる
def typoIN(hira_list, typoPoint, typo_type):
    # 誤記文を仮保存する配列
    typo = []
    typoAfterWord = []
    for i in range(len(hira_list)):
        if i == typoPoint:
            if typo_type == 0:
                target = fiveTypo.transpositionTypo(hira_list[i])
                typo.append(target[0] + ' ')
                typoAfterWord.append(target[1])
            elif typo_type == 1:
                target = fiveTypo.erasureTypo(hira_list[i])
                typo.append(target[0] + ' ')
                typoAfterWord.append(target[1])
            elif typo_type == 2:
                target = fiveTypo.substitutionTypo(hira_list[i])
                typo.append(target[0] + ' ')
                typoAfterWord.append(target[1])
            elif typo_type == 3:
                target = fiveTypo.deletionTypo(hira_list[i])
                typo.append(target[0] + ' ')
                typoAfterWord.append(target[1])
            elif typo_type == 4:
                target = fiveTypo.insertionTypo(hira_list[i])
                typo.append(target[0] + ' ')
                typoAfterWord.append(target[1])
        else:
            typo.append((hira_list[i]) + ' ')

    return ''.join(typo), typoAfterWord[0]

def main():
    response = requestGemini()
    # 「々」はMeCabはひらがなに変換できないため
    while '々' in response:
        time.sleep(10)
        response = requestGemini()

    # 分かち書きに変換
    wakati_list = bunsetsuWakachi(response)
    # 全てひらがなに変換する
    hira_list = []
    for word in wakati_list:
        hira_list.append(chengeHira(word))

    # 誤記の種類を決める(支部連合論文から)
    daice = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
    weights = [0, 0, 0, 5, 4, 6, 0, 0, 0, 2, 7, 3, 8, 0, 1]
    random_typo = random.choices(daice, weights)
    # 誤記の種類
    typo_type = int(random_typo[0]/3)
    # 誤記の位置
    typo_position = int(random_typo[0]%3)
    typoPoint = typoPotion(hira_list, typo_position)
    # 原文の保存
    original = ''.join(hira_list)
    
    typoString = typoIN(hira_list, typoPoint, typo_type)
    # print(typo_type)
    # print(typoPoint)
    # print(original)
    # print(typoString[0], typoString[1])
    return typoString[0], typoString[1]

if __name__ == '__main__':
    main()