import numpy as np
import os

def remove_key_from_npz(file_path, keys_to_remove):
    """
    file_path: 対象のnpzファイルパス
    keys_to_remove: 削除したいキーの名前（単一の文字列、またはリスト）
    """
    if not os.path.exists(file_path):
        print(f"エラー: ファイルが見つかりません: {file_path}")
        return

    # 削除対象が単一の文字列ならリストに変換
    if isinstance(keys_to_remove, str):
        keys_to_remove = [keys_to_remove]

    content = {}
    removed_any = False

    # 1. 既存ファイルを読み込む
    with np.load(file_path, allow_pickle=True) as data:
        # 全てのキーをループ
        for k in data.files:
            if k in keys_to_remove:
                print(f"🔥 キー '{k}' を削除対象として除外します。")
                removed_any = True
            else:
                # 削除対象でないものだけを辞書にコピー
                content[k] = data[k]

    # 2. 削除が実行された場合のみ上書き保存
    if removed_any:
        np.savez_compressed(file_path, **content)
        print(f"✅ 上書き保存が完了しました: {file_path}")
    else:
        print("⚠️ 指定されたキーは見つかりませんでした。変更は行われません。")

# --- 使用例 ---
# 'metadata.npz' から 'action' と 'old_key' を削除する場合
remove_key_from_npz('npz_file/original_test_anotation.npz', ['keypoints_2d', 'S'])