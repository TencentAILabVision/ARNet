# Code Captioning

## Dependencies
 - Python 3.6
 - Pytorch [0.1.12](http://download.pytorch.org/whl/cu80/torch-0.1.12.post1-cp36-cp36m-linux_x86_64.whl)
 - CUDA 8.0

## Data Pre-processing
The dataset of HabeasCorpus should be existed under the folder `data`, which is download from [ReviewNet](https://github.com/kimiyoung/review_net/blob/master/code_caption/README.md). Then we pre-process the dataset as follows:
```bash
python3.6 prepro_gen_data.py
```

We can obtain the following data:
 - index2token.pkl
 - token2index.pkl
 - train_data.pkl
 - val_data.pkl
 - test_data.pkl

## Encoder-Decoder Model

### Training with MLE
To train the encoder-decoder model with MLE, run
```bash
./bash_code_caption_ende_xe.sh
```

### Fine-tuning with ARNet
Then, we fune-tuning the network with our ARNet,
```bash
./bash_code_caption_ende_rcst.sh
```

### Inference
To test the model with greedy search, run
```bash
./bach_code_caption_ende_inf.sh
```

### Visualization
To visualize the hidden states with t-SNE, run
```bash
./bash_code_caption_ende_vis.sh
```
We will get the hidden states of generated sequence. Then, run
```bash
python3.6 prepro_tsne_reduction_vis.py --vis_batch_size 80 \
                                       --truncation 0  \
                                       --hidden_path '...' \
                                       --hidden_reduction_save_path '...'
```


## ReviewNet Model

### Training with MLE
We reimplement the ReviewNet proposed in [Yang](https://arxiv.org/abs/1605.07912) with PyTorch. To train the ReviewNet with MLE, run
```bash
./bash_code_caption_reviewnet_xe.sh
```

### Inference
To test the ReviewNet with greedy search, run
```bash
./bash_code_caption_reviewnet_inf.sh
```


## Attentive Encoder-Decoder Model

### Training with MLE
To train the attention-based model with MLE, run
```bash
./bash_code_caption_soft_att_xe.sh
```

### Fine-tuning with ARNet
To fine-tuning the model with our ARNet based on the MLE model, run
```bash
./bash_code_caption_soft_att_rcst.sh
```

### Inference
To test the model, run
```bash
./bash_code_caption_soft_att_inf.sh
```

### Visualization
To get the hidden states of the whole sequence, run
```bash
./bash_code_caption_soft_att_vis.sh
```
Then, visualize the hidden state as follows:
```bash
python3.6 prepro_tsne_reduction_vis.py --vis_batch_size 80 \
                                       --truncation 0  \
                                       --hidden_path '...' \
                                       --hidden_reduction_save_path '...'
```

