import numpy as np
import pickle
import os

def create_camera_params_pkl(output_filename: str):
    """
    H36M形式の階層的なカメラパラメータ辞書を作成し、
    pickleファイルとして保存する関数。

    Args:
        output_filename (str): 出力ファイル名 (例: 'cameras.pkl').
    """

    print(f"--- {output_filename} の作成開始 ---")

    # --- 1. カメラパラメータ辞書の構造定義 ---
    
    # NumPy配列のデータ型はH36Mの慣習に合わせて float64 を使用
    float_dtype = np.float64

    # 🔑 被験者 '100' のカメラパラメータ
    params_100 = {
            # K (内部パラメータ行列): [fx, 0, cx], [0, fy, cy], [0, 0, 1]
            'K': np.array([[50.,   0., 500.],
                           [  0., 50., 500.],
                           [  0.,   0.,   1.]], dtype=float_dtype),
            # R (回転行列): 単位行列 (回転なし)
            'R': np.array([[1., 0., 0.],
                           [0., 1., 0.],
                           [0., 0., 1.]], dtype=float_dtype),
            # T (並進ベクトル): [X, Y, Z] (Z=3000mm = 3m)
            'T': np.array([[   6700.],
                           [   0.],
                           [1000.]], dtype=float_dtype),
            # dist (歪み係数): [k1, k2, p1, p2, k3]
            'dist': np.zeros(5, dtype=float_dtype),
            'w': 1000,
            'h': 1000
    }

    # --- 2. 最終的な辞書構造 ---
    # キーは被験者ID (整数または文字列)
    camera_params_dict = {
        ('hm001', 'C1'): params_100,  # 被験者ID 100
    }

    # --- 3. pickleファイルとして保存 ---
    try:
        with open(output_filename, 'wb') as f:
            pickle.dump(camera_params_dict, f)
        print(f"✅ {output_filename} の保存が完了しました。")
        print(f"キー: {list(camera_params_dict.keys())} が保存されました。")
    except Exception as e:
        print(f"❌ ファイル保存中にエラーが発生しました: {e}")
    
    print("-" * 40)


# ==============================================================================
# 実行例 (Jupyter Notebookで実行する際は、このセクションのコードを使用します)
# ==============================================================================

# --- ファイル生成関数の呼び出し ---

create_camera_params_pkl(
    output_filename='original_cameras.pkl'
)

# --- 生成したファイルの確認（オプション）---
# 別のセルで実行すると便利です。
# with open('cameras.pkl', 'rb') as f:
#     loaded_params = pickle.load(f)
# print("--- ロードされたデータ構造の確認 ---")
# print(f"キー: {list(loaded_params.keys())}")
# print(f"100 の K 行列:\n{loaded_params[100][0]['K']}")