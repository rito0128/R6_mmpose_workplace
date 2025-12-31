import pyrealsense2 as rs
import numpy as np
import cv2
import os

#入力ファイル
print("入力ファイルを指定して")
bag_file = input()  # bagファイルのパスを指定
if not os.path.exists(bag_file):
    raise FileNotFoundError(f"指定したファイルがないよ")

print(bag_file + "をmp4に変換")

#出力ファイル
print("出力ファイルを指定して")
out_mp4 = input() 

#f = open('out_mp4', 'w')
#f.close()

#メイン処理
# RealSenseパイプラインの設定
config = rs.config()
config.enable_device_from_file(bag_file)

pipeline = rs.pipeline()
profile = pipeline.start(config)

# ストリームの情報取得
for stream in profile.get_streams():
    vprof = stream.as_video_stream_profile()
    if vprof.format() == rs.format.rgb8:
        frame_rate = vprof.fps()
        size = (vprof.width(), vprof.height())

# 動画ライターの準備
fmt = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')  # mp4形式
writer = cv2.VideoWriter(out_mp4, fmt, frame_rate, size)

#加筆
last_frame_number = 0

print(f"\\\\\\\\変換中\\\\\\\\\ '{bag_file}' to '{out_mp4}'...")
try:
    cur_position = -1
    playback = profile.get_device().as_playback()
    playback.set_real_time(False)#加筆

    while True:
        # フレーム取得
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()

        #加筆
        current_frame_number = color_frame.get_frame_number()

        if current_frame_number == last_frame_number:  # 同じフレームの場合はスキップ
            continue

        last_frame_number = current_frame_number  # 最新のフレーム番号を記録

        # フレームデータを処理
        color_image = np.asanyarray(color_frame.get_data())
        color_image = cv2.cvtColor(color_image, cv2.COLOR_RGB2BGR)
        writer.write(color_image)

        # 可視化オプション
        #if bag_file.visualize:
            #cv2.imshow("Video Preview", color_image)
            #if cv2.waitKey(1) & 0xFF == ord('q'):  # 'q'キーで中断
                #break

        # 再生位置の確認
        next_position = playback.get_position()
        if next_position < cur_position:  # 再生終了条件
            break
        cur_position = next_position

finally:
    # 後処理
    pipeline.stop()
    writer.release()
    cv2.destroyAllWindows()
    print(f"変換完了　 {out_mp4}")