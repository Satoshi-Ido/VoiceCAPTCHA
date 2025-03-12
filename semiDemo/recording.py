import sounddevice as sd
from scipy.io.wavfile import write
import threading
import time

# カウントダウン
def countdown_timer(seconds):
    for i in range(seconds, 0, -1):
        print(f"録音終了まで: {i}秒", end="\r")
        time.sleep(1)
    print("録音が終了しました。                 ")

# 録音を行うスレッド
def record_audio(sample_rate, duration, filename):
    print("録音を開始します...")
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
    sd.wait()  # 録音終了まで待機
    write(filename, sample_rate, recording)
    print(f"録音が保存されました: {filename}")

def main(filename):
    # サンプリング周波数 (Hz)
    sample_rate = 44100  
    # 録音時間 (秒)
    duration = 10  
    
    # カウントダウンスレッドを開始
    timer_thread = threading.Thread(target=countdown_timer, args=(duration,))
    audio_thread = threading.Thread(target=record_audio, args=(sample_rate, duration, filename))

    # 両方のスレッドを開始
    timer_thread.start()
    audio_thread.start()

    # 両方のスレッドが終了するのを待つ
    timer_thread.join()
    audio_thread.join()
