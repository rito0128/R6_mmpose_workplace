import numpy as np
import os

def split_npz_from_end(input_path, output_path, num_elements):
    """
    input_path: 元のnpzファイル
    output_path: 切り出したデータを保存する新しいnpzファイル
    num_elements: 末尾から取り出す要素数
    """
    if not os.path.exists(input_path):
        print(f"エラー: ファイルが見つかりません: {input_path}")
        return

    split_content = {}

    # 1. 元のファイルを読み込む
    with np.load(input_path, allow_pickle=True) as data:
        # すべてのキーをループ処理
        for key in data.files:
            array = data[key]
            total_count = len(array)

            if num_elements > total_count:
                print(f"⚠️ 警告: キー '{key}' の要素数({total_count})が指定数({num_elements})より少ないため、全要素をコピーします。")
                split_content[key] = array
            else:
                # 2. 末尾から num_elements 分のスライスを取得
                # array[-num_elements:] は後ろから数えて指定個数分を取り出す書き方
                split_content[key] = array[-num_elements:]
            
            print(f"キー '{key}': {total_count}個 -> {len(split_content[key])}個を抽出")

    # 3. 新しいnpzファイルとして保存
    np.savez_compressed(output_path, **split_content)
    print(f"\n✅ 分割完了: {output_path} に保存しました。")

# --- 使用例 ---
# 'original.npz' の各キーの末尾から 1000要素を取り出して 'test_data.npz' を作る
split_npz_from_end(
    input_path='npz_file/original_train_anotation.npz', 
    output_path='npz_file/original_test_anotation.npz', 
    num_elements=24
)