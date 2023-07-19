import pickle
from embedding import get_embedding
import numpy as np


def addition(new_item_name,new_image_link,new_item_class):
    with open("class_dict.pkl", "rb") as f:
        class_dict = pickle.load(f)

    new_text_embedding,new_image_embedding = get_embedding(new_item_name, new_image_link)
    new_class = new_item_class  # 根据实际情况设置类别信息

    if new_class in class_dict:
        print("该类别已存在")
        class_data = class_dict[new_class]
        class_data["items"].append(new_item_name)
        class_data["text_embeddings"].append(new_text_embedding)
        class_data["image_embeddings"].append(new_image_embedding)
        # 更新类别的平均向量
        text_average_embedding = np.mean(class_data["text_embeddings"], axis=0)
        image_average_embedding = np.mean(class_data["image_embeddings"], axis=0)
        class_data["text_average_embedding"] = text_average_embedding
        class_data["image_average_embedding"] = image_average_embedding
    else:
        print("该类别不存在,创建新类别")
        class_dict[new_class] = {
            "items": [new_item_name],
            "text_embeddings": [new_text_embedding],
            "image_embeddings": [new_image_embedding],
            "text_average_embedding": new_text_embedding,
            "image_average_embedding": new_image_embedding
        }

    # 输出添加到类别后的类别内容
    print(f"类别 {new_class} 的内容：")
    class_data = class_dict[new_class]
    for item, text_embedding, image_embedding in zip(class_data["items"], class_data["text_embeddings"],
                                                     class_data["image_embeddings"]):
        print(f"商品名称: {item}")
        print()

    with open("class_dict.pkl", "wb") as f:
        pickle.dump(class_dict, f)


def delete_item(class_name , item_to_remove):
    with open("class_dict.pkl", "rb") as f:
        class_dict = pickle.load(f)

    #检查要删除的类别是否存在：
    if class_name in class_dict:
        class_data = class_dict[class_name]
        items = class_data["items"]
        text_embeddings = class_data["text_embeddings"]
        image_embeddings = class_data["image_embeddings"]

        # 找到要删除的商品在类别中的索引
        item_index = items.index(item_to_remove)

        # 删除商品和对应的嵌入向量
        del items[item_index]
        del text_embeddings[item_index]
        del image_embeddings[item_index]

        # 更新类别的平均向量
        text_average_embedding = np.mean(text_embeddings, axis=0)
        image_average_embedding = np.mean(image_embeddings, axis=0)
        class_data["text_average_embedding"] = text_average_embedding
        class_data["image_average_embedding"] = image_average_embedding

        with open("class_dict.pkl", "wb") as f:
            pickle.dump(class_dict, f)

def delete_class(name_of_class):
    with open("class_dict.pkl", "rb") as f:
        class_dict = pickle.load(f)

    if class_name in class_dict:
        del class_dict[class_name]
    else:
        print(f"类别 {class_name} 不存在")

    with open("class_dict.pkl", "wb") as f:
        pickle.dump(class_dict, f)


if __name__ == 'main':
    item_name = "新款正品香奈包包女士小香儿真皮斜挎单肩百搭潮流链条金球小方包"
    image_path = "../data/test.jpg"
    class_name = "Chanel_金球盒子包_handbag"

    addition(item_name, image_path, class_name)