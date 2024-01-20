# bertかclipで感情分類
https://qiita.com/izaki_shin/items/2b4573ee7fbea5ec8ed6

## モチベーション
何となくやりたくなったから。あとbertの勉強。

## やりたいこと
* 怒りや憎しみなどの感情を分類するタスク

## ref
https://qiita.com/hima2b4/items/7694e2922707b456ecd1

## memo
text-classification taskのjapanで絞った結果
https://huggingface.co/datasets?task_ids=task_ids:multi-class-classification&language=language:ja&sort=trending

日本語の感情分類タスクで有名そうなデータセット
https://github.com/ids-cv/wrime

## 日本語tokenizer系
なんだろう。。。懐かしさを感じる。

* fugashi
    * pythonで書かれたmecabのwrapper
    * 扱いやすいらしい
* ipadic
* neologd
* mecab
* mecabtokenizer
* MeCabTagger
* jumanpp
* pyknp
* sudachi
    * java性
* kuromoji
https://github.com/WorksApplications/Sudachi


## BertJapaneseTokenizer
https://vscode.dev/github/0num4/bert-sentimental-classification/blob/mainapanese/tokenization_bert_japanese.py#L127
* bertjapanesetokenizerではbasicとmecabとsudachiとjumanppを選べる
* 

cl-tohoku/bert-base-japanese-v3を使うときはunidic_liteが必要
```
poetry add unidic
```