import json
import numpy as np
import os

# --- 設定 ---
EXPECTED_KEYPOINTS = 17 
OUTPUT_DIMENSIONS = 4 

# ----------------------------------------------------
# 1. パスの設定
# ----------------------------------------------------
print("入力するjsonディレクトリを選択")
input_dir = input().strip()
output_dir = os.path.join(input_dir, "converted_npz")
os.makedirs(output_dir, exist_ok=True)

# jsonファイルを取得
json_files = sorted([f for f in os.listdir(input_dir) if f.lower().endswith(('.json'))])

if not json_files:
    print(f"JSONファイルが見つかりません: {input_dir}")
    exit()

# ----------------------------------------------------
# 2. データの抽出と個別変換保存
# ----------------------------------------------------
processed_count = 0

print(f"\n⏳ {len(json_files)}個のファイルを処理中...")

for json_file in json_files:
    json_path = os.path.join(input_dir, json_file)
    file_base = os.path.splitext(json_file)[0]
    output_path = os.path.join(output_dir, f"{file_base}.npz")
    
    try:
        with open(json_path, 'r') as f:
            data = json.load(f)
            
            # ご提示の形式に合わせた抽出
            # トップレベルがリストなので最初の要素 [0] を取得
            target_data = data[0]
            
            # 3Dキーポイント (17x3)
            kpts_3d = np.array(target_data['keypoints'], dtype=np.float32)
            
            # スコア (17) -> (17x1) に整形
            scores = np.array(target_data['keypoint_scores'], dtype=np.float32).reshape(-1, 1)
            
            # 形状のチェック
            if kpts_3d.shape[0] != EXPECTED_KEYPOINTS:
                print(f"⚠️ スキップ ({json_file}): キーポイント数が {kpts_3d.shape[0]} です（期待値: 17）")
                continue

            # 座標とスコアを水平方向に結合 (17, 3) + (17, 1) -> (17, 4)
            keypoints_4d = np.hstack((kpts_3d, scores))
            
            # NPZファイルとして保存
            # キー名は後続のMotionBERTやBlender等で扱いやすい 'keypoints_3d' に設定
            np.savez_compressed(
                output_path, 
                keypoints_3d=keypoints_4d, 
                filename=file_base
            )
            
            processed_count += 1
            
    except Exception as e:
        print(f"❌ エラー ({json_file}): {e}")

print(f"\n✅ 完了: {processed_count}個のファイルを '{output_dir}' に作成しました。")


# import json
# import numpy as np
# import os
# #from IPython.display import display, Markdown

# # --- 設定 ---
# EXPECTED_KEYPOINTS = 17 
# OUTPUT_DIMENSIONS = 4 

# # ----------------------------------------------------
# # 1. パスの設定
# # ----------------------------------------------------
# print("入力するjsonディレクトリを選択")
# input_dir = input().strip()
# output_dir = os.path.join(input_dir, "converted_npz")
# os.makedirs(output_dir, exist_ok=True)

# # jsonファイルを取得
# json_files = sorted([f for f in os.listdir(input_dir) if f.lower().endswith(('.json'))])

# if not json_files:
#     print(f"JSONファイルが見つかりません: {input_dir}")
#     exit()

# # ----------------------------------------------------
# # 2. 構造の自動解析とインデックス設定
# # ----------------------------------------------------
# try:
#     with open(os.path.join(input_dir, json_files[0]), 'r') as f:
#         first_json = json.load(f)
    
#     # MMPose V1系の一般的な構造へのアクセス
#     # 構造が [ {...}, {...} ] のリスト形式かチェック
#     if isinstance(first_json, list):
#         data_root = first_json[0]
#     else:
#         data_root = first_json

#     # keypoints データの所在を探索
#     # 通常は 'instances' の中に人数分のポーズが入っています
#     if 'instances' in data_root:
#         instances = data_root['instances']
#     elif 'predictions' in data_root:
#         # predictions の中身がさらにリストの場合がある
#         preds = data_root['predictions']
#         instances = preds[0] if isinstance(preds, list) else preds
#     else:
#         # 構造が不明な場合、中身を直接表示してエラーにする
#         print("JSONの構造が解析できません。'instances' または 'predictions' キーが見つかりません。")
#         print("JSONのキー一覧:", data_root.keys())
#         exit()

#     max_index = len(instances) - 1
#     print(f"\n💡 各JSONファイルには、0から{max_index}までのポーズデータが格納されています。")
#     pose_index = int(input(f"🔢 抽出したいポーズデータのインデックス (0 から {max_index}) を入力してください: ").strip())

# except Exception as e:
#     print(f"初期化エラー: {e}")
#     import traceback
#     traceback.print_exc()
#     exit()

# # ----------------------------------------------------
# # 3. 変換処理
# # ----------------------------------------------------
# processed_count = 0
# for json_file in json_files:
#     json_path = os.path.join(input_dir, json_file)
#     file_base = os.path.splitext(json_file)[0]
#     output_path = os.path.join(output_dir, f"{file_base}.npz")
    
#     try:
#         with open(json_path, 'r') as f:
#             data = json.load(f)
#             # ルートがリストなら[0]を取る
#             root = data[0] if isinstance(data, list) else data
            
#             # ポーズデータの抽出 (MMPose V1.x 標準形式: instances[idx])
#             if 'instances' in root:
#                 target_instance = root['instances'][pose_index]
#             else:
#                 # 予備の探索 (旧形式など)
#                 target_instance = root['predictions'][pose_index]

#             # 3Dキーポイントとスコアの取得
#             # MMPose V1.x では 'keypoints' (3D) と 'keypoint_scores'
#             kpts_3d = np.array(target_instance['keypoints'], dtype=np.float32)
#             scores = np.array(target_instance['keypoint_scores'], dtype=np.float32).reshape(-1, 1)
            
#             # 結合して (17, 4) にする
#             keypoints_4d = np.hstack((kpts_3d, scores))
            
#             # 保存
#             np.savez_compressed(output_path, keypoints_3d=keypoints_4d, filename=file_base)
#             processed_count += 1
            
#     except Exception as e:
#         print(f"スキップ ({json_file}): {e}")

# print(f"\n✅ 完了: {processed_count}個のファイルを変換しました。")


# import json
# import numpy as np
# import os

# # --- 設定 ---
# # 期待されるキーポイントの数
# EXPECTED_KEYPOINTS = 17 
# # 期待される出力の次元数 (X, Y, Z, Score)
# OUTPUT_DIMENSIONS = 4 

# # ----------------------------------------------------
# # 1. パスの設定と検証
# # ----------------------------------------------------

# print("入力するjsonディレクトリを選択")
# input_dir = input().strip()

# # 出力先のディレクトリを作成（JSONと同じ場所、または別のフォルダを指定可能）
# output_dir = os.path.join(input_dir, "converted_npz")
# os.makedirs(output_dir, exist_ok=True)

# print(f"'{input_dir}' を入力として処理を開始します。")
# print(f"出力先: '{output_dir}'")

# # 入力ディレクトリが有効か確認
# if not os.path.exists(input_dir) or not os.path.isdir(input_dir):
#     # display(Markdown(f"### ❌ エラー: ディレクトリが見つかりません: `{input_dir}`"))
#     raise FileNotFoundError(f"ディレクトリが見つかりません: {input_dir}") 

# # ディレクトリ内のjsonファイルを取得
# json_files = sorted([f for f in os.listdir(input_dir) if f.lower().endswith(('.json'))])

# if not json_files:
#     # display(Markdown(f"### ⚠️ 処理対象ファイルなし: 指定したディレクトリ `{input_dir}` にJSONファイルが見つかりません。"))
#     raise RuntimeError("処理対象のJSONファイルが見つかりませんでした。")

# # ----------------------------------------------------
# # 2. 読み込むポーズデータのインデックス設定
# # ----------------------------------------------------

# try:
#     with open(os.path.join(input_dir, json_files[0]), 'r') as f:
#         first_json = json.load(f)
#     predictions_list = first_json['keypoints']['predictions'][0]
#     max_index = len(predictions_list) - 1
    
#     print(f"\n💡 各JSONファイルには、0から{max_index}までのポーズデータが格納されています。")
#     pose_index = int(input(f"🔢 抽出したいポーズデータのインデックス (0 から {max_index}) を入力してください: ").strip())
    
#     if not (0 <= pose_index <= max_index):
#         raise ValueError("範囲外のインデックス")
# except Exception as e:
#     print(f"初期化エラー: {e}")
#     raise

# # ----------------------------------------------------
# # 3. データの抽出・結合・個別保存
# # ----------------------------------------------------

# processed_count = 0
# # display(Markdown(f"### ⏳ {len(json_files)}個のJSONファイルを個別に変換中..."))

# for json_file in json_files:
#     json_path = os.path.join(input_dir, json_file)
#     # 出力ファイル名を作成 (例: image_01.json -> converted_npz/image_01.npz)
#     file_base = os.path.splitext(json_file)[0]
#     output_path = os.path.join(output_dir, f"{file_base}.npz")
    
#     try:
#         with open(json_path, 'r') as f:
#             json_data = json.load(f)
            
#         # ポーズ抽出
#         pose_data = json_data['keypoints']['predictions'][0][pose_index]
#         keypoints_3d = np.array(pose_data['keypoints'], dtype=np.float32)
#         keypoint_scores = np.array(pose_data['keypoint_scores'], dtype=np.float32).reshape(-1, 1)
        
#         # 検証
#         if keypoints_3d.shape != (EXPECTED_KEYPOINTS, 3):
#             continue
            
#         # 4D化 (17, 4)
#         keypoints_4d = np.hstack((keypoints_3d, keypoint_scores))
        
#         # --- 個別保存 ---
#         # 1ファイルごとにnpzを作成。
#         # 形状を (1, 17, 4) にして保存するか、(17, 4) で保存するかは用途に合わせて選べます。
#         # ここでは後続の処理で扱いやすいよう次元を維持したまま保存します。
#         np.savez_compressed(
#             output_path,
#             keypoints_3d=keypoints_4d,  # 形状: (17, 4)
#             filename=file_base
#         )
        
#         processed_count += 1
        
#     except (KeyError, IndexError):
#         continue # エラーのあるファイルはスキップ
#     except Exception as e:
#         print(f"エラー ({json_file}): {e}")

# # ----------------------------------------------------
# # 4. 完了表示
# # ----------------------------------------------------

# if processed_count == 0:
#     #display(Markdown("### ⚠️ 変換失敗: 有効なデータがありませんでした。"))
#     print("### ⚠️ 変換失敗: 有効なデータがありませんでした。")
# else:
#     #display(Markdown("---"))
#     #display(Markdown(f"## ✅ 処理完了: {processed_count}個のNPZファイルを `{output_dir}` に作成しました。"))
#     #display(Markdown(f"各NPZ内の `keypoints_3d` 形状: `({EXPECTED_KEYPOINTS}, {OUTPUT_DIMENSIONS})`"))
#     print(f"## ✅ 処理完了: {processed_count}個のNPZファイルを `{output_dir}` に作成しました。")
#     print(f"各NPZ内の `keypoints_3d` 形状: `({EXPECTED_KEYPOINTS}, {OUTPUT_DIMENSIONS})`")