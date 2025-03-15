
# 模型相关配置
MODEL_NAME = "csebuetnlp/mT5_multilingual_XLSum"
DATASET_PATH = "data/cleaned_DPO.json"  # 新数据路径
TEST_SIZE = 0.2  # 测试集比例
OUTPUT_DIR = "./dpo_results"

# 训练相关配置
BATCH_SIZE = 2
GRADIENT_ACCUMULATION_STEPS = 2
LEARNING_RATE = 1e-5
NUM_EPOCHS = 10

# 生成相关配置
MAX_GENERATION_LENGTH = 512  # 生成摘要最大长度