import random

# ok　入換
def transpositionTypo(text):
    first_word = text[0]
    end_word = text[-1]
    middle_word = text[1: -1]

    list_middle_word = list(middle_word)
    # print(list_middle_word)
    small_chars = 'ゃゅょ'
    list_join = [] 
    i=0
    while i < len(list_middle_word):
        # 小さい文字が元の文章に入っているか
        if list_middle_word[i] in small_chars and list_join:
            # はい->配列の最後に結合する
            list_join[-1] += list_middle_word[i]
        else:
            # いいえ->新しい要素として追加する
            list_join.append(list_middle_word[i])
        
        i += 1

    # print(list_join)
    list_chenge = []

    if len(list_join) > 1:
        # 入れ替え場所を決める
        chengePoint = random.randint(0, len(list_join)-2)
        # print(chengePoint)

        left_words = ''.join(list_join[:chengePoint])
        right_words = ''.join(list_join[chengePoint+2:])
        # print(left_words)
        # print(right_words)

        for i in range(2):
            list_chenge.append(list_join[chengePoint-i+1])
        # print(list_chenge)
        pre_middle = ''.join(list_chenge)

        middle_word = left_words+pre_middle+right_words
    
    String = first_word+middle_word+end_word

    # 入れ替わっていることを確認する
    if text == String:
        transpositionTypo(text)

    return String, String[chengePoint+1:chengePoint+3]

# ok　削除して該当箇所を空白にする
def erasureTypo(text):
    first_word = text[0]
    end_word = text[-1]
    middle_word = text[1: -1]

    list_middle_word = list(middle_word)
    # print(list_middle_word)
    small_chars = 'ゃゅょ'
    list_join = [] 
    i=0
    while i < len(list_middle_word):
        # 小さい文字が元の文章に入っているか
        if list_middle_word[i] in small_chars and list_join:
            # はい->配列の最後に結合する
            list_join[-1] += list_middle_word[i]
        else:
            # いいえ->新しい要素として追加する
            list_join.append(list_middle_word[i])
        
        i += 1

    if len(list_join) > 0:
        spacePoint = random.randint(0, len(list_join)-1)
        # print("randint : "+str(spacePoint))
        left_words = ''.join(list_join[:spacePoint])
        right_words = ''.join(list_join[spacePoint+1:])

        middle_word = left_words+ '　' + right_words 

    String = first_word+middle_word+end_word

    return String, String[spacePoint+1:spacePoint+3]

# ok　関連した文字に変える
def substitutionTypo(text):
    first_word = text[0]
    end_word = text[-1]
    middle_word = text[1: -1]
    before = ['か','き','く','け','こ','さ','し','す','せ','そ','た','ち','つ','て','と','は','ひ','ふ','へ','ほ','や','ゆ','よ','が','ぎ','ぐ','げ','ご','ざ','じ','ず','ぜ','ぞ','だ','ぢ','づ','で','ど','ば','び','ぶ','べ','ぼ','ゃ','ゅ','ょ','っ']
    after = ['が','ぎ','ぐ','げ','ご','ざ','じ','ず','ぜ','ぞ','だ','ぢ','っ','で','ど','ば','び','ぶ','べ','ぼ','ゃ','ゅ','ょ','か','き','く','け','こ','さ','し','す','せ','そ','た','ち','つ','て','と','は','ひ','ふ','へ','ほ','や','ゆ','よ','つ']

    list_word = []
    list_inversion =[]
    chengePoint = 0

    for i in range(len(middle_word)):
        for j in range(len(before)):
            if before[j] in middle_word[i]:
                list_word.append(int(i))
                list_inversion.append(int(j))
    
    if len(list_word) > 1:
        i = random.randint(0, len(list_word)-1)
        chengePoint = i
        middle_word = middle_word.replace(middle_word[int(list_word[i])], after[int(list_inversion[i])])
    
    elif len(list_word) == 1:
        middle_word = middle_word.replace(middle_word[int(list_word[0])], after[int(list_inversion[0])])
    
    String = first_word+middle_word+end_word
    if text == String:
        substitutionTypo(text)

    return String, String[chengePoint+1:chengePoint+3]

# ok 削除して前後を結合する
def deletionTypo(text):
    first_word = text[0]
    end_word = text[-1]
    middle_word = text[1: -1]

    if len(middle_word) > 0:
        deletPoint = random.randint(0, len(middle_word)-1)
        # print("randint : "+str(i))
        middle_word = middle_word.replace(middle_word[deletPoint], '')

    String = first_word+middle_word+end_word

    return String, String[deletPoint+1:deletPoint+3]

# ok　別の文字を挿入する
def insertionTypo(text):
    first_word = text[0]
    end_word = text[-1:]
    middle_word = text[1: -1]

    hiragana = 'あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをん'
    random_hiragana = random.choice(hiragana)
    insert_position = random.randint(0, len(middle_word))

    middle_word = middle_word[:insert_position]+random_hiragana+middle_word[insert_position:]

    String = first_word+middle_word+end_word

    return String, String[insert_position+2:insert_position+4]

# text = "きゃくがいっぱいのきょうと"

# print("Original      : "+text)
# print("")
# print("Transposition : "+transpositionTypo(text))
# print("Erasure       : "+erasureTypo(text))
# print("Substitution  : "+substitutionTypo(text))
# print("Deletion      : "+deletionTypo(text))
# print("Insertion     : "+insertionTypo(text))