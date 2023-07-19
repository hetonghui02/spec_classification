from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
import pandas as pd


def raner(excel_path):
    df = pd.read_excel(excel_path)

    item_name = df["item_name"].tolist()
    img_names = df['img_head'].tolist()

    brand_name_list = []  # 品牌
    model_name_list = []  # 款式
    category_name_list = []  # 产品
    series_name_list = []  # 系列
    effectivity_name_list = []  # 功能功效
    description_name_list = []  # 修饰
    place_of_origin_list = []  # 原产地
    other_place_list = []  # 其他地区相关
    size_list = []  # 尺寸规格
    material_list = []  # 材质
    range_list = []  # 适用范围
    color_list = []  # 颜色
    style_list = []  # 风格

    ner_pipeline = pipeline(Tasks.named_entity_recognition,
                            'damo/nlp_raner_named-entity-recognition_chinese-base-ecom-50cls')

    for name in item_name:
        result = ner_pipeline(name)
        output = result['output']
        brand_spans = list(set([item['span'] for item in output if item['type'] == '品牌']))
        model_spans = list(set([item['span'] for item in output if
                                item['type'] == '款式_其他' or item['type'] == '款式_厚薄' or item['type'] == '款式_袖型'
                                or item['type'] == '款式_裙型' or item['type'] == '款式_裤型' or item['type'] == '款式_领型'
                                or item['type'] == '款式_鞋型']))
        category_spans = list(set([item['span'] for item in output if
                                   item['type'] == '产品_核心产品' or item['type'] == '产品_修饰产品' or item[
                                       'type'] == '产品_其他']))
        series_spans = list(set([item['span'] for item in output if item['type'] == '系列']))
        effectivity_spans = list(set([item['span'] for item in output if item['type'] == '功能功效']))
        description_spans = list(
            set([item['span'] for item in output if item['type'] == '修饰_产品属性' or item['type'] == '修饰_其他'
                 or item['type'] == '修饰_口味' or item['type'] == '修饰_外观描述' or item['type'] == '修饰_工作方式'
                 or item['type'] == '修饰_评价体验']))
        place_of_origin_spans = list(set([item['span'] for item in output if item['type'] == '地点地域_产地']))
        other_place_spans = list(
            set([item['span'] for item in output if item['type'] == '地点地域_其他' or item['type'] == '地点地域_发货地'
                 or item['type'] == '地点地域_商标产地' or item['type'] == '地点地域_适用地区']))
        size_spans = list(
            set([item['span'] for item in output if item['type'] == '尺寸规格_其他' or item['type'] == '尺寸规格_售卖规格'
                 or item['type'] == '尺寸规格_外观尺寸' or item['type'] == '尺寸规格_指标参数'
                 or item['type'] == '尺寸规格_重量']))
        material_spans = list(
            set(item['span'] for item in output if item['type'] == '材质_其他' or item['type'] == '材质_木质材质'
                or item['type'] == '材质_金属材质'))
        range_spans = list(
            set([item['span'] for item in output if item['type'] == '适用范围_其他' or item['type'] == '适用范围_适用人群'
                 or item['type'] == '适用范围_适用场景' or item['type'] == '适用范围_适用季节'
                 or item['type'] == '适用范围_适用对象']))
        color_spans = list(
            set([item['span'] for item in output if item['type'] == '颜色_其他' or item['type'] == '颜色_色彩'
                 or item['type'] == '颜色_配色方案']))
        style_spans = list(set(item['span'] for item in output if item['type'] == '风格'))

        brand_name_list.append(brand_spans)
        model_name_list.append(model_spans)
        category_name_list.append(category_spans)
        series_name_list.append(series_spans)
        effectivity_name_list.append(effectivity_spans)
        description_name_list.append(description_spans)
        place_of_origin_list.append(place_of_origin_spans)
        other_place_list.append(other_place_spans)
        size_list.append(size_spans)
        material_list.append(material_spans)
        range_list.append(range_spans)
        color_list.append(color_spans)
        style_list.append(style_spans)

    df["品牌"] = brand_name_list
    df["款式"] = model_name_list
    df["产品"] = category_name_list
    df["系列"] = series_name_list
    df["功能功效"] = effectivity_name_list
    df["修饰"] = description_name_list
    df["原产地"] = place_of_origin_list
    df["其他地点"] = other_place_list
    df["尺寸规格"] = size_list
    df["材质"] = material_list
    df["适用范围"] = range_list
    df["颜色"] = color_list
    df["风格"] = style_list
    df['图片'] = img_names
    output_file = excel_path.rsplit('.', 1)[0] + '_classification.xlsx'
    df.to_excel(output_file, index=False)

    '''
    result = ner_pipeline('【只做原鞋 自家工厂】AJ1 AJ1dunk dunk sb  dunksb 冰雪奇缘 情人节 影子灰 鸽子粉 黑白熊猫 白绿 酒红 复古蓝 芝加哥 北卡蓝 骨白 白紫 绿 白棕 海军')
    output = result['output']
    brand_spans = list(set([item['span'] for item in output if item['type'] == '品牌']))
    model_spans = list(set([item['span'] for item in output if item['type'] == '款式_其他' or item['type'] == '款式_厚薄' or item['type'] == '款式_袖型'
                                or item['type'] == '款式_裙型' or item['type'] == '款式_裤型' or item['type'] == '款式_领型'
                                or item['type'] == '款式_鞋型']  ))
    category_spans = list(set([item['span'] for item in output if item['type'] == '产品_核心产品' or item['type'] == '产品_修饰产品' or item['type'] == '产品_其他']))
    series_spans = list(set([item['span'] for item in output if item['type'] == '系列']))
    effectivity_spans = list(set([item['span'] for item in output if item['type'] == '功能功效']))
    description_spans = list(set([item['span'] for item in output if item['type'] == '修饰_产品属性' or item['type'] == '修饰_其他'
                                      or item['type'] == '修饰_口味' or item['type'] == '修饰_外观描述' or item['type'] == '修饰_工作方式'
                                      or item['type'] == '修饰_评价体验' ]))
    place_of_origin_spans = list(set([item['span'] for item in output if item['type'] == '地点地域_产地']))
    other_place_spans = list(set([item['span'] for item in output if item['type'] == '地点地域_其他' or item['type'] == '地点地域_发货地'
                                      or item['type'] == '地点地域_商标产地' or item['type'] == '地点地域_适用地区']))
    size_spans = list(set([item['span'] for item in output if item['type'] == '尺寸规格_其他' or item['type'] == '尺寸规格_售卖规格'
                               or item['type'] == '尺寸规格_外观尺寸' or item['type'] == '尺寸规格_指标参数'
                               or item['type'] == '尺寸规格_重量']))
    material_spans = list(set(item['span'] for item in output if item['type'] == '材质_其他' or item['type'] == '材质_木质材质'
                                  or item['type'] == '材质_金属材质'))
    range_spans = list(set([item['span'] for item in output if item['type'] == '适用范围_其他' or item['type'] == '适用范围_适用人群'
                                or item['type'] == '适用范围_适用场景' or item['type'] == '适用范围_适用季节'
                                or item['type'] == '适用范围_适用对象']))
    color_spans = list(set([item['span'] for item in output if item['type'] == '颜色_其他' or item['type'] == '颜色_色彩'
                                or item['type'] == '颜色_配色方案']))
    style_spans = list(set(item['span'] for item in output if item['type'] == '风格'))
    print("品牌",brand_spans)
    print("款式",model_spans)
    print("产品",category_spans)
    print("系列" , series_spans)
    print("功能功效",effectivity_spans)
    print("修饰",description_spans)
    print("原产地",place_of_origin_spans)
    print("其他地址",other_place_spans)
    print("尺寸规格",size_spans)
    print("材质",material_spans)
    print("适用范围",range_spans)
    print("颜色",color_spans)
    print("风格",style_spans)
    '''