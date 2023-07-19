from modelscope.models import Model
from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
from PIL import Image
import requests


def load_image(image_path):
    if image_path.startswith("http"):
        # 通过链接获取图像数据
        image = Image.open(requests.get(image_path, stream=True).raw)
    else:
        # 打开本地图像文件
        image = Image.open(image_path)
    return image
def get_embedding(item_names,image_path):
    model = Model.from_pretrained('damo/multi-modal_gemm-vit-large-patch14_generative-multi-modal-embedding')
    p = pipeline(task=Tasks.generative_multi_modal_embedding, model=model)

    image = load_image(image_path)

    text_embedding = p.forward({'text': item_names})['text_embedding']
    img_embedding = p.forward({'image': image})['img_embedding']

    return text_embedding[0],img_embedding[0]

