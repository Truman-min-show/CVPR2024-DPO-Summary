# 📂 CVPR2024-DPO-Summary

本项目基于2024年CVPR会议的文献数据，构建了一个用于直接偏好优化（DPO）的文本摘要数据集，并提供了完整的数据处理、模型训练和推理代码。项目包含：

- CVPR 2024论文标题和摘要的CSV数据集
- 用于DPO训练的JSON格式数据集
- 基于mT5模型的DPO训练、评估和推理代码
- 数据清洗、预处理和生成工具

适合用于研究DPO方法在摘要生成任务中的应用，以及探索如何利用学术会议文献数据提升语言模型性能。

## 📜 数据集说明

数据集包含两部分：

1. **CSV 文件**（完整数据）
   - 2024年CVPR会议所有论文（约1400篇）的：
     - `title`（标题）
     - `abstract`（摘要）
     - `introduction`（引文介绍）

2. **JSON 文件**（DPO训练数据）
   - 用于偏好优化（DPO）任务，共200条数据：
     - `prompt`：论文摘要
     - `chosen`：高评分优质摘要
     - `rejected`：低评分摘要

## 📊 数据示例

### 📄 CSV数据（arxiv_data.csv）

![image](https://github.com/user-attachments/assets/6fd5d726-6fe4-430d-bf3f-0d5783618728)

👉 [查看完整CSV数据](./data/arxiv_data.csv)

### 📜 JSON数据（2024_CVPR_DPO.json）

```json
[
    {
        "prompt": "summary: Efficient generation of 3D digital humans is important\nin several industries...",
        "chosen": "Gaussian Shell Maps (GSMs) are introduced to enhance 3D human generation efficiency...",
        "rejected": "Efficient generation of 3D digital humans using Gaussian Shell Maps that ..."
    },
    {
        "prompt": "summary: Quantifying the degree of similarity between images is a\nkey copyright issue for image-based machine learning..."
        "chosen": "A novel method called Complexity-Constrained Descriptive Autoencoding (CC:DAE) is proposed to define...",
        "rejected": "This work introduces a method to quantify 'conceptual similarity' among images by generating ..."
    }
]
```

👉 [查看完整JSON数据](./data/cleaned_DPO.json)

## 🚀 项目功能

本项目不仅提供了丰富的数据集，还包含了基于DPO方法对mT5模型进行训练和推理的完整流程，具体功能如下：

### 📚 数据处理

- `clean_data.py`：对原始数据进行清洗，去除不必要的内容，如代码片段等。
- `get_json.py`：将CSV文件转换为DPO训练所需的JSON格式，其中`chosen`和`rejected`字段为空，供后续填充。
- `get_txt.py`：将CSV文件中的每10行数据分别生成一个内容为摘要的TXT文件和一个内容为标题的TXT文件，便于数据的分块处理和分析。
- `process_data.py`：利用mT5模型生成`rejected`摘要，并将数据划分为训练集和测试集，最终生成完整的DPO训练数据集。

### 🧠 模型训练与评估

- `train.py`：基于DPO方法对mT5模型进行训练，配置了训练参数如批量大小、学习率、训练轮数等，并在训练过程中保存模型。
- `evaluate.py`：评估模型在测试集上的表现，计算ROUGE指标，包括ROUGE-1和ROUGE-L，以衡量生成摘要的质量。
- `inference.py`：加载训练好的模型，对输入文本进行摘要生成，支持自定义文本的摘要提取。

### 📖 配置管理

- `config.py`：集中管理项目中的各种配置参数，包括模型名称、数据集路径、训练参数等，方便统一管理和调整。

## 💻 环境配置

### 📋 安装依赖

项目依赖于以下Python库，可在项目根目录下运行以下命令安装：

```bash
pip install -r requirements.txt
```

### 📜 依赖列表

- `transformers~=4.49.0`：用于加载和使用Hugging Face的预训练模型。
- `trl~=0.15.2`：提供了DPO训练器等工具，便于实现Direct Preference Optimization训练。
- `numpy~=1.26.4`：用于数值计算和数组操作。
- `rouge-score~=0.1.2`：用于计算ROUGE指标，评估生成摘要的质量。
- `datasets~=3.3.2`：提供了数据集加载和处理的功能。
- `tqdm~=4.66.5`：用于显示进度条，方便跟踪长时间运行的任务进度。

## 📖 使用指南

### 📑 数据准备

1. 将CVPR 2024的文献数据整理成CSV格式，包含`title`、`abstract`、`introduction`等字段。
2. 将CSV文件放置在`data`目录下，命名为`arxiv_data.csv`。

### 🛠️ 数据处理

运行以下脚本对数据进行处理：

1. **生成空JSON数据**：运行`get_json.py`，将CSV文件转换为DPO训练所需的空JSON格式文件。
2. **生成TXT文件**：运行`get_txt.py`，将CSV文件中的每10行数据分别生成摘要和标题的TXT文件，便于后续处理。
3. **填充rejected摘要并划分数据集**：运行`process_data.py`，利用mT5模型生成rejected摘要，并将数据划分为训练集和测试集，最终生成完整的DPO训练数据集。

### 🚂 模型训练

在完成数据处理后，运行`train.py`进行模型训练。脚本会自动加载配置参数、初始化训练器，并在训练过程中保存模型。训练完成后，模型将保存在`./dpo_final_model`目录下。

### 🧪 模型评估

训练完成后，运行`evaluate.py`评估模型在测试集上的表现。脚本会计算并输出ROUGE-1和ROUGE-L指标，帮助了解模型生成摘要的质量。

### 📝 模型推理

加载训练好的模型，对输入文本进行摘要生成。可以在`inference.py`中修改`example_text`变量的值，替换为自定义的文本内容，然后运行脚本，查看生成的摘要结果。

## 🔍 使用方式

- **数据分析**：本项目的数据集可用于NLP任务、文献分析等研究，帮助研究人员了解CVPR 2024会议的论文分布和研究热点。
- **DPO训练**：提供了完整的DPO训练流程和代码实现，研究者可以基于此数据集和代码框架，进一步探索和优化文本摘要生成模型。
- **机器学习**：项目中的代码和模型可结合其他LLM进行研究，为自然语言处理领域的相关任务提供参考和基础。
## 协作者

- [tzhm5577](https://github.com/tzhm5577)
- [wangxinyue-maomi](https://github.com/wangxinyue-maomi)
- [dzwdzwd1](https://github.com/dzwdzwd1)
- [ChenMing_Li]

📢 **欢迎Star ⭐ 和 Fork 🍴！** 如果您在使用过程中有任何问题或建议，欢迎随时提出，我们会尽力为您解答和改进！
