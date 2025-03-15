import csv
import os


def generate_txt_files(input_csv, output_dir, max_rows=200, rows_per_file=10):
    """
    将 CSV 文件中的每 10 行数据分别生成一个内容为摘要的 TXT 文件和一个内容为标题的 TXT 文件

    参数：
    input_csv: 输入的 CSV 文件路径，包含文献标题和摘要
    output_dir: 输出的 TXT 文件存储目录
    max_rows: 最大处理行数，默认为 200
    rows_per_file: 每个文件包含的行数，默认为 10
    """
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)

    # 读取 CSV 文件
    with open(input_csv, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)

        # 限制处理行数
        limited_rows = []
        for i, row in enumerate(reader):
            if i >= max_rows:
                break
            limited_rows.append(row)

        # 按每 10 行分组
        for i in range(0, len(limited_rows), rows_per_file):
            group = limited_rows[i:i + rows_per_file]

            # 准备文件名
            start_index = i + 1
            end_index = i + len(group)
            abstracts_filename = f"abstracts_{start_index}-{end_index}.txt"
            titles_filename = f"titles_{start_index}-{end_index}.txt"
            abstracts_path = os.path.join(output_dir, abstracts_filename)
            titles_path = os.path.join(output_dir, titles_filename)

            # 写入摘要文件
            with open(abstracts_path, 'w', encoding='utf-8') as abstracts_file:
                for row in group:
                    abstracts_file.write(row['Abstract'] + '\n')

            # 写入标题文件
            with open(titles_path, 'w', encoding='utf-8') as titles_file:
                for row in group:
                    title = row['Folder Name'].replace('_', ' ')  # 去除下划线并替换为空格
                    titles_file.write(title + '\n')


# 使用示例
generate_txt_files(
    input_csv='./data/arxiv_data.csv',  # 输入的 CSV 文件路径
    output_dir='../txt_files',  # 输出的 TXT 文件存储目录
    max_rows=200,  # 最大处理行数
    rows_per_file=10  # 每个文件包含的行数
)