from pydub import AudioSegment
from pydub.silence import detect_nonsilent

def audio_length(audio_path):
    # 音声ファイルを読み込む
    audio = AudioSegment.from_file(audio_path)
    # 無音ではない区間を検出する
    # 閾値(-50 dBFS)より大きい音の区間を取得 (dBFS: デシベル)
    nonsilent_ranges = detect_nonsilent(audio, min_silence_len=500, silence_thresh=-50)

    if nonsilent_ranges:
        # 最初の音声が始まる位置
        start_of_sound = nonsilent_ranges[0][0] / 1000  # ミリ秒を秒に変換
        
        # 最後の音声が終わる位置
        end_of_sound = nonsilent_ranges[-1][1] / 1000  # ミリ秒を秒に変換
        
        # duration_of_sound = end_of_sound - start_of_sound
        duration_of_sound = start_of_sound

    return duration_of_sound

def main(audio_path):
    speed = audio_length(audio_path)
    if 0 <= speed < 1:
        return 1
    elif 1 <= speed <= 2:
        return 2 - speed
    else:
        return 0

if __name__ == '__main__':
    main()