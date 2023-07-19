from modelscope.pipelines.multi_modal.gridvlp_pipeline import GridVlpClassificationPipeline

import pandas as pd
import re
from modelscope.models import Model
from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
from PIL import Image
import requests


def GridVLP(excel_path):
    # 从Excel文件中读取数据
    df = pd.read_excel(excel_path)

    # 从item_name列读取商品名称到item_name变量
    item_name = df["item_name"].tolist()

    # 从img_head列读取图片链接到url变量
    url = df["img_head"].tolist()

    cate_name_list = []
    brand_name_list = []
    pipeline_brand = GridVlpClassificationPipeline('rgtjf1/multi-modal_gridvlp_classification_chinese-base-ecom-brand')

    pipeline_cate = GridVlpClassificationPipeline(
        'rgtjf1/multi-modal_gridvlp_classification_chinese-base-ecom-cate-large')

    """
    ##test
    output_brand = pipeline_brand(
                    {'text':"小雨越南尾货已过检过验流浪包系列流浪包单肩斜挎手提背包香奶奶流浪背囊小号双肩包双肩链条包女包小书包",
                     'image':"https://si.geilicdn.com/open1777114774-1234478995-14b4000001879f7c63780a219249_1080_1080.jpg"
                    })
    print(output_brand['text'][0]['label'])
    output_cate = pipeline_cate(
                    {'text':"小雨越南尾货已过检过验流浪包系列流浪包单肩斜挎手提背包香奶奶流浪背囊小号双肩包双肩链条包女包小书包",
                     'image':"https://si.geilicdn.com/open1777114774-1234478995-14b4000001879f7c63780a219249_1080_1080.jpg"
                    })
    print(output_cate['text'][0]['label']['cate_name'])
    """
    for name, link in zip(item_name, url):
        output_cate = pipeline_cate(
            {'text': name,
             'image': link})
        output_brand = pipeline_brand(
            {'text': name,
             'image': link})

        cate_name_list.append(output_cate['text'][0]['label']['cate_name'])
        brand_name_list.append((output_brand['text'][0]['label']))

    df["预测类目"] = cate_name_list
    df["预测品牌"] = brand_name_list


    df.to_excel(excel_path, index=False)

