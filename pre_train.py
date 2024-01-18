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
