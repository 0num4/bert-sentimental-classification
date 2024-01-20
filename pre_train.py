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

# 使用するモデルを指定して、トークナイザとモデルを読み込む
checkpoint = 'cl-tohoku/bert-base-japanese-whole-word-masking'
checkpoint2 = "cl-tohoku/bert-base-japanese-v3"
tokenizer = AutoTokenizer.from_pretrained(checkpoint2)
model = AutoModelForSequenceClassification.from_pretrained(checkpoint, num_labels=8)