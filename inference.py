
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import torch,random
import load_dataset,evaluate

# ================= 配置参数 =================
MODEL_PATH = "./dpo_final_model"  # 训练后保存的模型路径
MAX_INPUT_LENGTH = 512  # 输入文本最大长度
MAX_GENERATION_LENGTH = 150  # 生成摘要最大长度
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"  # 自动选择设备
DATASET_PATH = "data/cleaned_DPO.json"  # 新数据路径
TEST_SIZE = 0.2  # 测试集比例
LENGTH_PENALTY=1.7
# ================= 加载模型和分词器 =================
def load_model():
    # 加载分词器
    tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)

    # 加载模型
    model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_PATH).to(DEVICE)
    model.eval()  # 设置为评估模式

    return tokenizer, model

# ================= 生成摘要 =================
def generate_summary(text, tokenizer, model):
    # 文本预处理
    inputs = tokenizer(
        f"summary: {text}",  # 保持与训练时相同的prompt格式
        return_tensors="pt",
        max_length=MAX_INPUT_LENGTH,
        truncation=True
    ).to(DEVICE)

    # 生成摘要
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_length=MAX_GENERATION_LENGTH,
            num_beams=4,  # 束搜索参数
            length_penalty=LENGTH_PENALTY,  # 长度惩罚系数（>1鼓励更长，<1鼓励更短）
            no_repeat_ngram_size=2,  # 禁止2-gram重复
            early_stopping=True  # 提前停止生成
        )

    # 解码生成结果
    summary = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return summary

# ================= 使用示例 =================
if __name__ == "__main__":
    # 加载模型
    tokenizer, model = load_model()
    print("模型加载成功！设备：", DEVICE)


    dataset = load_dataset.load_and_split_data()
    print("已生成随机测试数据集")

    print("评估测试集表现...")
    test_data = dataset["test"]
    metrics = evaluate.evaluate_model(model, tokenizer, test_data)

    # 打印评估结果
    print(f"\n评估结果：")
    print(f"ROUGE-1: {metrics['rouge1'] * 100:.2f}%")
    print(f"ROUGE-L: {metrics['rougeL'] * 100:.2f}%")

    # 示例输入
    example_text = """ 
    Leveraging Vision-Language Models for Improving Domain Generalization in Image Classification:
    Vision-Language Models (VLMs) such as CLIP are trained on large amounts of image-text pairs, resulting in remarkable generalization across several data distributions. However, in several cases, their expensive training and data collection/curation costs do not justify the end application. This motivates a vendor-client paradigm, where a vendor trains a large-scale VLM and grants only input-output access to clients on a pay-per-query basis in a black-box setting. The client aims to minimize inference cost by distilling the VLM to a student model using the limited available task-specific data, and further deploying this student model in the downstream application. While naive distillation largely improves the In-Domain (ID) accuracy of the student, it fails to transfer the superior out-of-distribution (OOD) generalization of the VLM teacher using the limited available labeled images. To mitigate this, we propose Vision-Language to Vision - Align, Distill, Predict (VL2V-ADiP), which first aligns the vision and language modalities of the teacher model with the vision modality of a pre-trained student model, and further distills the aligned VLM representations to the student. This maximally retains the pre-trained features of the student, while also incorporating the rich representations of the VLM image encoder and the superior generalization of the text embeddings. The proposed approach achieves state-of-the-art results on the standard Domain Generalization benchmarks in a black-box teacher setting as well as a white-box setting where the weights of the VLM are accessible.
    """

    # 生成摘要
    summary = generate_summary(example_text, tokenizer, model)

    print("生成摘要：")
    print(summary)
    print("样例摘要：")
    print("VL2V-ADiP is introduced to improve domain generalization in image classification by leveraging Vision-Language Models (VLMs). This method first aligns the vision and language modalities of a VLM teacher with a pre-trained student model's vision modality, then distills the aligned VLM representations to the student. This approach retains the student's pre-trained features while incorporating the rich representations of the VLM image encoder and superior generalization of text embeddings. VL2V-ADiP achieves state-of-the-art results on standard Domain Generalization benchmarks in both black-box and white-box teacher settings.")