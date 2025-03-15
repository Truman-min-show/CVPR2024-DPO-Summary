import config as cg
import numpy as np
from rouge_score import rouge_scorer

# ================= 评估函数 =================
def evaluate_model(model, tokenizer, test_data):
    """评估模型并返回ROUGE指标"""
    model.eval()
    scorer = rouge_scorer.RougeScorer(['rouge1', 'rougeL'], use_stemmer=True)
    rouge_scores = []

    for sample in test_data:
        # 生成摘要
        inputs = tokenizer(
            sample["prompt"],
            return_tensors="pt",
            max_length=512,
            truncation=True
        ).to(model.device)

        outputs = model.generate(
            **inputs,
            max_length=cg.MAX_GENERATION_LENGTH,
            num_beams=4,  # 启用束搜索
            length_penalty=1.6,  # 惩罚过短生成
            no_repeat_ngram_size=2  # 避免重复n-gram
        )

        generated_summary = tokenizer.decode(outputs[0], skip_special_tokens=True)

        # 计算ROUGE分数
        score = scorer.score(
            sample["chosen"],
            generated_summary
        )

        rouge_scores.append({
            "rouge1": score["rouge1"].fmeasure,
            "rougeL": score["rougeL"].fmeasure
        })

    # 计算平均指标
    avg_rouge1 = np.mean([s["rouge1"] for s in rouge_scores])
    avg_rougeL = np.mean([s["rougeL"] for s in rouge_scores])

    return {
        "rouge1": round(avg_rouge1, 4),
        "rougeL": round(avg_rougeL, 4)
    }