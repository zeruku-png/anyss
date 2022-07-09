import pyaudio
import regex as re
import speech_recognition as sr
import time

dev = True
r = sr.Recognizer()
mic = sr.Microphone()

def srMain():
    while True:
        print("[sr] 音声認識を待機中...")

        # 音声を取得
        with mic as source:
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)

        #--- Develop info start ---
        dev_start_time = time.time()
        #--- Develop info end ---

        print ("[sr] 認識した音声を処理中...")

        try:
            sr_result = r.recognize_google(audio, language='ja-JP')

            #--- Develop info start ---
            dev_elapdsed_time = time.time() - dev_start_time
            if dev==True:
                print(f"[sr][dev] 音声認識処理時間: {dev_elapdsed_time}秒")
            #--- Develop info end ---

            print(f"[sr] 認識結果: {sr_result}")

        # 例外処理
        except sr.UnknownValueError:
            print("[sr][error] 日本語を聞き取れませんでした。")
        except sr.RequestError as e:
            print("[sr][error] Google Speech Recognition service への接続に失敗しました。; {0}".format(e))
