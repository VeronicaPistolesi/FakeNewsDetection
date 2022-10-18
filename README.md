# FakeNewsDetection

The purpose of this work is to make a contribution to the challenge of Fake News Detection:
the task of correctly classifying news as fake or real. In particular, this study compares four
different neural networks trained on the pre-processed Fake News Dataset [1] with the state
of the art. All the architectures are implemented with a pre-trained word embedding method,
namely GloVe or fastText. The proposed models are a Convolutional Neural Network, two
types of gated Recurrent Neural Networks - Bidirectional LSTM and GRU - and a combination
of Convolutional Neural Network with Bidirectional LSTM. The first experiments show that
Bidirectional LSTM with fastText word embedding is the model with the best results. Finally,
the best model is put into a Transformer architecture, with BERT (bert-base-uncased) used
as embedding layer, further exceeding previous performances.

Authors: Annachiara Aiello and Veronica Pistolesi
