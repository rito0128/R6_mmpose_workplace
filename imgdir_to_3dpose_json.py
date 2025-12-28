from mmpose.apis import MMPoseInferencer
import os
import glob

# --- 設定 ---
# 入力画像が入っているディレクトリを指定
print("画像ディレクトリのパスを入力してください（例: input_images/ ）")
input_dir = input().strip()

if not os.path.exists(input_dir):
    print(f"ディレクトリが見つかりません: {input_dir}")
    exit()

# 出力先ディレクトリの作成
os.makedirs('output', exist_ok=True)
os.makedirs('predictions', exist_ok=True)

# 1. 画像ファイルの取得とソート（連番順）
# 対応する拡張子を指定（jpg, pngなど）
img_extensions = ('.jpg', '.jpeg', '.png', '.JPG', '.PNG')
img_list = [f for f in os.listdir(input_dir) if f.endswith(img_extensions)]

# ファイル名を数値としてソート（例: 1.jpg, 2.jpg, 10.jpg を正しい順にする）
def extract_number(filename):
    # ファイル名から拡張子を除き、数字の部分だけを取り出す
    num_part = ''.join(filter(str.isdigit, filename))
    return int(num_part) if num_part else filename

img_list.sort(key=extract_number)

if not img_list:
    print("指定されたディレクトリに画像が見つかりませんでした。")
    exit()

print(f"{len(img_list)}枚の画像を連番順に処理します...")

# 2. 推論器の初期化
inferencer = MMPoseInferencer(pose3d="human3d")

# 3. ループ処理
for img_name in img_list:
    img_path = os.path.join(input_dir, img_name)
    
    # ファイル名（拡張子なし）を取得（例: "0001"）
    base_name = os.path.splitext(img_name)[0]
    
    print(f"処理中: {img_name}")

    # 推論実行
    # show=False にすることで Matplotlib の画面表示エラーを回避
    # out_dir: 可視化画像の保存先
    # pred_out_dir: JSON結果の保存先
    result_generator = inferencer(
        img_path, 
        show=False, 
        out_dir='output', 
        pred_out_dir='predictions'
    )
    result = next(result_generator)

    # MMPoseInferencerはデフォルトで元のファイル名でJSONを作りますが、
    # もし明示的にリネーム等が必要な場合はここで行います。
    # 現在のままでも predictions/base_name.json という形で保存されます。

print("\nすべて完了しました。")
print("画像結果: output/visualizations/")
print("JSON結果: predictions/")