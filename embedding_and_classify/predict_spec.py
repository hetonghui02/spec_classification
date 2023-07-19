import pickle
import numpy as np
import sys
# 导入 embedding.py 中的函数和类
from embedding import get_embedding
import pandas as pd

pre_specs = []
true_specs = []

#计算准确率
def calculate_accuracy(true_labels, predicted_labels):
    total_samples = len(true_labels)
    correct_predictions = 0

    for true_label, predicted_label in zip(true_labels, predicted_labels):
        print(true_label,predicted_label)
        if true_label == predicted_label:
            correct_predictions += 1

    accuracy = correct_predictions / total_samples

    return accuracy

def compute_similarity(embedding1, embedding2):
    # 计算余弦相似度
    similarity = np.dot(embedding1, embedding2) / (np.linalg.norm(embedding1) * np.linalg.norm(embedding2))
    return similarity

def predict_data(excel_path):
    # 读取Excel文件
    new_data = pd.read_excel(excel_path)
    new_item_names = new_data["命名"].tolist()
    new_image_links = new_data["img_head"].tolist()
    new_classes = new_data["预测类目"].tolist()
    new_brands = new_data["预测品牌"].tolist()
    new_specs = new_data["预测型号"].tolist()


    # 从文件中加载类别平均向量
    with open("class_dict.pkl", "rb") as f:
        class_dict = pickle.load(f)

    # 遍历新数据进行预测
    for new_item_name, new_image_link, new_class, new_brand, new_spec in zip(new_item_names, new_image_links, new_classes,
                                                                   new_brands, new_specs):
        # 获取新数据的文本向量和图像向量
        new_text_embedding, new_image_embedding = get_embedding(new_item_name, new_image_link)
        true_spec = f"{new_brand}_{new_spec}_{new_class}"
        true_specs.append(true_spec)

        # 初始化相似度列表
        text_similarities = []
        image_similarities = []
        class_similarities = []

        for class_name, class_data in class_dict.items():
            text_average_embedding = class_data["text_average_embedding"]
            image_average_embedding = class_data["image_average_embedding"]

            # 计算文本相似度和图像相似度
            text_similarity = compute_similarity(new_text_embedding, text_average_embedding)
            image_similarity = compute_similarity(new_image_embedding, image_average_embedding)

            # 计算图像与类的相似度
            class_similarity = text_similarity * 0.5 + image_similarity * 0.5

            # 将相似度添加到相似度列表
            text_similarities.append(text_similarity)
            image_similarities.append(image_similarity)
            class_similarities.append(class_similarity)

            # 如果图像与类的相似度大于90%，则将新数据加入到该类中，并更新类别的平均向量
            if class_similarity > 0.85:
                class_data["items"].append(new_item_name)
                class_data["text_embeddings"].append(new_text_embedding)
                class_data["image_embeddings"].append(new_image_embedding)

                # 更新类别的平均向量
                text_average_embedding = np.mean(class_data["text_embeddings"], axis=0)
                image_average_embedding = np.mean(class_data["image_embeddings"], axis=0)
                class_data["text_average_embedding"] = text_average_embedding
                class_data["image_average_embedding"] = image_average_embedding




        # 获取前三个相似度的索引
        top_text_indices = np.argsort(text_similarities)[-3:][::-1]
        top_image_indices = np.argsort(image_similarities)[-3:][::-1]
        top_class_indices = np.argsort(class_similarities)[-3:][::-1]

        # 找到最大相似度和对应的类别
        max_similarity = max(class_similarities)
        max_class_index = np.argmax(class_similarities)
        max_class = list(class_dict.keys())[max_class_index]

        # 输出前三个文本相似度、图像相似度和总体相似度
        print(f"商品 {new_item_name} 的相似度排名：")
        print("文本相似度:")
        for index in top_text_indices:
            print(f" - 类别 {list(class_dict.keys())[index]}: {text_similarities[index]}")
        print("图像相似度:")
        for index in top_image_indices:
            print(f" - 类别 {list(class_dict.keys())[index]}: {image_similarities[index]}")
        print("总体相似度:")
        for index in top_class_indices:
            print(f" - 类别 {list(class_dict.keys())[index]}: {class_similarities[index]}")

        # 如果没有匹配到任何类别，则创建新类别并将新数据加入其中
        if max_similarity < 0.8:
            new_class_name = f"{new_brand}_{new_spec}_{new_class}"
            class_dict[new_class_name] = {
                "items": [new_item_name],
                "text_embeddings": [new_text_embedding],
                "image_embeddings": [new_image_embedding],
                "text_average_embedding": new_text_embedding,
                "image_average_embedding": new_image_embedding
            }
            print(f"商品 {new_item_name} 创建新类别 {new_class_name}")
            #pre_specs.append(new_class_name)
        else:
            #pre_specs.append(max_class)
            print(f"商品 {new_item_name} 归类到类别 {max_class}，相似度为 {max_similarity}")

     #保存更新后的类别平均向量到文件
    with open("class_dict.pkl", "wb") as f:
        pickle.dump(class_dict, f)
