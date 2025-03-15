# clean_project_pages.py
import json
import re


def remove_project_page(text):
    """删除字符串中'Project Page:'及其之后的所有内容"""
    # 使用正则表达式匹配（不区分大小写）
    pattern = re.compile(r"Code .*", flags=re.IGNORECASE)
    return pattern.split(text)[0].strip()


def process_json_file(input_path, output_path):
    # 读取原始数据
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 处理每个条目
    for item in data:
        original_prompt = item["prompt"]
        cleaned_prompt = remove_project_page(original_prompt)
        item["prompt"] = cleaned_prompt

    # 保存处理后的数据
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    input_file = "../data/cleaned_DPO.json"  # 原始数据路径
    output_file = "../data/cleaned_DPO.json"  # 输出路径

    process_json_file(input_file, output_file)
    print(f"处理完成！已保存至 {output_file}")