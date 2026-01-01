import numpy as np
import os

def shorten_npz_by_removing_end(file_path, num_to_remove):
    """
    file_path: 対象のnpzファイル（読み込んで上書きします）
    num_to_remove: 末尾から削除する要素の数
    """
    if not os.path.exists(file_path):
        print(f"エラー: ファイルが見つかりません: {file_path}")
        return

    shortened_content = {}

    # 1. 元のファイルを読み込む
    with np.load(file_path, allow_pickle=True) as data:
        for key in data.files:
            array = data[key]
            total_count = len(array)

            if num_to_remove >= total_count:
                print(f"⚠️ 警告: キー '{key}' の要素数({total_count})が削除指定数({num_to_remove})以下のため、配列が空になります。")
                # 空の配列を作成（元の型を維持）
                shortened_content[key] = array[:0]
            else:
                # 2. 最初から「末尾の指定数」の手前までを取り出す
                # array[:-1000] は「最初から、後ろから数えて1000番目の手前まで」という意味
                shortened_content[key] = array[:-num_to_remove]
            
            print(f"キー '{key}': {total_count}個 -> {len(shortened_content[key])}個に短縮")

    # 3. 同じファイル名で上書き保存
    np.savez_compressed(file_path, **shortened_content)
    print(f"\n✅ 短縮完了: {file_path} を更新しました。")

# --- 使用例 ---
# 'original_train_anotation.npz' の各データから、末尾の 1000要素を削除して上書きする
shorten_npz_by_removing_end(
    file_path='npz_file/original_train_anotation.npz', 
    num_to_remove=24
)