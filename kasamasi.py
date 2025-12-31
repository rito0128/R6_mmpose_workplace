import os
import shutil
import re

def natural_keys(text):
    """文字列内の数字を数値として扱い、正しく連番ソートするための関数"""
    return [int(c) if c.isdigit() else c for c in re.split(r'(\d+)', text)]

def duplicate_frames(input_dir, output_dir, extension=".jpg"):
    # 出力ディレクトリがなければ作成
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 1. ファイルリストを取得して数値順にソート
    files = sorted([f for f in os.listdir(input_dir) if f.endswith(extension)], key=natural_keys)

    if not files:
        print("指定されたディレクトリに画像が見つかりませんでした。")
        return

    print(f"{len(files)}枚の画像を処理中...")

    new_count = 1
    for filename in files:
        # 元ファイルのフルパス
        src_path = os.path.join(input_dir, filename)
        
        # 2回コピーを実行
        for _ in range(2):
            # 新しいファイル名を作成（0埋め4桁の例: 0001, 0002...）
            new_filename = f"{new_count:04d}{extension}"
            dst_path = os.path.join(output_dir, new_filename)
            
            # ファイルをコピー
            shutil.copy2(src_path, dst_path)
            new_count += 1

    print(f"完了！ {output_dir} に {new_count - 1} 枚の画像を生成しました。")

# --- 設定 ---
INPUT_DIRECTORY = './img_dir/m3'   # 元画像があるフォルダ
OUTPUT_DIRECTORY = './img_dir/m3_kasamasi' # 保存先フォルダ
FILE_EXTENSION = '.jpg'              # 画像の拡張子

# 実行
duplicate_frames(INPUT_DIRECTORY, OUTPUT_DIRECTORY, FILE_EXTENSION)