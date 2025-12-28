from mmpose.apis import MMPoseInferencer
import cv2
import numpy as np
import os

#入力する画像
print("入力する画像ファイルを選択")
img_path = input()
print(img_path + "を入力")

# 入力パスが有効か確認
if not os.path.exists(img_path):
    print(f"ファイルが見つかりません。指定したパスを確認してください: {img_path}")
    exit()

# instantiate the inferencer using the model alias
inferencer = MMPoseInferencer(pose3d="human3d")

# The MMPoseInferencer API employs a lazy inference approach,
# creating a prediction generator when given input
result_generator = inferencer(img_path, show=True)
result = next(result_generator)

# 結果画像を保存
output_path = 'output_result.jpg'

result_generator = inferencer(img_path, out_dir='output')
result = next(result_generator)

# 結果をjson形式で保存
result_generator = inferencer(img_path, pred_out_dir='predictions')
result = next(result_generator)
