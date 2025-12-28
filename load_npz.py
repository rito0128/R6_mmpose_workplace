# npzを読み込む
import numpy as np

# input_file = input().strip()
input_file = "predictions\converted_npz\img_001.npz"

data = np.load(input_file, allow_pickle = True)
keys = list(data.keys())

# キーを表示
for key in keys:
    array = data[key]
    print(f"- {key}: shape={array.shape}, dtype={array.dtype}")

# 表示したいキーを選択
select_key = input().strip()
array_display = data[select_key]

# 配列の次元数に基づいてデータを表示
print("配列の次元数: " + str(array_display.ndim))

if array_display.ndim >= 1:
    # 1次元以上の場合、最初の5要素/行を表示
    print(array_display[:243])
else:
    # 0次元（単一の値）の場合
    print(array_display)