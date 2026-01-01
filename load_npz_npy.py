import numpy as np
import os

# ファイルパスの入力
print("読み込むファイル（.npz または .npy）を入力してください:")
input_file = input().strip()

if not os.path.exists(input_file):
    print(f"❌ ファイルが見つかりません: {input_file}")
    exit()

# 拡張子を確認
extension = os.path.splitext(input_file)[1].lower()

print(f"\n📁 ファイル名: {input_file}")

if extension == ".npz":
    # --- NPZ形式の処理 ---
    data = np.load(input_file, allow_pickle=True)
    keys = list(data.keys())
    
    print("📋 格納されているキー一覧:")
    for key in keys:
        array = data[key]
        print(f"  - {key}: shape={array.shape}, dtype={array.dtype}")

    print("\n表示したいキーを入力してください:")
    select_key = input().strip()
    
    if select_key in data:
        display_data = data[select_key]
    else:
        print(f"❌ キー '{select_key}' は見つかりません。")
        exit()

elif extension == ".npy":
    # --- NPY形式の処理 ---
    print("📦 NPY形式として読み込みます（単一配列）")
    display_data = np.load(input_file, allow_pickle=True)
    print(f"  - shape={display_data.shape}, dtype={display_data.dtype}")

else:
    print("❌ 対応していないファイル形式です（.npz または .npy のみ）")
    exit()

# --- データの表示処理 ---
print(f"\n🔢 配列の次元数: {display_data.ndim}")

# 表示範囲の指定（必要に応じて調整してください）
SHOW_COUNT = 243

if display_data.ndim >= 1:
    # 1次元以上の場合、指定された要素数まで表示
    # 実際のサイズが表示数より小さい場合に備えてスライスを使用
    print(display_data[:SHOW_COUNT])
else:
    # 0次元（単一の値）の場合
    print(display_data)

# 後片付け（npzの場合は閉じるのが推奨されます）
if extension == ".npz":
    data.close()