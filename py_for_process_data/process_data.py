import json
import csv
import random
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import torch
from tqdm import tqdm

# 加载 mT5 模型和分词器
model_name = "csebuetnlp/mT5_multilingual_XLSum"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)


def generate_rejected_abstract(abstract):
    """
    使用 mT5 模型生成 rejected 摘要

    参数：
    abstract: 原始摘要

    返回：
    rejected_abstract: 生成的 rejected 摘要
    """
    # 对输入摘要进行编码
    inputs = tokenizer.encode("summarize: " + abstract, return_tensors="pt", max_length=512, truncation=True)

    # 生成摘要
    outputs = model.generate(
        inputs,
        max_length=150,
        min_length=50,
        num_beams=4,
        early_stopping=True,
        temperature=0.7,
        top_p=0.9,
        no_repeat_ngram_size=2
    )

    # 解码生成的摘要
    rejected_abstract = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return rejected_abstract


def process_arxiv_data(input_csv, output_train_json, output_test_json, test_ratio=0.2, max_rows=200):
    """
    将 Arxiv 文献数据转换为 DPO 训练格式的 JSON 数据集，并生成 rejected 摘要

    参数：
    input_csv: 输入的 CSV 文件路径，包含文献标题和摘要
    output_train_json: 输出的训练集 JSON 文件路径
    output_test_json: 输出的测试集 JSON 文件路径
    test_ratio: 测试集所占比例，默认为 0.2
    max_rows: 最大处理行数，默认为 200
    """
    # 读取 CSV 文件
    with open(input_csv, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        total_rows = min(sum(1 for row in reader), max_rows)
        csvfile.seek(0)
        next(reader)  # 跳过表头

        # 初始化进度条
        progress_bar = tqdm(total=total_rows, desc="Processing rows")

        # 打开输出文件
        with open(output_train_json, 'w', encoding='utf-8') as train_file, \
                open(output_test_json, 'w', encoding='utf-8') as test_file:

            train_file.write("[\n")
            test_file.write("[\n")

            for i, row in enumerate(reader):
                if i >= max_rows:
                    break

                title = row['Folder Name'].replace('_', ' ')  # 去除下划线并替换为空格
                abstract = row['Abstract']

                # 构造 DPO 格式的数据
                chosen_abstract = title
                rejected_abstract = generate_rejected_abstract(abstract)

                dpo_data = {
                    "prompt": f"summary: {abstract}",
                    "chosen": chosen_abstract,
                    "rejected": rejected_abstract
                }

                # 随机决定是否加入测试集
                if random.random() < test_ratio:
                    # 写入测试集文件
                    json.dump(dpo_data, test_file, ensure_ascii=False, indent=4)
                    if i != total_rows - 1:
                        test_file.write(",\n")
                else:
                    # 写入训练集文件
                    json.dump(dpo_data, train_file, ensure_ascii=False, indent=4)
                    if i != total_rows - 1:
                        train_file.write(",\n")

                progress_bar.update(1)

            # 关闭进度条
            progress_bar.close()

            # 写入结尾的 ]
            train_file.write("\n]")
            test_file.write("\n]")


# 使用示例
process_arxiv_data(
    input_csv='./data/arxiv_data.csv',  # 输入的 CSV 文件路径
    output_train_json='./data/DPO_train_data.json',  # 输出的训练集 JSON 文件路径
    output_test_json='./data/DPO_test_data.json',  # 输出的测试集 JSON 文件路径
    test_ratio=0.2,  # 测试集所占比例
    max_rows=200  # 最大处理行数
)