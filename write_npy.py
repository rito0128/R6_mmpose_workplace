import numpy as np
import os

def create_fixed_5_npy():
    # 1. 保存先ファイル名の入力
    print("作成するファイル名を入力してください（例: data.npy）:")
    file_path = input().strip()
    if not file_path.endswith('.npy'):
        file_path += '.npy'

    # 2. 値の入力
    print("\n配列に格納する5つの値をスペース区切りで入力してください:")
    print("入力例: 1.2 3.4 5.6 7.8 9.0")
    
    try:
        raw_input = input().strip().split()
        
        # 個数チェック
        if len(raw_input) != 5:
            print(f"❌ エラー: 要素の数が {len(raw_input)} 個です。5個ちょうど入力してください。")
            return

        # 数値（float）に変換して配列を作成
        # 文字列として保存したい場合は dtype='U20' などに変更してください
        array = np.array(raw_input, dtype=np.float32)

        # 3. 保存
        np.save(file_path, array)
        
        print("\n✅ 保存が完了しました。")
        print(f"ファイル: {os.path.abspath(file_path)}")
        print(f"内容: {array}")
        print(f"Shape: {array.shape}, Dtype: {array.dtype}")

    except ValueError:
        print("❌ エラー: 数値として解釈できない文字が含まれています。")
    except Exception as e:
        print(f"❌ 予期せぬエラーが発生しました: {e}")

if __name__ == "__main__":
    create_fixed_5_npy()