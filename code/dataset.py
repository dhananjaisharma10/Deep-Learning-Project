import os
import torch
import random
import numpy as np
from PIL import Image
from torch.utils import data
from torchvision import transforms as T
from torchvision.datasets import ImageFolder

class CelebA(data.Dataset):
    """Dataset class for the CelebA dataset."""

    def __init__(self, image_dir, attr_path, transform, mode, selected_attr=None):
        """Initialize and preprocess the CelebA dataset."""
        self.image_dir = image_dir
        self.attr_path = attr_path
        self.transform = transform
        self.selected_attr = selected_attr
        self.mode = mode
        self.train_dataset = []
        self.test_dataset = []
        self.attr2idx = {}
        self.idx2attr = {}
        self.preprocess()
        if mode == 'train':
            self.num_images = len(self.train_dataset)
        elif mode == 'test':
            self.num_images = len(self.test_dataset)
        else:   # mode == all
            self.num_images = len(self.train_dataset) + len(self.test_dataset)
        print('Mode: %s, Num Images: %d' % (mode, self.num_images))

    def preprocess(self):
        """Preprocess the CelebA attribute file."""
        lines = [line.rstrip() for line in open(self.attr_path, 'r')]
        all_attr_names = lines[1].split()
        for i, attr_name in enumerate(all_attr_names):
            self.attr2idx[attr_name] = i
            self.idx2attr[i] = attr_name
        lines = lines[2:]
        if self.selected_attr is None:
            selected_attr_names = all_attr_names
        else:
            selected_attr_names = self.selected_attr
        #random.shuffle(lines)
        for i, line in enumerate(lines):
            split = line.split()
            filename = split[0]
            values = split[1:]
            label = []
            for attr_name in selected_attr_names:
                idx = self.attr2idx[attr_name]
                label.append(values[idx] == '1')
            if (i+1) < 2000:
                self.test_dataset.append([filename, label])
            else:
                self.train_dataset.append([filename, label])
            if i == 0:
                image = Image.open(os.path.join(self.image_dir, filename))
                image = self.transform(image)
                self.image_shape = image.shape
        self.label_shape = np.array(self.train_dataset[0][1]).shape
        print('Finished preprocessing the CelebA dataset for mode =', self.mode)

    def __getitem__(self, index):
        """Return one image and its corresponding attribute label."""
        mode = self.mode
        if self.mode == 'all':
            mode = 'train' if index < len(self.train_dataset) else 'test'
            index = index if index < len(self.train_dataset) else index - len(self.train_dataset)
        dataset = self.train_dataset if mode == 'train' else self.test_dataset
        filename, label = dataset[index]
        image = Image.open(os.path.join(self.image_dir, filename))
        return self.transform(image), torch.FloatTensor(label)

    def __len__(self):
        """Return the number of images."""
        return self.num_images

def get_loader(image_dir, attr_path, crop_size=178, image_size=64,
               batch_size=16, mode='train', num_workers=1, selected_attr=None):
    """Build and return a data loader."""
    transform = []
    if mode == 'train':
        transform.append(T.RandomHorizontalFlip())
    transform.append(T.CenterCrop(crop_size))
    transform.append(T.Resize(image_size))
    transform.append(T.ToTensor())
    transform.append(T.Normalize(mean=(0.5, 0.5, 0.5), std=(0.5, 0.5, 0.5)))
    transform = T.Compose(transform)
    dataset = CelebA(image_dir, attr_path,  transform, mode, selected_attr=selected_attr)
    data_loader = data.DataLoader(dataset=dataset,
                                  batch_size=batch_size,
                                  shuffle=(mode=='train' or mode=='all'),
                                  num_workers=num_workers)
    data_loader.image_shape = dataset.image_shape
    data_loader.label_shape = dataset.label_shape
    return data_loader
