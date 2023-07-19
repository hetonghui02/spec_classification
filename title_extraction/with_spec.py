import pandas as pd
import re

def with_spec(excel_path):
   # 读取 Excel 文件
   df = pd.read_excel(excel_path)

   # 将缺失值替换为空字符串
   df.fillna('', inplace=True)

   # 生成新的 spec 列
   df['预测型号'] = df['款式'] + df['系列'] + df['功能功效'] + df['修饰'] + df['尺寸规格'] + df['颜色'] + df['风格'] + df[
      '适用范围']
   df['命名'] = df['预测品牌'] + df['预测型号'] + df['预测类目']

   # 删除除了数字、汉字和字母以外的符号
   df['预测型号' \
      ''] = df['型号'].apply(lambda x: re.sub(r'[^\w\u4e00-\u9fa5]', '', x))

   df['命名' \
      ''] = df['命名'].apply(lambda x: re.sub(r'[^\w\u4e00-\u9fa5]', '', x))

   # 遍历每个单元格，并进行处理
   for col in df.columns:
      for i, cell in enumerate(df[col]):
         if isinstance(cell, str):
            # 删除方括号、单引号和逗号
            cell = re.sub(r'[\[\]\',]', '', cell)

            # 更新单元格的值
            df.at[i, col] = cell
   df.to_excel(excel_path, index=False)
