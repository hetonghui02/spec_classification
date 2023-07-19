import pandas as pd
import embedding
import numpy as np
import pickle


def get_embeddings(item_names, image_links):
    # 初始化嵌入向量列表
    text_embeddings = []
    image_embeddings = []

    for item_name, image_link in zip(item_names, image_links):
        # 调用 embedding.py 中的函数获取文本和图像的嵌入向量
        text_embedding, image_embedding = embedding.get_embedding(item_name, image_link)

        # 将嵌入向量添加到列表中
        text_embeddings.append(text_embedding)
        image_embeddings.append(image_embedding)

    return text_embeddings, image_embeddings


def classify(excel_path):
    # 读取Excel文件
    data = pd.read_excel(excel_path)
    item_names = data["item_name"].tolist()
    image_links = data["img_head"].tolist()
    brands = data["brand"].tolist()
    specs = data["spec"].tolist()
    classes = data["class"].tolist()

    # 调用函数获取图像和文本的嵌入向量
    text_embeddings, image_embeddings = get_embeddings(item_names, image_links)

    class_dict = {}

    for item_name, brand, spec, class_, text_embedding, image_embedding in zip(item_names, brands, specs, classes,
                                                                               text_embeddings, image_embeddings):
        class_name = f"{brand}_{spec}_{class_}"
        if class_name not in class_dict:
            class_dict[class_name] = {
                "items": [],
                "text_embeddings": [],
                "image_embeddings": [],
                "text_average_embedding": None,
                "image_average_embedding": None
            }
        class_dict[class_name]["items"].append(item_name)
        class_dict[class_name]["text_embeddings"].append(text_embedding)
        class_dict[class_name]["image_embeddings"].append(image_embedding)

        # 更新类别的平均向量
        class_dict[class_name]["text_average_embedding"] = np.mean(class_dict[class_name]["text_embeddings"], axis=0)
        class_dict[class_name]["image_average_embedding"] = np.mean(class_dict[class_name]["image_embeddings"], axis=0)

    # 打印每个类别的商品名称和嵌入向量的平均值
    for class_name, items_data in class_dict.items():
        items = items_data["items"]
        text_average_embedding = items_data["text_average_embedding"]
        image_average_embedding = items_data["image_average_embedding"]

        print(f"类别 {class_name}:")
        print(f"商品名称: {items}")
        print(f"文本嵌入向量平均值: {text_average_embedding}")
        print(f"图像嵌入向量平均值: {image_average_embedding}")
        print()

    with open("class_dict.pkl", "wb") as f:
        pickle.dump(class_dict, f)