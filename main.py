import regex as re
import speech_recognition as sr
import time
from janome.tokenizer import Tokenizer
from pprint import pprint

dev = True
r = sr.Recognizer()
mic = sr.Microphone()

# パターンリスト。
# index[0]に検索用正規表現
# index[1]に検索ワードを特定するための削除用正規表現
# index[2]に内部ID（srMainSwitch関数での分岐を分けるため）
pattern_list = [
    [r"Twitterで.*(に関して|について|を)検索", r"(Twitterで|に関して|について|を検索|検索)", 1],
    [r"Googleで.*(に関して|について|を)検索",  r"(Googleで|に関して|について|を検索|検索)", 2],
]

def srMainSwitch(text: str):

    #--- Develop info start ---
    print("[switch] --- start ---")
    #--- Develop info end ---

    # パターンリストの総当り検索
    for pattern in pattern_list:
        result = re.match(pattern[0], text)
        # ヒットする正規表現があったら
        # ・検索用正規表現をdelete_patternに入れて保存
        # ・内部IDをpattern_idに保存
        # した後、ループから離脱
        if result:
            delete_pattern = pattern[1]
            pattern_id = pattern[2]
            break

    # 上記ループ内で正規表現が見つからなかった場合
    if not result:
        print("[switch] 該当する正規表現が見つかりませんでした。")
        print("[switch] --- end ---")
        return

    # 恐らく今後見ることのない処理1
    if not delete_pattern:
        print("[switch] 該当する正規表現は見つかりましたが、登録漏れや例外のため、削除用の正規表現が見つかりませんでした。")
        print("[switch] --- end ---")
        return

    # 恐らく今後見ることのない処理2
    if not pattern_id:
        print("[switch] 該当する正規表現、削除用正規表現は見つかりましたが、登録漏れや例外のため、内部IDが見つかりませんでした。")
        print("[switch] --- end ---")
        return


    if pattern_id == 1:
        # 検索ワードを正規表現で絞り込み
        search_word = re.sub(delete_pattern, "", result.group())
        print(f"[switch] Twitterで「{search_word}」を検索します。")

    elif pattern_id == 2:
        # 検索ワードを正規表現で絞り込み
        search_word = re.sub(delete_pattern, "", result.group())
        print(f"[switch] Googleで「{search_word}」を検索します。")

    #--- Develop info start ---
    print("[switch] --- end ---")
    #--- Develop info end ---

    return

def srJanome(text: str):
    """
    Janomeを使用して、音声認識で認識した文章を形態素解析する。


    Parameters
    ----------
    text : str
        srMain関数より取得したテキスト

    Returns
    -------
    tokenized_list : list
        textを形態素解析し、[表層形, 品詞]の形のlistにした後、二次元配列にしたものを返す。
        index[0]には、必ず元のテキストがstrで収納される。
    """

    # 形態素解析
    tokenizer = Tokenizer()
    # 元のテキストのみが収納されたリストを作成
    tokenized_list = [text]

    #--- Develop info start ---
    print("[janome] --- start ---")
    #--- Develop info end ---

    for token in tokenizer.tokenize(text):
        # リストに"表層形 品詞"の形で収納
        tokenized_list.append([token.surface, token.part_of_speech])
        print(f"[janome] {token.surface} | {token.part_of_speech}")

    #--- Develop info start ---
    print("[janome] --- end ---")
    #--- Develop info end ---

    return tokenized_list

def srMain():
    """
    音声認識で文字起こしをする関数。

    Returns
    -------
    text : str
        文字起こしをした文字列をstrで返す。
    """

    #--- Develop info start ---
    if dev: print("[sr] --- start ---")
    #--- Develop info end ---

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
            # Google Speech Recognitionを利用
            sr_result = r.recognize_google(audio, language='ja-JP')

            #--- Develop info start ---
            dev_elapdsed_time = time.time() - dev_start_time
            if dev==True: print(f"[sr][dev] 音声認識処理時間: {dev_elapdsed_time}秒")
            #--- Develop info end ---

            # 認識結果を返答
            print(f"[sr] 認識結果: {sr_result}")

            #--- Develop info start ---
            print("[sr] --- end ---")
            #--- Develop info end ---

            return sr_result.replace(" ", "")

        # 例外処理
        except sr.UnknownValueError:
            print("[sr][error] 日本語を聞き取れませんでした。")
        except sr.RequestError as e:
            print("[sr][error] Google Speech Recognition への接続に失敗しました。; {0}".format(e))

if __name__ == "__main__":
    while True:
        text = srMain()
        srMainSwitch(text=text)