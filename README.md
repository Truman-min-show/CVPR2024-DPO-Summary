
# 📂 2024_CVPR_Summary_Dataset  
本项目整理了 2024 年 CVPR 会议的文献标题及摘要数据集，包含所有论文的关键信息，同时构建了一个 DPO（Direct Preference Optimization）数据集，助力学术研究与自然语言处理任务。
## 📜 数据集说明  
数据集包含两部分：  
1. **CSV 文件**（完整数据）  
   - 2024 年 CVPR 会议所有论文（约 1400 篇）的：
     - `title`（标题）
     - `abstract`（摘要）
     - `introduction`（引言）
  
2. **JSON 文件**（DPO 训练数据）  
   - 用于偏好优化（DPO）任务，共 200 条数据：
     - `prompt`：论文摘要
     - `chosen`：基于 Kimi 深度思考得到的优质摘要  
     - `rejected`：基于通义千问生成的较弱摘要  

---

## 📊 数据示例  

### 📄 CSV 数据（2024_CVPR_papers.csv）  

![image](https://github.com/user-attachments/assets/6fd5d726-6fe4-430d-bf3f-0d5783618728)


👉 [查看完整 CSV 数据](./2024_CVPR_papers.csv)  

---

### 📜 JSON 数据（2024_CVPR_DPO.json）  

```json
[
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

👉 [查看完整 JSON 数据](./2024_CVPR_DPO.json)  

---

## 🔍 使用方式  

- **数据分析**：可用于 NLP 任务、文献分析等  
- **DPO 训练**：提升文本摘要生成质量  
- **机器学习**：可结合 LLM 进行研究  

📢 **欢迎 Star ⭐ 和 Fork 🍴！**  

---

这个 README 采用了：
- **表格** 来展示 CSV 结构  
- **JSON 代码块** 展示数据格式  
- **超链接** 指向具体文件，方便下载和查看  

你可以根据实际情况调整表格数据示例的内容，增加详细描述或者图片，使其更直观！ 🚀
