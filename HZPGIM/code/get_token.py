# -*- coding: utf-8 -*-

from transformers import XLMRobertaTokenizer

# 尝试强制重新下载模型
tokenizer = XLMRobertaTokenizer.from_pretrained('xlm-roberta-large', force_download=True)


# 你的文本
text = "明打假人举报花西子虚假宣传称啊花西子应该给消费者退一赔三起步价。 2MG  分析：在这段文本中，花西子被提及为产品品牌，因此标注为“PRODUCT_BRAND”。退一赔三是一个涉及赔偿金额的短语，通常指消费者保护法中的赔偿原则，这里标注为“AMOUNT”。2MG在文本中看起来像是一个产品名称或型号，因此标注为“PRODUCT_NAME”。图像描述显示的是一个女人拿着牙刷，这与文本中提到的花西子产品没有直接关联。"

# 使用分词器分词
tokens = tokenizer.tokenize(text)

# 检查分词后的长度
print("Token count:", len(tokens))
