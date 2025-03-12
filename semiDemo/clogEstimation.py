import librosa
import numpy as np
from scipy.io import wavfile
from scipy.signal import stft, istft
import os
import re
import short_whisper
import chengeHira
import warnings
warnings.filterwarnings("ignore", message="PySoundFile failed. Trying audioread instead.")


def spectral_subtraction(signal, frame_length=2048, hop_length=512, noise_estimate_frames=10):
    # STFT(短時間フーリエ変換)を実行
    f, t, Zxx = stft(signal, nperseg=frame_length, noverlap=frame_length-hop_length)
    
    # ノイズスペクトルの推定（最初の10フレームを使用）
    noise_spectrum = np.mean(np.abs(Zxx[:, :noise_estimate_frames]), axis=1)
    
    # スペクトルサブトラクション
    cleaned_spectrum = np.maximum(0, np.abs(Zxx) - noise_spectrum[:, np.newaxis])
    cleaned_Zxx = cleaned_spectrum * np.exp(1j * np.angle(Zxx))
    
    # 逆STFTを実行
    _, cleaned_signal = istft(cleaned_Zxx, nperseg=frame_length, noverlap=frame_length-hop_length)
    
    return cleaned_signal

def calculate_short_time_energy(signal, frame_length=2048, hop_length=512):
    num_frames = 1 + (len(signal) - frame_length) // hop_length
    energy = np.zeros(num_frames)
    
    for i in range(num_frames):
        start = i * hop_length
        end = start + frame_length
        frame = signal[start:end]
        energy[i] = np.sum(frame**2) / frame_length
    
    return energy

def detect_silence(energy, threshold, hop_length, sr, min_silence_duration=0.2):
    # エネルギーがしきい値以下の箇所を特定
    is_silence = energy < threshold
    
    # 無音区間の開始時刻と終了時刻を取得
    silence_starts = []
    silence_ends = []
    in_silence = False
    silence_start = 0
    
    for i in range(len(is_silence)):
        if not in_silence and is_silence[i]:
            # 無音の開始
            silence_start = i
            in_silence = True
        elif in_silence and not is_silence[i]:
            # 無音の終了
            silence_duration = (i - silence_start) * hop_length / sr
            if silence_duration >= min_silence_duration:
                silence_starts.append(silence_start * hop_length / sr)
                silence_ends.append(i * hop_length / sr)
            in_silence = False
    
    # 最後の無音区間が続いている場合の処理
    if in_silence:
        silence_duration = (len(is_silence) - silence_start) * hop_length / sr
        if silence_duration >= min_silence_duration:
            silence_starts.append(silence_start * hop_length / sr)
            silence_ends.append(len(is_silence) * hop_length / sr)
    
    return silence_starts, silence_ends

# 2秒間の音声を切り出して保存する関数
def extract_audio_segments(audio_data, sample_rate, silence_ends):
    # 出力ディレクトリの作成
    os.makedirs("shortAudio", exist_ok=True)
    
    for i, time in enumerate(silence_ends):
        # サンプル数に変換(無音区間の0.2秒前に)
        start_sample = int((time - 0.2) * sample_rate)
        # print(f'end_time:{time}')
        # print(f'0.1秒前の時刻:{start_sample/sample_rate}')

        # 指定された時刻から2秒間（サンプル数）を切り出す
        end_sample = start_sample + 2 * sample_rate
        segment = audio_data[start_sample:end_sample]
        
        # 切り出した音声をファイルとして保存
        output_file = os.path.join("shortAudio", f"segment_{i}.wav")
        wavfile.write(output_file, sample_rate, segment)
        # print(f"Saved: {output_file}")

# 日本語以外の文字列を削除する関数
def remove_non_japanese_strings(arr):
    # 日本語文字が含まれる正規表現パターン
    japanese_pattern = re.compile(r'[ぁ-んァ-ン一-龯]')
    
    # 日本語文字が含まれる文字列だけを保持
    return [string for string in arr if japanese_pattern.search(string)]

def clear_wav_files():
    folder_path = "shortAudio"
    # フォルダ内のすべての.wavファイルを削除
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            # ファイルが.wav拡張子を持つか確認
            if os.path.isfile(file_path) and file_path.endswith('.wav'):
                os.unlink(file_path)  # .wavファイルを削除
        except Exception as e:
            print(f'Error: {e} - {file_path}')

def main(audio_path, typoAfterWord):
    # メイン処理

    # 音声データの読み込みとサンプリング
    sample_rate = 44100
    audio_data, sr = librosa.load(audio_path, sr=sample_rate)

    # スペクトルサブトラクション法による雑音除去
    cleaned_audio = spectral_subtraction(audio_data)

    # 短時間エネルギーの計算
    energy = calculate_short_time_energy(cleaned_audio)

    # 無音区間の検出
    silence_threshold = np.mean(energy) * 0.1  # しきい値は平均エネルギーの10%に設定（要調整）
    hop_length = 512  # calculate_short_time_energy関数で使用した値と同じにする
    silence_starts, silence_ends = detect_silence(energy, silence_threshold, hop_length, sr, min_silence_duration=0.2)
    # print(f'silence_starts:{silence_starts}')
    # print(f'silence_ends:{silence_ends}')

    # 無音区間が検出できなかった時は０を返す
    if not silence_ends:
        print("無音区間がありませんでした")
        return 0

    # 最初と最後を削除した配列
    silence_starts = silence_starts[1:-1]
    silence_ends = silence_ends[1:-1]

    # 無音区間を切り出す
    extract_audio_segments(audio_data, sample_rate, silence_ends)

    # 切り出した音声ファイルを文字起こし
    transcription = short_whisper.short_whisper()
    # print(transcription)
     
    transcription = remove_non_japanese_strings(transcription)
    # ひらがなに変換
    transcription = chengeHira.change_to_hiragana(transcription)
    # print(transcription)

    # 誤記の後ろの文字があるか確認する
    for word in transcription:
        while typoAfterWord in word:
            # shortAudioフォルダの中身を空にする
            clear_wav_files()   
            return 1

    # shortAudioフォルダの中身を空にする
    clear_wav_files()   

    return 0.5

