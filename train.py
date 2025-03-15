from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from trl import DPOTrainer, DPOConfig
import load_dataset
import config as cg
import evaluate



# ================= 主流程 =================
if __name__ == "__main__":
    # 加载模型和分词器
    tokenizer = AutoTokenizer.from_pretrained(cg.MODEL_NAME)
    model = AutoModelForSeq2SeqLM.from_pretrained(cg.MODEL_NAME)

    # 加载并分割数据
    dataset = load_dataset.load_and_split_data()

    # 配置DPO训练参数
    training_args = DPOConfig(
        output_dir=cg.OUTPUT_DIR,
        per_device_train_batch_size=cg.BATCH_SIZE,
        gradient_accumulation_steps=cg.GRADIENT_ACCUMULATION_STEPS,
        learning_rate=cg.LEARNING_RATE,
        num_train_epochs=cg.NUM_EPOCHS,
        logging_steps=10,
        save_steps=500,
        fp16=True,
        remove_unused_columns=False
    )

    # 初始化DPO训练器
    dpo_trainer = DPOTrainer(
        model=model,
        ref_model=None,
        args=training_args,
        train_dataset=dataset["train"],
        tokenizer=tokenizer,
    )

    # 执行训练
    print("开始训练...")
    dpo_trainer.train()



    # 评估测试集表现
    print("\n评估测试集表现...")
    test_data = dataset["test"]
    metrics = evaluate.evaluate_model(model, tokenizer, test_data)

    # 打印评估结果
    print(f"\n评估结果：")
    print(f"ROUGE-1: {metrics['rouge1'] * 100:.2f}%")
    print(f"ROUGE-L: {metrics['rougeL'] * 100:.2f}%")

    # 保存最终模型
    dpo_trainer.save_model("./dpo_final_model")