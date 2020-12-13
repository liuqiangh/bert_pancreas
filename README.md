# bert-chinese-ner

## 前言

使用预训练语言模型BERT做中文NER尝试，fine - tune BERT模型

PS: 移步最新[**albert fine-tune ner**](https://github.com/ProHiryu/albert-chinese-ner)模型

## 代码参考

- [BERT-NER](https://github.com/kyzhouhzau/BERT-NER)
- [BERT-TF](https://github.com/google-research/bert)

## 使用方法

从[BERT-TF](https://github.com/google-research/bert)下载bert源代码，存放在路径下bert文件夹中

从[BERT-Base Chinese](https://storage.googleapis.com/bert_models/2018_11_03/chinese_L-12_H-768_A-12.zip)下载模型，存放在checkpoint文件夹下

使用BIO数据标注模式，使用人民日报经典数据

train：

`CUDA_VISIBLE_DEVICES=1 python BERT_NER.py --data_dir=data/ruijin/ --bert_config_file=checkpoint/bert_config.json --init_checkpoint=checkpoint/bert_model.ckpt --vocab_file=vocab.txt --output_dir=./output5/result_dir/`

brat:

`Linux系统在/var/www/html文件夹下`

extract_feature:

`CUDA_VISIBLE_DEVICES=1 python extract_features.py --input_file=/tmp/0.txt --output_file=/tmp/output.jsonl --vocab_file=../checkpoint/vocab.txt --bert_config_file=../checkpoint/bert_config.json --init_checkpoint=../output19/checkpoint/model.ckpt-2000 --layers=-1,-2,-3,-4 --max_seq_length=128 --batch_size=8`

run_classifier.py:
`CUDA_VISIBLE_DEVICES=1 python run_classifier.py --data_dir=../data/zheyi/note/ --bert_config_file=../checkpoint/bert_config.json --init_checkpoint=../checkpoint/clinical_bert/model.ckpt-9000 --vocab_file=../vocab.txt --output_dir=../output1/result_dir/ --do_train=True --do_eval=True`

create_pretraining_data:

`CUDA_VISIBLE_DEVICES=1 python create_pretraining_data.py --input_file=../data/zheyi/all_panc_note/pretraining.txt --output_file=../data/zheyi/all_panc_note/tf_examples.tfrecord --vocab_file=../vocab.txt --do_lower_case=True --max_seq_length=128 --max_predictions_per_seq=20 --masked_lm_prob=0.15 --random_seed=12345 --dupe_factor=5`

run_pretraining:
`CUDA_VISIBLE_DEVICES=1 python run_pretraining.py --input_file=../data/zheyi/all_panc_note/tf_examples_128.tfrecord --output_dir=../pretrained_model/pretraining_output_128 --do_train=True --do_eval=True --bert_config_file=../checkpoint/bert_config.json --init_checkpoint=../checkpoint/bert_model.ckpt --train_batch_size=64 --max_seq_length=128 --max_predictions_per_seq=20 --num_train_steps=100000 --num_warmup_steps=10 --learning_rate=2e-5`


## 结果

经过100个epoch跑出来的结果

```
eval_f = 0.9662649
eval_precision = 0.9668882
eval_recall = 0.9656949
global_step = 135181
loss = 40.160034
```

测试结果第一句：

![](test.png)
