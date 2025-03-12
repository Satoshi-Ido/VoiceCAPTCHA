import createTypo
import recording
import transcription
import clogEstimation
import responseSpeed

def main():
    # 問題文を作る
    print("-"*50)
    print("文章作成")
    typoString, typoAfterWord = createTypo.main()
    print("以下の文章を読み上げてください")
    print(typoString)
    print("-"*50)
    # 録音
    print("音声入力")
    fileName = "voice.wav"
    recording.main(fileName)
    print("-"*50)
    # 提示文字確認
    print("提示文確認")
    if transcription.main(fileName, typoString) < 50:
        print("認証を棄却しました")
        print("-"*50)
        return 0
    else:
        print("認証を採択しました")
        print("-"*50)
        print("発話型属性認証")
        clog = clogEstimation.main(fileName, typoAfterWord)
        speed = responseSpeed.main(fileName)
        print(f'応答速度:{speed}')
        print(f'詰り位置:{clog}')
        print(f'あなたは{clog*50+speed*50}%人間です')
        print("-"*50)
        return

if __name__ == '__main__':
    main()