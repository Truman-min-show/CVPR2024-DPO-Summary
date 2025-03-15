import csv
import json


def generate_empty_json(input_csv, output_json, max_rows=200):
    """
    将 CSV 文件中的数据转换为一个 JSON 文件，其中 "chosen" 和 "rejected" 字段为空

    参数：
    input_csv: 输入的 CSV 文件路径，包含文献标题和摘要
    output_json: 输出的 JSON 文件路径
    max_rows: 最大处理行数，默认为 200
    """
    data = []

    # 读取 CSV 文件
    with open(input_csv, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)

        # 限制处理行数
        for i, row in enumerate(reader):
            if i >= max_rows:
                break

            # 构造 JSON 数据格式
            json_data = {
                "prompt": f"summary: {row['Abstract']}",
                "chosen": "",
                "rejected": ""
            }
            data.append(json_data)

    # 写入 JSON 文件
    with open(output_json, 'w', encoding='utf-8') as jsonfile:
        json.dump(data, jsonfile, ensure_ascii=False, indent=4)


# 使用示例
generate_empty_json(
    input_csv='./data/arxiv_data.csv',  # 输入的 CSV 文件路径
    output_json='./data/empty_DPO_data.json',  # 输出的 JSON 文件路径
    max_rows=200  # 最大处理行数
)