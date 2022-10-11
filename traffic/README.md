# ATTEMPT 1

This was just a test to see if I got the syntax right. There are no deep layers here - the input layer gets flattened and passed straight into the output. This was done on the test set

The accuracy is remarkable - even without any deep layers or convolution steps we went from a 0.33 accuracy to 0.8 - although in this case, we might be benefiting from the simplicity of the dataset, as well as the dataset being heavily weighted to category 1

## Attempt 1 model
    model = tf.keras.Sequential([
    tf.keras.layers.InputLayer(input_shape=input_shape), # input layer - 3 dimensional array of width, height, RGB values
    tf.keras.layers.Flatten(), # flatten the inputs into a single dimension
    tf.keras.layers.Dense(NUM_CATEGORIES, activation="sigmoid")]) # output layer - 41 units, one for each category, sigmoid activation function
    model.compile(
        optimizer="adam",
        loss="binary_crossentropy",
        metrics=["accuracy"]
    )


## Attempt 1 results
Epoch 1/10
493/493 [==============================] - 1s 2ms/step - loss: 2.9468 - accuracy: 0.3652
Epoch 2/10
493/493 [==============================] - 1s 2ms/step - loss: 1.3688 - accuracy: 0.6003
Epoch 3/10
493/493 [==============================] - 1s 2ms/step - loss: 1.2700 - accuracy: 0.6642
Epoch 4/10
493/493 [==============================] - 1s 2ms/step - loss: 1.0984 - accuracy: 0.7130
Epoch 5/10
493/493 [==============================] - 1s 2ms/step - loss: 1.2132 - accuracy: 0.7284
Epoch 6/10
493/493 [==============================] - 1s 2ms/step - loss: 1.1015 - accuracy: 0.7559
Epoch 7/10
493/493 [==============================] - 1s 2ms/step - loss: 1.0929 - accuracy: 0.7669
Epoch 8/10
493/493 [==============================] - 1s 2ms/step - loss: 0.9894 - accuracy: 0.7917
Epoch 9/10
493/493 [==============================] - 1s 2ms/step - loss: 0.9126 - accuracy: 0.8097
Epoch 10/10
493/493 [==============================] - 1s 2ms/step - loss: 0.9757 - accuracy: 0.8076
329/329 - 0s - loss: 0.9789 - accuracy: 0.7973 - 477ms/epoch - 1ms/step


# ATTEMPT 2
Let's try adding a convolution and a single deep layer

## Attempt 2 model
model = tf.keras.Sequential([
    tf.keras.layers.InputLayer(input_shape=input_shape), # input layer - 3 dimensional array of width, height, RGB values
    tf.keras.layers.Conv2D (32, (3, 3), activation="relu", input_shape=input_shape), # 32 filters, 3x3 kernel, ReLu activation function
    tf.keras.layers.Flatten(), # flatten the inputs into a single dimension
    tf.keras.layers.Dense(64, activation="relu"), # 64 neurons, ReLu activation function for a single deep layer
    tf.keras.layers.Dense(NUM_CATEGORIES, activation="sigmoid")]) # output layer - 41 units, one for each category, sigmoid activation function
    model.compile(
        optimizer="adam",
        loss="binary_crossentropy",
        metrics=["accuracy"]
    )

I'll be honest - I don't fully understand the 'filters' variable in Conv2D
My understanding is that the CNN learns and refines the filters in this way - but the sheer number of filters (32) seems like a bit much?

## Attempt 2 results
Epoch 1/10
16/16 [==============================] - 1s 10ms/step - loss: 50.6427 - accuracy: 0.7996
Epoch 2/10
16/16 [==============================] - 0s 9ms/step - loss: 0.7242 - accuracy: 0.9742
Epoch 3/10
16/16 [==============================] - 0s 9ms/step - loss: 4.6795e-04 - accuracy: 1.0000
Epoch 4/10
16/16 [==============================] - 0s 9ms/step - loss: 0.0112 - accuracy: 1.0000
Epoch 5/10
16/16 [==============================] - 0s 9ms/step - loss: 0.0048 - accuracy: 1.0000
Epoch 6/10
16/16 [==============================] - 0s 9ms/step - loss: 0.0016 - accuracy: 1.0000
Epoch 7/10
16/16 [==============================] - 0s 9ms/step - loss: 7.5082e-05 - accuracy: 1.0000
Epoch 8/10
16/16 [==============================] - 0s 9ms/step - loss: 2.2667e-05 - accuracy: 1.0000
Epoch 9/10
16/16 [==============================] - 0s 9ms/step - loss: 6.5694e-06 - accuracy: 1.0000
Epoch 10/10
16/16 [==============================] - 0s 9ms/step - loss: 3.6642e-06 - accuracy: 1.0000
11/11 - 0s - loss: 0.0803 - accuracy: 0.9911 - 135ms/epoch - 12ms/step

Much better accuracy. Let's test it on the main dataset.

# ATTEMPT 3
The same network as above, tested on the main dataset

## Attempt 3 results
Epoch 1/10
493/493 [==============================] - 5s 9ms/step - loss: 0.4908 - accuracy: 0.5223
Epoch 2/10
493/493 [==============================] - 4s 8ms/step - loss: 0.0369 - accuracy: 0.8390
Epoch 3/10
493/493 [==============================] - 4s 8ms/step - loss: 0.0237 - accuracy: 0.9068
Epoch 4/10
493/493 [==============================] - 4s 8ms/step - loss: 0.0191 - accuracy: 0.9316
Epoch 5/10
493/493 [==============================] - 4s 8ms/step - loss: 0.0154 - accuracy: 0.9489
Epoch 6/10
493/493 [==============================] - 4s 8ms/step - loss: 0.0134 - accuracy: 0.9583
Epoch 7/10
493/493 [==============================] - 4s 8ms/step - loss: 0.0144 - accuracy: 0.9583
Epoch 8/10
493/493 [==============================] - 4s 8ms/step - loss: 0.0117 - accuracy: 0.9657
Epoch 9/10
493/493 [==============================] - 4s 8ms/step - loss: 0.0120 - accuracy: 0.9681
Epoch 10/10
493/493 [==============================] - 4s 8ms/step - loss: 0.0127 - accuracy: 0.9681
329/329 - 1s - loss: 0.0433 - accuracy: 0.8975 - 1s/epoch - 3ms/step

Actually not too bad. Note that the accuracy on the actual set is significantly worse than the training set - we're probably looking at some overfitting here.

Let's try adding a second convolution and pooling layer before the flattening, as well as a dropout layer to prevent overfitting

# ATTEMPT 4

## Attempt 4 model
    input_shape = (IMG_WIDTH, IMG_HEIGHT, 3)
    model = tf.keras.Sequential([
    tf.keras.layers.InputLayer(input_shape=input_shape), # input layer - 3 dimensional array of width, height, RGB values
    tf.keras.layers.Conv2D (16, (3, 3), activation="relu", input_shape=input_shape), # 16 filters, 3x3 kernel, ReLu activation function
    tf.keras.layers.MaxPooling2D(pool_size=(2, 2)), # pooling
    tf.keras.layers.Conv2D (32, (3, 3), activation="relu", input_shape=input_shape), # 32 filters, 3x3 kernel, ReLu activation function
    tf.keras.layers.MaxPooling2D(pool_size=(2, 2)), # pooling
    tf.keras.layers.Flatten(), # flatten the inputs into a single dimension
    tf.keras.layers.Dense(128, activation="relu"), # 128 neurons, ReLu activation function for a single deep layer
    tf.keras.layers.Dropout(0.5), #dropout layer to prevent overfitting
    tf.keras.layers.Dense(NUM_CATEGORIES, activation="sigmoid")]) # output layer - 41 units, one for each category, sigmoid activation function
    model.compile(
        optimizer="adam",
        loss="binary_crossentropy",
        metrics=["accuracy"]
    )

# Attempt 4 results
Epoch 1/10
493/493 [==============================] - 3s 6ms/step - loss: 0.2387 - accuracy: 0.2020   
Epoch 2/10
493/493 [==============================] - 3s 6ms/step - loss: 0.0665 - accuracy: 0.5344
Epoch 3/10
493/493 [==============================] - 3s 6ms/step - loss: 0.0436 - accuracy: 0.6991
Epoch 4/10
493/493 [==============================] - 3s 6ms/step - loss: 0.0325 - accuracy: 0.7904
Epoch 5/10
493/493 [==============================] - 3s 6ms/step - loss: 0.0251 - accuracy: 0.8492
Epoch 6/10
493/493 [==============================] - 3s 6ms/step - loss: 0.0205 - accuracy: 0.8836
Epoch 7/10
493/493 [==============================] - 3s 6ms/step - loss: 0.0170 - accuracy: 0.9086
Epoch 8/10
493/493 [==============================] - 3s 6ms/step - loss: 0.0151 - accuracy: 0.9236
Epoch 9/10
493/493 [==============================] - 3s 6ms/step - loss: 0.0133 - accuracy: 0.9340
Epoch 10/10
493/493 [==============================] - 3s 6ms/step - loss: 0.0119 - accuracy: 0.9460
329/329 - 1s - loss: 0.0070 - accuracy: 0.9764 - 929ms/epoch - 3ms/step

We see that the final accuracy of the training set is similar to the actual set - the dropout layer seems to help with overfitting, while the additional pooling layer actually reduces model training time with no decrease in accuracy.

We can still do better though. It looks like it was still continuing to improve with each epoch - let's increase epochs to 15

# ATTEMPT 5
Same code as before but with 15 epochs

## Attempt 5 results
Epoch 1/15
493/493 [==============================] - 4s 7ms/step - loss: 0.3172 - accuracy: 0.1250
Epoch 2/15
493/493 [==============================] - 3s 7ms/step - loss: 0.0801 - accuracy: 0.4492
Epoch 3/15
493/493 [==============================] - 3s 7ms/step - loss: 0.0521 - accuracy: 0.6434
Epoch 4/15
493/493 [==============================] - 3s 7ms/step - loss: 0.0387 - accuracy: 0.7535
Epoch 5/15
493/493 [==============================] - 3s 7ms/step - loss: 0.0301 - accuracy: 0.8179
Epoch 6/15
493/493 [==============================] - 3s 7ms/step - loss: 0.0236 - accuracy: 0.8669
Epoch 7/15
493/493 [==============================] - 3s 7ms/step - loss: 0.0195 - accuracy: 0.8983
Epoch 8/15
493/493 [==============================] - 3s 6ms/step - loss: 0.0165 - accuracy: 0.9179
Epoch 9/15
493/493 [==============================] - 3s 6ms/step - loss: 0.0144 - accuracy: 0.9302
Epoch 10/15
493/493 [==============================] - 3s 7ms/step - loss: 0.0129 - accuracy: 0.9389
Epoch 11/15
493/493 [==============================] - 3s 6ms/step - loss: 0.0116 - accuracy: 0.9483
Epoch 12/15
493/493 [==============================] - 3s 7ms/step - loss: 0.0111 - accuracy: 0.9502
Epoch 13/15
493/493 [==============================] - 3s 7ms/step - loss: 0.0102 - accuracy: 0.9582
Epoch 14/15
493/493 [==============================] - 3s 6ms/step - loss: 0.0092 - accuracy: 0.9623
Epoch 15/15
493/493 [==============================] - 3s 7ms/step - loss: 0.0087 - accuracy: 0.9643
329/329 - 1s - loss: 0.0068 - accuracy: 0.9801 - 980ms/epoch - 3ms/step

Pretty happy with this one.