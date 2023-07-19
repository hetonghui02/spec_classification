import os
import pandas as pd
import requests


# 创建保存图片的文件夹
picture_folder = './picture'
if not os.path.exists(picture_folder):
    os.makedirs(picture_folder)

# 读取Excel文件
df = pd.read_excel('val.xlsx')

df.dropna(inplace=True)

# 遍历每个商品
for index, row in df.iterrows():
    img_url = row['img_head']
    item_name = str(row['item_name'])
    item_name = item_name.replace('/', '-')  # 替换商品名中的斜杠，避免作为文件名的一部分

    # 生成保存图片的文件名
    file_name = item_name + '.jpg'
    file_path = os.path.join(picture_folder, file_name)

    # 处理重复的文件名
    count = 1
    while os.path.exists(file_path):
        file_name = f"{item_name}_{count}.jpg"
        file_path = os.path.join(picture_folder, file_name)
        count += 1

    # 下载并保存图片
    response = requests.get(img_url)
    with open(file_path, 'wb') as f:
        f.write(response.content)

print('图片保存完成！')

# 读取Excel文件
df = pd.read_excel('val_updated.xlsx')

# 生成新列
df['new_column'] = '../data/picture/' + df['item_name'].astype(str) +'.jpg'

# 保存修改后的Excel文件

df['命名'] = df['预测品牌'] + df['预测型号'] + df['预测类目']
df.to_excel('val_updated.xlsx', index=False)