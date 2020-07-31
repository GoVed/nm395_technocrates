import tensorflow as tf
import numpy as np

def conv3d(x, W, b, strides=1):
    # Conv2D wrapper, with bias and relu activation
    x = tf.nn.conv3d(x, W, strides=[1, strides, strides, 1, 1], padding='SAME')
    x = tf.nn.bias_add(x, b)
    return tf.nn.relu(x)

def maxpool3d(x, k=2):
    return tf.nn.max_pool3d(x, ksize=[1, k, k, 1, 1], strides=[1, k, k, 1, 1],padding='SAME')



x_train=np.load('features.npy')

y_train=np.zeros(2000,dtype=np.float32)
y_train[:400]=1



x=tf.placeholder(np.uint8,[None,100,100,3,6])
x=tf.cast(x,tf.float32)
y=tf.placeholder(np.float32,[None,1])


wc1=tf.Variable(tf.random_normal([3,3,1,6,8]))
wc2=tf.Variable(tf.random_normal([3,3,1,8,16]))
wc3=tf.Variable(tf.random_normal([3,3,1,16,4]))
wd1=tf.Variable(tf.random_normal([150000,1]))
out=tf.Variable(tf.random_normal([128,1]))

bc1=tf.Variable(tf.random_normal([8]))
bc2=tf.Variable(tf.random_normal([16]))
bc3=tf.Variable(tf.random_normal([4]))
bd1=tf.Variable(tf.random_normal([1]))
out=tf.Variable(tf.random_normal([1]))



conv1 = conv3d(x,wc1, bc1)
conv1 = maxpool3d(conv1, k=2)


conv2 = conv3d(conv1,wc2, bc2)
conv2 = maxpool3d(conv2, k=2)

conv3 = conv3d(conv2, wc3, bc3)


fc1 = tf.reshape(conv3, [-1, 150000])
fc1 = tf.add(tf.matmul(fc1,wd1), bd1)
fc1 = tf.nn.relu(fc1)

# out = tf.add(tf.matmul(fc1, out), out)

cost=abs((fc1-y))/1

optimizer = tf.train.AdamOptimizer(learning_rate=0.001).minimize(cost)
batch_size=20
init = tf.global_variables_initializer()
with tf.Session() as sess:
    sess.run(init)
    
    
    for i in range(25):
        randomimg=np.random.choice(2000,batch_size)
        x_batch=np.zeros((batch_size,100,100,3,6))
        y_batch=np.zeros((batch_size,1))
        j=0
        for each in randomimg:
            x_batch[j]=x_train[each]
            y_batch[j]=y_train[each]
            j+=1
        opt = sess.run(optimizer, feed_dict={x: x_batch,y: y_batch})
        loss = sess.run(cost, feed_dict={x: x_batch,y: y_batch})
        print(i,loss.mean())
    print(sess.run(fc1,feed_dict={x:x_train[0:20]}))
    print(sess.run(fc1,feed_dict={x:x_train[500:520]}))
        

