import numpy as np
import os

def save_string_array_to_npz(file_path, key_name, string_value, count, dtype_str='U10'):
    """
    file_path: 保存先のnpzファイル名
    key_name: 格納するキー名
    string_value: 格納したい文字列
    count: 配列の長さ (個数)
    dtype_str: NumPyの文字列型を指定 (例: 'U10', 'U70')
    """
    
    # 1. 指定された型で1次元配列を作成
    # np.fullを使用して、固定長の文字列型として初期化
    new_array = np.full(count, string_value, dtype=dtype_str)
    
    content = {}
    
    # 2. 既存ファイルがある場合は中身を読み込む
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        with np.load(file_path, allow_pickle=True) as data:
            # 既存の全データを取得
            content = {k: data[k] for k in data.files}
        
        # 3. すでに同じキーがある場合は後ろに追加（結合）
        if key_name in content:
            print(f"キー '{key_name}' は既存です。型 {content[key_name].dtype} で結合します。")
            # 結合。この際、既存のdtypeが優先されます。
            content[key_name] = np.concatenate([content[key_name], new_array])
        else:
            print(f"キー '{key_name}' を型 {dtype_str} で新規追加します。")
            content[key_name] = new_array
    else:
        # 新規作成
        print(f"新規ファイルを作成します: {file_path} (型: {dtype_str})")
        content[key_name] = new_array

    # 4. NPZとして保存
    np.savez_compressed(file_path, **content)
    
    # 最終的な型を確認して表示
    print(f"完了: '{key_name}' にデータ件数 {len(content[key_name])} 個を格納しました。")
    print(f"最終的なデータ型 (dtype): {content[key_name].dtype}")

import numpy as np
import os

def save_sequential_string_array_to_npz(file_path, key_name, prefix, count, start_num=1, digits=4, dtype_str='U20'):
    """
    file_path: 保存先のnpzファイル名
    key_name: 格納するキー名
    prefix: 文字列の接頭辞 (例: 'hm001')
    count: 生成する個数
    start_num: 開始番号 (デフォルト: 1)
    digits: 連番部分の桁数 (4の場合 '0001')
    dtype_str: NumPyの文字列型を指定 (連番を含むため長めに設定を推奨)
    """
    
    # 1. 連番を含む文字列リストを作成
    # 例: prefix='hm001', start_num=1 -> 'hm001_0001', 'hm001_0002'...
    seq_list = [f"{prefix}_{i:0{digits}d}" for i in range(start_num, start_num + count)]
    
    # NumPy配列に変換
    new_array = np.array(seq_list, dtype=dtype_str)
    
    content = {}
    
    # 2. 既存ファイルがある場合は中身を読み込む
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        with np.load(file_path, allow_pickle=True) as data:
            content = {k: data[k] for k in data.files}
        
        # 3. すでに同じキーがある場合は後ろに追加
        if key_name in content:
            print(f"キー '{key_name}' は既存です。結合します。")
            content[key_name] = np.concatenate([content[key_name], new_array])
        else:
            print(f"キー '{key_name}' を新規追加します。")
            content[key_name] = new_array
    else:
        print(f"新規ファイルを作成します: {file_path}")
        content[key_name] = new_array

    # 4. NPZとして保存
    np.savez_compressed(file_path, **content)
    
    print(f"完了: '{key_name}' に {count} 個の連番データを格納しました。")
    print(f"例: {content[key_name][0]} ... {content[key_name][-1]}")
    print(f"最終的なデータ型 (dtype): {content[key_name].dtype}")

# --- 連番の要素を追加---
save_sequential_string_array_to_npz(
    file_path='npz_file/original_train_anotation.npz', 
    key_name='imgname', 
    prefix='hm001_judo.C1', 
    count=11040,   # 11040個生成
    start_num=1,   # 1から開始
    digits=5,      # 5桁 (00001) に設定
    dtype_str='U70' # 文字列が長くなるのでU20に拡張
)

# # --- キーと要素を追加 ---
# # 'metadata.npz' に 'action' というキーで 'walking' を 50個入れる (最大10文字)
# save_string_array_to_npz(
#     file_path='npz_file/original_train_anotation.npz', 
#     key_name='subject', 
#     string_value='hm001', 
#     count=11040,
#     dtype_str='U10'
# )