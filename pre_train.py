# 前処理 感情の低いサンプルを除外して整形
import datasets
filename = "./wrime-ver1.tsv"
# d = datasets.Dataset.from_file(filename="wrime-ver1.tsv", split="\t")
# print(d)
# d = datasets.load_dataset(path=filename, split="\t")
dataset = datasets.load_dataset('csv', data_files=filename, delimiter='\t', quotechar='"')
print(dataset)
# print(d)

import pandas as pd
df_wrime = pd.read_table(filename)
df_wrime.info()
emotion_names = ['Joy', 'Sadness', 'Anticipation', 'Surprise', 'Anger', "Fear", "Disgust", "Trust"]
df_wrime['readers_emotion_intensities'] = df_wrime.apply(lambda x: [x['Avg. Readers_' + name] for name in emotion_names], axis=1)

# 感情強度が低いサンプルは除外する
# (readers_emotion_intensities の max が２以上のサンプルのみを対象とする)
is_target = df_wrime['readers_emotion_intensities'].map(lambda x: max(x) >= 2)
df_wrime_target = df_wrime[is_target]

# train / test に分割する
df_groups = df_wrime_target.groupby('Train/Dev/Test')
df_train = df_groups.get_group('train')
df_test = pd.concat([df_groups.get_group('dev'), df_groups.get_group('test')])
print('train :', len(df_train))  # train : 17104
print('test :', len(df_test))    # test : 1133

from transformers import AutoTokenizer, AutoModelForSequenceClassification, BertJapaneseTokenizer, MecabTokenizer
import transformers
import transformers.models

# 使用するモデルを指定して、トークナイザとモデルを読み込む
checkpoint = 'cl-tohoku/bert-base-japanese-whole-word-masking'
checkpoint2 = "cl-tohoku/bert-base-japanese-v3"
tokenizer = transformers.models.bert_japanese.BertJapaneseTokenizer.from_pretrained(checkpoint2)
model = transformers.models.bert.BertForPreTraining.from_pretrained(checkpoint, num_labels=8)



# # BERTはサブワードを含めて最大512単語まで扱える
# MAX_LENGTH = 512
# def bert_tokenizer(text):
#     return tokenizer.encode(text, max_length=MAX_LENGTH, truncation=True, return_tensors='pt')[0]


encs = tokenizer.encode_plus(
    "本日はお日柄も良く…なのです。",
    return_tensors="pt",
    add_special_tokens=False,
)

print(encs["input_ids"])

# outs = model.generate(
#     inputs=encs["input_ids"],
#     do_sample=True,
#     top_k=0,
#     top_p=0.9,
#     max_length=128,
# )

# txt = tokenizer.decode(outs[0])

target_columns = ['Sentence', 'readers_emotion_intensities']
train_dataset = datasets.Dataset.from_pandas(df_train[target_columns])
test_dataset = datasets.Dataset.from_pandas(df_test[target_columns])
import numpy as np


def tokenize_function(batch):
    """Tokenizerを適用 （感情強度の正規化も同時に実施する）."""
    tokenized_batch = tokenizer.encode_plus(batch['Sentence'], truncation=True, padding='max_length')
    tokenized_batch['labels'] = [x / np.sum(x) for x in batch['readers_emotion_intensities']]  # 総和=1に正規化
    return tokenized_batch


train_tokenized_dataset = train_dataset.map(tokenize_function, batched=True)
test_tokenized_dataset = test_dataset.map(tokenize_function, batched=True)

