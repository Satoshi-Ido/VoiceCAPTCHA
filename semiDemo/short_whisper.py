import whisper
import os
import re

def short_whisper():
    # wav_files = glob.glob(os.path.join("shortAudio", '*.wav'))

    # フォルダ内を番号順に並び替えて取得
    wav_files = sort_wav_files('shortAudio')
    # print(wav_files)
    
    if not wav_files:
        print(f"No .wav files.")
        return None
    
    # whisperモデル選択
    model = whisper.load_model("base")
    # 戻り値用の配列
    transcriptionStrings = []
    for wav_file in wav_files:
        full_path = os.path.join('shortAudio', wav_file)
        try:
            result = model.transcribe(full_path, language="ja", fp16=False)['text']
            # print(f"File: {wav_file}")
            # print(f"Transcription: {result}")
            # print("-" * 50)
            transcriptionStrings.append(result)
        except Exception as e:
            print(f"Error processing {wav_file}: {str(e)}")
    
    # print(transcriptionStrings)
    return transcriptionStrings

def sort_wav_files(folder_path):
    # フォルダ内のすべてのWAVファイルを取得
    wav_files = [f for f in os.listdir(folder_path) if f.endswith('.wav')]
    
    # ファイル名から数字を抽出し、数字とファイル名のタプルのリストを作成
    numbered_files = []
    for file in wav_files:
        # ファイル名から数字を抽出
        match = re.search(r'\d+', file)
        if match:
            number = int(match.group())
            numbered_files.append((number, file))
    
    # 数字に基づいてファイルをソート
    sorted_files = sorted(numbered_files, key=lambda x: x[0])
    
    # ソートされたファイル名のリストを作成
    sorted_file_names = [file for _, file in sorted_files]
    
    return sorted_file_names

if __name__ == '__main__':
    short_whisper()