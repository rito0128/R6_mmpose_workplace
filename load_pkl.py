import pickle
import pprint
import os
import numpy as np

def load_and_display_pkl():
    # 1. ファイルパスの入力
    print("読み込む.pklファイルを入力してください:")
    file_path = input().strip()

    if not os.path.exists(file_path):
        print(f"❌ ファイルが見つかりません: {file_path}")
        return

    try:
        # 2. ファイルの読み込み
        # Pickleはバイナリ形式なので 'rb' (Read Binary) モードで開きます
        with open(file_path, 'rb') as f:
            data = pickle.load(f)

        print("\n" + "="*50)
        print(f"📁 ファイル: {file_path}")
        print(f"🧬 データ型: {type(data)}")
        print("="*50 + "\n")

        # 3. データの構造に応じた表示処理
        if isinstance(data, dict):
            # 辞書型の場合、キーの一覧とデータの概要を表示
            print(f"🔑 辞書のキー一覧 ({len(data)}個):")
            for k in data.keys():
                val = data[k]
                # 値がNumPy配列やリストなら形状や長さを表示
                summary = ""
                if hasattr(val, 'shape'):
                    summary = f"shape={val.shape}"
                elif isinstance(val, list):
                    summary = f"length={len(val)}"
                
                print(f"  - {k}: {type(val)} {summary}")
            
            print("\n📝 辞書の内容（一部）:")
            # pprintで整形して表示
            pprint.pprint(data, depth=2, compact=True)

        elif isinstance(data, (list, tuple)):
            # リストやタプルの場合
            print(f"📊 要素数: {len(data)}")
            print("\n📝 内容（最初の3件）:")
            pprint.pprint(data[:3])

        elif hasattr(data, 'shape'):
            # NumPy配列などの場合
            print(f"🔢 形状 (Shape): {data.shape}")
            print(f"🔢 型 (Dtype): {data.dtype}")
            print("\n📝 内容（一部）:")
            print(data)

        else:
            # その他のオブジェクト
            print("📝 内容:")
            pprint.pprint(data)

    except Exception as e:
        print(f"❌ エラーが発生しました: {e}")

if __name__ == "__main__":
    load_and_display_pkl()