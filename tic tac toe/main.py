import tensorflow as tf
import numpy as np
from nn import *

input = tf.placeholder(dtype = tf.float32,
                       shape = [None, 9],
                       name = "input")

output = nn(input)

init = tf.global_variables_initializer()

with tf.Session() as sess:
    sess.run(init)
    print(sess.run(output, feed_dict = {input: np.ones([1, 9])}));
