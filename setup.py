from title_extraction.raner_complete import raner
from title_extraction.predict_brand_class import  GridVLP
from title_extraction.with_spec import with_spec
from embedding_and_classify.embedding import get_embedding
from embedding_and_classify.classify import classify
from embedding_and_classify.view_calsses import view_h
from embedding_and_classify.predict_spec import predict_data
from embedding_and_classify.Manual import addition, delete_item,delete_class

#构建数据库,构建初始数据库和类目的数据集
def construction(path_of_excel):

    outputfile = path_of_excel.rsplit('.', 1)[0] + '_classification.xlsx'
    # 调用函数获取图像和文本的嵌入向量,并构造类目库
    classify(outputfile)

    #将类别保存在class_dict.xlsx中可视化查看
    view_h()

    #人工添加或删除数据
    #添加的商品名称、图片url和要加入的类名称
    new_item_name = ""
    new_image_link = ""
    new_item_class = ""

    #删除的商品名和所在的类目
    class_name = ""
    item_to_remove = ""

    #删除的类目名称
    name_of_class = ""

    addition(new_item_name,new_image_link,new_item_class)
    delete_item(class_name , item_to_remove)
    delete_class(name_of_class)

#对新产品的预测和分类
def predict_new_item(new_item_excel_path):
    # raNER对商品标题进行细颗粒度提取，输出结果到path_of_excel_classification.xlsx中
    raner(new_item_excel_path)

    # GridVLP输出商品的预测品牌和预测类目（brand和class）
    outputfile_of_raner =new_item_excel_path.rsplit('.', 1)[0] + '_classification.xlsx'
    GridVLP(outputfile_of_raner)

    # 通过raner细颗粒度提取给出预测型号和预测命名
    with_spec(outputfile_of_raner)


    