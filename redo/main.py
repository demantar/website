import tensorflow as tf
import mnist as mn
import numpy as np
from random import randint


data = mn.MNIST("C:\\Users\\zulutime\\Documents\\mnist")
data.gz = True;

images, labels_unproccesed = data.load_training()

labels = np.zeros((len(labels_unproccesed), 10), dtype = np.float32)
labels[np.arange(len(labels_unproccesed)), labels_unproccesed] = 1;

t_images, t_labels_unproccesed = data.load_testing()

t_labels = np.zeros((len(t_labels_unproccesed), 10), dtype = np.float32)
t_labels[np.arange(len(t_labels_unproccesed)), t_labels_unproccesed] = 1;


SETTINGS = {
    "learning_rate"   : 1e-4,
    "batch_size"      : 50,
    "epochs"          : 3,
    "data_set_size"   : len(images),
    "print_frequency" : 50
}


def convnn(input, dropout_keep_probability, histograms = True):

    with tf.name_scope("reshape_layer_1"):
        reshape_layer_1_O = tf.reshape(input, [-1, 28, 28, 1])

    with tf.name_scope("convolutional_layer_1"):
        convolutional_layer_1_W = tf.Variable(tf.truncated_normal([5, 5, 1, 32]))
        convolutional_layer_1_B = tf.Variable(tf.zeros([32]))
        convolutional_layer_1_O = tf.nn.relu(tf.nn.conv2d(reshape_layer_1_O,
                                                          convolutional_layer_1_W,
                                                          [1, 1, 1, 1],
                                                          padding = "SAME") +
                                                          convolutional_layer_1_B)
        if histograms:
            tf.summary.histogram("Weights", convolutional_layer_1_W)
            tf.summary.histogram("Biases",  convolutional_layer_1_B)
            tf.summary.histogram("Output",  convolutional_layer_1_O)

    with tf.name_scope("pooling_layer_1"):
        pooling_layer_1_O = tf.nn.max_pool(convolutional_layer_1_O,
                                           ksize = [1, 2, 2, 1],
                                           strides = [1, 2, 2, 1],
                                           padding = "SAME")

    with tf.name_scope("convolutional_layer_2"):
        convolutional_layer_2_W = tf.Variable(tf.truncated_normal([5, 5, 32, 64]))
        convolutional_layer_2_B = tf.Variable(tf.zeros([64]))
        convolutional_layer_2_O = tf.nn.relu(tf.nn.conv2d(pooling_layer_1_O,
                                                          convolutional_layer_2_W,
                                                          [1, 1, 1, 1],
                                                          padding = "SAME") +
                                                          convolutional_layer_2_B)
        if histograms:
            tf.summary.histogram("Weights", convolutional_layer_2_W)
            tf.summary.histogram("Biases",  convolutional_layer_2_B)
            tf.summary.histogram("Output",  convolutional_layer_2_O)

    with tf.name_scope("pooling_layer_2"):
        pooling_layer_2_O = tf.nn.max_pool(convolutional_layer_2_O,
                                           ksize = [1, 2, 2, 1],
                                           strides = [1, 2, 2, 1],
                                           padding = "SAME")

    with tf.name_scope("reshape_layer_2"):
        reshape_layer_2_O = tf.reshape(pooling_layer_2_O, [-1, 7 * 7 * 64])

    with tf.name_scope("fully_connected_layer_1"):
        fully_connected_layer_1_W = tf.Variable(tf.truncated_normal([7 * 7 * 64, 1024]))
        fully_connected_layer_1_B = tf.Variable(tf.zeros([1024]))
        fully_connected_layer_1_O = tf.nn.relu(reshape_layer_2_O @
                                               fully_connected_layer_1_W +
                                               fully_connected_layer_1_B)
        if histograms:
            tf.summary.histogram("Weights", fully_connected_layer_1_W)
            tf.summary.histogram("Biases",  fully_connected_layer_1_B)
            tf.summary.histogram("Output",  fully_connected_layer_1_O)

    with tf.name_scope("dropout_layer_1"):
        dropout_layer_1_O = tf.nn.dropout(fully_connected_layer_1_O,
                                          dropout_keep_probability)

    with tf.name_scope("fully_connected_layer_2"):
        fully_connected_layer_2_W = tf.Variable(tf.truncated_normal([1024, 10]))
        fully_connected_layer_2_B = tf.Variable(tf.zeros([10]))
        fully_connected_layer_2_O = tf.add((dropout_layer_1_O @
                                            fully_connected_layer_2_W),
                                            fully_connected_layer_2_B, name = "output")
        if histograms:
            tf.summary.histogram("Weights", fully_connected_layer_2_W)
            tf.summary.histogram("Biases",  fully_connected_layer_2_B)
            tf.summary.histogram("Output",  fully_connected_layer_2_O)

    return fully_connected_layer_2_O


xs = tf.placeholder(tf.float32, [None, 784], name = "input")
ys = tf.placeholder(tf.float32, [None, 10], name = "wanted_output")
keep_prob = tf.placeholder(tf.float32, name = "keep_probability")

output = convnn(xs, keep_prob)

with tf.name_scope("error"):
    cross_entropy = tf.nn.softmax_cross_entropy_with_logits(logits = output,
                                                            labels = ys)
    error = tf.reduce_mean(cross_entropy, name="error")

with tf.name_scope('accuracy'):
    correct_prediction = tf.equal(tf.argmax(output, 1), tf.argmax(ys, 1))
    correct_prediction = tf.cast(correct_prediction, tf.float32)
    accuracy = tf.reduce_mean(correct_prediction, name="accuracy")

with tf.name_scope("optimizer"):
    optimizer = tf.train.AdamOptimizer(SETTINGS["learning_rate"])
    train_step = optimizer.minimize(error)

tf.summary.scalar("error", error)
tf.summary.scalar("accuracy", accuracy)
tf.summary.scalar("learning_rate", optimizer._lr)

with tf.Session() as sess:

    graph_save = input("directory to save information about graph in: ")
    if graph_save != "f":
        train_writer = tf.summary.FileWriter("C:\\Users\\zulutime\\Documents\\atom projects\\python test\\redo\\logs\\train\\" + graph_save + "tr", sess.graph)
        test_writer = tf.summary.FileWriter("C:\\Users\\zulutime\\Documents\\atom projects\\python test\\redo\\logs\\train\\" + graph_save + "te", sess.graph)

    sess.run(tf.global_variables_initializer())

    for epoch in range(SETTINGS["epochs"]):
        for b in range(0, SETTINGS["data_set_size"], SETTINGS["batch_size"]):
            #print (images[b:SETTINGS["batch_size"]])
            sess.run(train_step, feed_dict = {xs: images[b:b+SETTINGS["batch_size"]],
                                              ys: labels[b:b+SETTINGS["batch_size"]],
                                              keep_prob: 0.5})
            if b / SETTINGS["batch_size"] % SETTINGS["print_frequency"] == 0:
                print ("epoch: {} batch: {} accuracy: {}".format(epoch,
                                                                 b / SETTINGS["batch_size"],
                                                                 sess.run(accuracy,
                                                                          feed_dict = {xs: images[b:b+SETTINGS["batch_size"]],
                                                                                       ys: labels[b:b+SETTINGS["batch_size"]],
                                                                                       keep_prob: 0.5})))
                if graph_save != "f":
                    merge = tf.summary.merge_all()
                    summary = sess.run(merge, feed_dict = {xs: images[b:b+SETTINGS["batch_size"]],
                                                           ys: labels[b:b+SETTINGS["batch_size"]],
                                                           keep_prob: 1})
                    train_writer.add_summary(summary, SETTINGS["data_set_size"] * epoch + b)

                    index = randint(0, len(t_images) - SETTINGS["batch_size"] - 1)
                    summary = sess.run(merge, feed_dict = {xs: t_images[index:index+SETTINGS["batch_size"]],
                                                           ys: t_labels[index:index+SETTINGS["batch_size"]],
                                                           keep_prob: 1})
                    test_writer.add_summary(summary, SETTINGS["data_set_size"] * epoch + b)
        print ("epoch: {} finneshed".format(epoch))

    tf.saved_model.simple_save(sess,
            "C:\\Users\\zulutime\\Documents\\atom projects\\python test\\redo\\mod\\" + graph_save,
            inputs={"xs": xs, "ys": ys, "keep_prob": keep_prob},
            outputs={"output": output, "error": error, "accuracy": accuracy})

    print ("testing set accuracy:")
    print (sess.run(accuracy,
                    feed_dict = {xs: t_images,
                                 ys: t_labels,
                                 keep_prob: 1}))
