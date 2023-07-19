# 商品识别与分类

## 流程

### 一.使用标注好的数据构造数据库和类目数据集（setup.construction）
1. 对于图像和商品标题结合的数据，使用GEMM生成式多模态表征模型进行标题和图像的嵌入向量embedding值的提取和分析。
    1. 视觉encoder采用vit-large-patch14结构，生成text_embedding![16897535979080](https://github.com/hetonghui02/spec_classification/assets/36235543/d20c8626-5498-4918-8e6f-bb54a11cc092)


    2. 文本encoder采用bert-base结构，生成image_embedding![](assets/16897536186855.jpg)

    3. 对已经标注好brand_spec_class的数据，将brand_spec_class相同的商品归于一个类目，类目名为“brand_spec_class”，聚类中心的文本和图像向量由类目内所有产品的文本、图像向量计算平均得到。
2. 将生成的模型保存到class_pred.pkl中，模型中保存着每个类目的类目名称、类目中的商品名和对应的文本、图像向量，以及类目整体的向量。
3. 可通过view—h,将模型保存到对应的excel文件中，方便查看。![](assets/16897532628655.jpg)

4.   可通过Manual.addition,delete_class,delete_item方式进行手动添加和删除类目或商品名称。

### 二.预测和迭代
1. 对于未标注的数据，如只有商品标题和商品图片的数据，对商品标题进行细颗粒度分词和实体识别。采用基于Transformer-CRF的RaNER模型，使用StructBERT作为预训练模型底座，使用Multi-view Training方式进行训练。![](assets/16897536717438.jpg)
![](assets/16897537046698.jpg)

1. 分词和识别标题后，使用基于Bert+Resnet50模型，使用StructBERT作为预训练模型底座的GridVLP多模态类目预测和品牌预测模型，生成预测品牌和预测类目。![](assets/16897541329755.jpg)

2. 对预测商品标题和商品图片使用GEMM模型进行提取文本和图片向量，并和生成的类目做相似度比较，分别计算文本和图片相似度，并设置权重令二者乘以权重后相加，为图片后类目的最终相似度。

3. 如果图像与类的相似度大于90%，则将新数据加入到该类中，并更新类别的平均向量，并且输出最高的前三个文本相似度、图像相似度和总体相似度供参考。 ![](assets/16897550529937.jpg)

4. 每次加入新的商品后都会更新模型并保存。

### 验证集上的准确率：
![](assets/16897551589921.jpg)


