import tensorflow as tf

def nn(input):
    with tf.name_scope("layer_1"):
        l1_reshape = tf.reshape(input, [-1, 3, 3, 1])
        l1_weights = tf.Variable(tf.truncated_normal([3, 3, 1, 64]))
        l1_biases  = tf.Variable(tf.zeros([64]))
        l1_output  = tf.nn.elu(tf.nn.convolution(l1_reshape, l1_weights, "VALID") +
                                l1_biases)
        print ("l1_output_shape: " + str(l1_output.get_shape()))

    with tf.name_scope("layer_2"):
        l2_reshape = tf.reshape(l1_output, [-1, 64])
        l2_weights = tf.Variable(tf.truncated_normal([64, 64]))
        l2_biases  = tf.Variable(tf.zeros([64]))
        l2_output  = tf.nn.elu(l2_reshape @
                                l2_weights +
                                l2_biases)
        print ("l2_output_shape: " + str(l2_output.get_shape()))

    with tf.name_scope("layer_3"):
        l3_weights = tf.Variable(tf.truncated_normal([64, 32]))
        l3_biases  = tf.Variable(tf.zeros([32]))
        l3_output  = tf.tanh(l2_output @
                              l3_weights +
                              l3_biases)
        print ("l3_output_shape: " + str(l3_output.get_shape()))

    with tf.name_scope("layer_4"):
        l4_weights = tf.Variable(tf.truncated_normal([32, 9]))
        l4_biases  = tf.Variable(tf.zeros([9]))
        l4_output  = l3_output @ l4_weights + l4_biases
        print ("l4_output_shape: " + str(l4_output.get_shape()))

    return (l4_output)
