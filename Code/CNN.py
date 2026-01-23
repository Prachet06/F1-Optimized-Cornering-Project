# TODO: Create a bespoke CNN model for this data set
# TODO: Think about cropping the image to only include the road maybe but I guess the image has to be square
# TODO: Think of how much padding should be applied to this CNN based on how important the borders of the image are
#       consult this article (https://medium.com/thedeephub/convolutional-neural-networks-a-comprehensive-guide-5cc0b5eae175)
#       and think about the stride too.
import tensorflow as tf

from tensorflow.keras import datasets, layers, models
import matplotlib.pyplot as plt