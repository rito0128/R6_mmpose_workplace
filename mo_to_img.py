import cv2
import os
import sys

def save_all_frames(video_path, dir_path, basename, ext='jpg'):
    #動画の読み込み
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        return

    #ディレクトリの作成
    if dir_path!=".":
        os.makedirs(dir_path, exist_ok=True)

    base_path = os.path.join(dir_path, basename)

    #フレーム数の桁数の取得
    digit = len(str(int(cap.get(cv2.CAP_PROP_FRAME_COUNT))))

    #フレーム数を取得
    frame = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    #FPSを取得
    fps=cap.get(cv2.CAP_PROP_FPS)

    print("この動画のフレーム数は{0}です。". format(frame))
    print("この動画のフレームレートは{0}fpsです。". format(fps))

    #書き出すフレーム数を入力
    print("書き出すフレーム数を入力してクレメンス")
    write_fps=input()
    print("書き出すフレーム数を{}と設定。". format(write_fps))

    n = 0
    #int(write_fps)-1

    #フレームごとに画像を読み込む
    while True:
        ret, frame = cap.read()
        if ret:
            if n == int(write_fps):
                return
            
            cv2.imwrite('{}_{}.{}'.format(base_path, str(n), ext), frame)
            n += 1
        else:
            return

args=sys.argv
if len(args)==4:
    #jpegで保存
    save_all_frames(args[1], args[2], args[3])
    #pngで保存
    #save_all_frames(args[1], args[2], args[3], 'png')
else:
    print("引数が足りないよ、、、、　読み込むファイル 保存先のディレクトリ 書き出すファイル(拡張子なしで)")