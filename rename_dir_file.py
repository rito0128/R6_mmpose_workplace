import os
import re

# ----------------------------------------------------
# ユーザー入力
# ----------------------------------------------------

# リネーム対象のディレクトリパスを入力
directory_path = input("📂 画像があるディレクトリのパスを入力してください: ").strip()

# 新しいファイル名に付ける任意の文字列を入力
prefix = input("🏷️ 新しいファイル名に付ける任意の文字列（例: photo_）を入力してください: ").strip()
if not prefix:
    prefix = "image_" # 文字列が空だった場合のデフォルト

# 連番の開始番号を入力
try:
    start_number = int(input("🔢 連番の開始番号を入力してください (例: 1): "))
except ValueError:
    start_number = 1 # 無効な入力の場合のデフォルト

# ----------------------------------------------------
# 処理ロジック
# ----------------------------------------------------

# 対象とする画像ファイルの拡張子リスト
IMAGE_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp')

# 処理結果を格納するリスト
rename_log = []
error_log = []
file_count = 0

if not os.path.isdir(directory_path):
    print(f"### ❌ エラー: 指定されたパスが見つかりません: `{directory_path}`")
else:
    # ディレクトリ内のファイルをリストアップ
    files = sorted(os.listdir(directory_path))

    for filename in files:
        # 拡張子を取得し、画像ファイルであるかチェック
        name, ext = os.path.splitext(filename)
        
        # 拡張子を小文字にしてチェック
        if ext.lower() in IMAGE_EXTENSIONS:
            file_count += 1
            
            # 連番をゼロ埋め (例: 001, 002)。ここでは最大999ファイルまでを想定
            # ファイル数に応じて桁数を調整してください (例: 4桁にするなら f'{num:04d}')
            num = start_number + file_count - 1
            new_filename = f'{prefix}{num:03d}{ext.lower()}'
            
            # 古いパスと新しいパスを生成
            old_filepath = os.path.join(directory_path, filename)
            new_filepath = os.path.join(directory_path, new_filename)
            
            try:
                # ファイル名を変更 (リネーム)
                os.rename(old_filepath, new_filepath)
                rename_log.append((filename, new_filename))
            except Exception as e:
                error_log.append((filename, str(e)))

# ----------------------------------------------------
# 結果表示
# ----------------------------------------------------
if file_count > 0 and not error_log:
    print(f"## ✅ リネーム完了: {len(rename_log)}個のファイルを処理しました")
elif file_count == 0:
    print(f"## ⚠️ 処理対象ファイルなし: 指定されたディレクトリ `{directory_path}` に画像ファイルが見つかりませんでした。")

# 変更ログの表示
if rename_log:
    print("### 📝 変更されたファイル名")
    # 結果を表形式で表示
    log_table = "| 元のファイル名 | 新しいファイル名 |\n| :--- | :--- |\n"
    for old, new in rename_log:
        log_table += f"| `{old}` | **`{new}`** |\n"
    print(log_table)

if error_log:
    print("### ⚠️ リネームエラー")
    for filename, error in error_log:
        print(f"* ファイル `{filename}` のリネームに失敗しました: {error}")