import transformers
import transformers.models
import datasets

texts = [
    "眠い",
    "マジで麻雀ってカス。立直すると絶対振り込むんだけど。",
    "許せねぇ。○○を〇したい。",
    "devcontainer上のdindでdocker -vを使うと認識してくれないですが仕様なのかバグなのかよく分からんけど、キレてますとりあえず。",
    "機械には皮肉は通じないんだろうね。働かずにパソコンをカタカタしてれば人生終えれるの楽そうでいいね。",
    "いやそれはおかしい。働いているのはむしろパソコンだろ。"
]

