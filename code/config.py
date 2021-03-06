############################
# General Settings
############################

# crop_size: crop size for the input image, center crop
crop_size = 178

# image_size: input/output image resolution, test output is 2x
image_size = 64

# Establish convention for real and fake probability labels during training
real_prob = 1
fake_prob = 0

# train_batch_size: mini-batch size for training
train_batch_size = 128

# test_batch_size: mini-batch size for testing
test_batch_size = 64

# num_workers
num_workers = 4

# n_epochs: number of training epochs
n_epochs = 80

# random_seed: to give consistent results
random_seed = 1111

# selected_attr: list of selected attributes to train. Set to None for all attr.
selected_attr = None

############################
# Generator Settings
############################

# g_input_dim: dimension of domain labels, input to G.
g_input_dim = len(selected_attr) if selected_attr else 40

# g_num_blocks: number of residual blocks in G
g_num_blocks = 6

# g_conv_channels: list of out channels for conv layers in G
g_conv_channels = [512, 256, 128, 64]

# g_out_channels: number of channels in the output image from G
g_out_channels = 3

# g_wd: weight decay for G
g_wd = 0

# g_lr: learning rate for G
g_lr = 0.0001

# g_l1_weights: weights for L1 Loss.
g_l1_weights = [1.0, 0.9, 0.8 ,0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1]

# g_skip_all: number of image samples for which to skip G training
g_skip_all = 200600*35

# g_skip_cls: number of image samples for which to skip G cls loss
g_skip_cls = 200600*50

############################
# Discriminator Settings
############################

# d_cls_dim: dimension of domain labels, classification by D.
d_cls_dim = g_input_dim

# d_in_channels: number of channels in the input image
d_in_channels = g_out_channels

# d_wd: weight decay for D
d_wd = 0

# d_lr: learning rate for D
d_lr = 0.001

# d_conv_channels: list of out channels for conv layers in D
d_conv_channels = [64, 128, 256, 512]

# d_leaky_slope: slope of leaky relu
d_leaky_slope = 0.2

# d_update_ratio: number of D updates per each G update
d_update_ratio = 1

############################
# Directory Settings
############################

image_dir = './../data/images/'
attr_path = './../data/list_attr_celeba.txt'
log_dir = './../logs'
models_dir = './../models'
result_dir = './../results'
