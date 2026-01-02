import numpy as np
import os

def append_data_to_npz(target_npz_path, source_npz_path, target_key, source_key=None):
    """
    target_npz_path: 編集したい（追記先の）NPZファイルパス
    source_npz_path: データを取得する（追記元の）NPZファイルパス
    target_key: 追記先のファイル内でのキー名
    source_key: 追記元のファイル内でのキー名（指定しない場合はtarget_keyと同じとみなす）
    """
    if source_key is None:
        source_key = target_key

    # 1. 追記元データの読み込み
    if not os.path.exists(source_npz_path):
        print(f"エラー: 追記元のファイルが見つかりません: {source_npz_path}")
        return

    with np.load(source_npz_path, allow_pickle=True) as src_data:
        if source_key not in src_data:
            print(f"エラー: 追記元ファイルにキー '{source_key}' がありません。")
            return
        new_array = src_data[source_key]

    # 2. 既存（追記先）データの読み込み
    content = {}
    if os.path.exists(target_npz_path) and os.path.getsize(target_npz_path) > 0:
        with np.load(target_npz_path, allow_pickle=True) as tar_data:
            # 全てのキーとデータを一旦辞書にコピー
            content = {k: tar_data[k] for k in tar_data.files}
        
        # 3. 指定したキーが既にある場合は後ろに追加（結合）
        if target_key in content:
            print(f"キー '{target_key}' は既存です。データを結合します。")
            # axis=0 (行方向/フレーム方向) で結合
            content[target_key] = np.concatenate([content[target_key], new_array], axis=0)
        else:
            print(f"キー '{target_key}' は新規です。データを追加します。")
            content[target_key] = new_array
    else:
        # 追記先ファイルがない場合は新規作成
        print(f"追記先ファイルが存在しないため新規作成します: {target_npz_path}")
        content[target_key] = new_array

    # 4. 上書き（または新規）保存
    np.savez_compressed(target_npz_path, **content)
    print(f"保存完了: {target_npz_path} (現在の形状: {content[target_key].shape})")

# --- 使用例 ---
# target の 'keypoints_2d' の後ろに、source の 'keypoints_2d' を追加する場合
append_data_to_npz(
    target_npz_path='npz_file/original_test_anotation.npz', 
    source_npz_path='npz_file/sourse_original_test_anotation.npz', 
    target_key='S'
)