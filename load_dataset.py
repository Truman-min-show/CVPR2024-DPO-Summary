from datasets import load_dataset, DatasetDict

# ================= 配置参数 =================
MODEL_NAME = "csebuetnlp/mT5_multilingual_XLSum"
DATASET_PATH = "data/cleaned_DPO.json"  # 新数据路径
TEST_SIZE = 0.2  # 测试集比例
OUTPUT_DIR = "./dpo_results"
BATCH_SIZE = 2
GRADIENT_ACCUMULATION_STEPS = 2
LEARNING_RATE = 1e-5
NUM_EPOCHS = 10
MAX_GENERATION_LENGTH = 512  # 生成摘要最大长度


# ================= 加载并分割数据集 =================
def load_and_split_data():
    # 加载完整数据集
    dataset = load_dataset("json", data_files=DATASET_PATH)["train"]

    # 分割为训练集和测试集
    split_dataset = dataset.train_test_split(
        test_size=TEST_SIZE,
        shuffle=True,
        seed=42
    )

    return DatasetDict({
        "train": split_dataset["train"],
        "test": split_dataset["test"]
    })


