import Levenshtein

def calculate_similarity(str1, str2):
    # Levenshtein 距離を計算
    distance = Levenshtein.distance(str1, str2)
    # 文字列の最大長で割って一致度を計算（1から距離の割合を引く）
    max_len = max(len(str1), len(str2))
    similarity = (1 - distance / max_len) * 100  # パーセンテージに変換
    return similarity

# サンプル
str1 = "halloeee"
str2 = "hallo"

similarity_score = calculate_similarity(str1, str2)
print(f"The similarity score between '{str1}' and '{str2}' is {similarity_score:.2f}%")
