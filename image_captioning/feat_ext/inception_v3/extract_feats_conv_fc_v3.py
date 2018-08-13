#! encoding: UTF-8

import os
import glob
import time
import h5py
import ipdb
import urllib2
import numpy as np
import tensorflow as tf
from datasets import imagenet
from nets import inception
from preprocessing import inception_preprocessing


checkpoints_dir = './checkpoints'
if not tf.gfile.Exists(checkpoints_dir):
    tf.gfile.MakeDirs(checkpoints_dir)

slim = tf.contrib.slim

image_size = inception.inception_v4.default_image_size

mscoco_images_path = '/data1/ailab_view/image_caption/data/images_horizontal_flip/train2014'

images_conv_feats_save_path = '/data1/ailab_view/image_caption/inception/feats/train_val_test_feats_v4_conv_horizontal_flip'
images_fc_feats_save_path = '/data1/ailab_view/image_caption/inception/feats/train_val_test_feats_v4_fc_horizontal_flip'

images_lists = sorted(glob.glob(mscoco_images_path + '/*.jpg'))

tf_image = tf.placeholder(tf.string, None)
image = tf.image.decode_jpeg(tf_image, channels=3)
processed_image = inception_preprocessing.preprocess_image(image, image_size, image_size, is_training=False)
processed_images  = tf.expand_dims(processed_image, 0)

with slim.arg_scope(inception.inception_v4_arg_scope()):
    tf_feats_att, tf_feats_fc = inception.inception_v4(processed_images, num_classes=1001, is_training=False, create_aux_logits=False)

init_fn = slim.assign_from_checkpoint_fn(os.path.join(checkpoints_dir, 'inception_v4.ckpt'), slim.get_model_variables('InceptionV4'))   
        
with tf.Session() as sess:    

    init_fn(sess)

    for idx, image_path in enumerate(images_lists):
        start_time = time.time()
        
        image_name = os.path.basename(image_path)
        
        url = 'file://' + image_path
        image_string = urllib2.urlopen(url).read()
        
        conv_feats, fc_feats = sess.run([tf_feats_att, tf_feats_fc], feed_dict={tf_image: image_string})
        conv_feats = np.squeeze(conv_feats)
        fc_feats = np.squeeze(fc_feats)

        conv_feats_save_path = images_conv_feats_save_path + '/' + image_name + '.npy'
        fc_feats_save_path = images_fc_feats_save_path + '/' + image_name + '.npy'

        np.save(conv_feats_save_path, conv_feats)
        np.save(fc_feats_save_path, fc_feats)

        print('{}  {}  time cost: {:.5f}'.format(idx, image_name, time.time()-start_time))

