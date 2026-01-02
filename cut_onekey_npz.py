import numpy as np
import os

def shorten_npz_keys(file_path, keys_to_shorten, num_to_remove):
    """
    file_path: 対象のnpzファイル
    keys_to_shorten: 短縮（末尾削除）を適用したいキーのリスト
    num_to_remove: 末尾から削除する要素の数
    """
    if not os.path.exists(file_path):
        print(f"エラー: ファイルが見つかりません: {file_path}")
        return

    updated_content = {}

    # 1. 元のファイルを読み込む
    with np.load(file_path, allow_pickle=True) as data:
        for key in data.files:
            array = data[key]
            total_count = len(array)

            # 指定されたキーリストに含まれている場合のみ短縮処理を行う
            if key in keys_to_shorten:
                if num_to_remove >= total_count:
                    print(f"⚠️ 警告: キー '{key}' の要素数({total_count})が削除指定数以下です。空にします。")
                    updated_content[key] = array[:0]
                else:
                    updated_content[key] = array[:-num_to_remove]
                print(f"✂️ 短縮適用 '{key}': {total_count}個 -> {len(updated_content[key])}個")
            
            else:
                # 指定されていないキーはそのままコピー
                updated_content[key] = array
                print(f"保持済み '{key}': {total_count}個 (変更なし)")

    # 2. 上書き保存
    np.savez_compressed(file_path, **updated_content)
    print(f"\n✅ 処理完了: {file_path} を更新しました。")

# --- 使用例 ---
# 'original_train_anotation.npz' 内の 'keypoints_2d' と 'keypoints_3d' だけ末尾24個消す場合
shorten_npz_keys(
    file_path='npz_file/original_train_anotation.npz', 
    keys_to_shorten=['keypoints_2d', 'S'], # 対象のキーをリストで指定
    num_to_remove=24
)