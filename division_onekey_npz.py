import numpy as np
import os

def split_npz_keys_from_end(input_path, output_path, keys_to_extract, num_elements):
    """
    input_path: 元のnpzファイル
    output_path: 切り出したデータを保存する新しいnpzファイル
    keys_to_extract: 抽出（末尾スライス）の対象にするキーのリスト
    num_elements: 末尾から取り出す要素数
    """
    if not os.path.exists(input_path):
        print(f"エラー: ファイルが見つかりません: {input_path}")
        return

    split_content = {}

    # 1. 元のファイルを読み込む
    with np.load(input_path, allow_pickle=True) as data:
        # 指定されたキーが実際にファイル内に存在するか確認
        for key in keys_to_extract:
            if key not in data.files:
                print(f"⚠️ スキップ: キー '{key}' はファイル内に存在しません。")
                continue

            array = data[key]
            total_count = len(array)

            if num_elements > total_count:
                print(f"⚠️ 警告: キー '{key}' の要素数({total_count})が指定数({num_elements})より少ないため、全要素をコピーします。")
                split_content[key] = array
            else:
                # 2. 末尾から num_elements 分のスライスを取得
                split_content[key] = array[-num_elements:]
            
            print(f"✅ 抽出中 '{key}': {total_count}個 -> 末尾{len(split_content[key])}個を取得")

    if not split_content:
        print("❌ 抽出できるデータがなかったため、保存を中止しました。")
        return

    # 3. 新しいnpzファイルとして保存
    np.savez_compressed(output_path, **split_content)
    print(f"\n✨ 完了: {output_path} に指定キーの末尾データを保存しました。")

# --- 使用例 ---
# 'keypoints_2d' と 'keypoints_3d' だけを対象に、末尾24要素を切り出して別ファイルにする
split_npz_keys_from_end(
    input_path='npz_file/original_train_anotation.npz', 
    output_path='npz_file/original_test_anotation.npz', 
    keys_to_extract=['keypoints_2d', 'S'], # 抽出したいキーをリストで指定
    num_elements=24
)