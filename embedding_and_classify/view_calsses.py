import pandas as pd
import pickle

def view_h():
    # 加载 class_dict.pkl 文件
    with open("class_dict.pkl", "rb") as f:
        class_dict = pickle.load(f)

    # 创建 DataFrame 用于保存数据
    data = []
    for class_name, class_data in class_dict.items():
        items = class_data["items"]
        text_average_embedding = class_data["text_average_embedding"]
        image_average_embedding = class_data["image_average_embedding"]
        data.append([class_name, items, text_average_embedding, image_average_embedding])

    # 将数据转换为 DataFrame
    df = pd.DataFrame(data, columns=["Class Name", "Items", "Text Average Embedding", "Image Average Embedding"])

    # 保存 DataFrame 到 Excel 文件
    df.to_excel("class_dict.xlsx", index=False)
