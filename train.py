
import transformers
import transformers.models
from transformers import BertJapaneseTokenizer
import datasets
from datasets import Dataset


model_id = "cl-tohoku/bert-base-japanese-v3"
tokenizer = transformers.models.bert_japanese.BertJapaneseTokenizer.from_pretrained(model_id)
model = transformers.models.bert.BertForPreTraining.from_pretrained(model_id)

# 1. Transformers用のデータセット形式に変換
# pandas.DataFrame -> datasets.Dataset
target_columns = ['Sentence', 'readers_emotion_intensities']
train_dataset = Dataset.from_pandas(df_train[target_columns])
test_dataset = Dataset.from_pandas(df_test[target_columns])

# 2. Tokenizerを適用（モデル入力のための前処理）
def tokenize_function(batch):
    """Tokenizerを適用 （感情強度の正規化も同時に実施する）."""
    tokenized_batch = tokenizer(batch['Sentence'], truncation=True, padding='max_length')
    tokenized_batch['labels'] = [x / np.sum(x) for x in batch['readers_emotion_intensities']]  # 総和=1に正規化
    return tokenized_batch

train_tokenized_dataset = train_dataset.map(tokenize_function, batched=True)
test_tokenized_dataset = test_dataset.map(tokenize_function, batched=True)

args = transformers.TrainingArguments(
    output_dir="./output",
    num_train_epochs=1.0,
    evaluation_strategy="steps", eval_steps=200
)
transformers.Trainer(
    model=model,
    args = args,
    train_dataset=,
    eval_dataset=
)