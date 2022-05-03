#!/usr/bin/env python3
"""
nyuloader.py

PyTorch dataloader for the NYUv2 dataset, using the Bian 2020/2022 split.
"""

from types import SimpleNamespace

import numpy as np
import glob
import os

from torch.utils.data import Dataset

class NYUDataset(Dataset):
    def __init__(
            self,
            nyu_folder,
            set,                # ['train' | 'val' | 'test']
            frame_spacing = 1
            ):
        self.items = []

        if set == 'train' or set == 'val':
            dirs = []
            with open(f'{nyu_folder}/training/train.txt', 'rt') as f:
                for line in f:
                    dirs.append(line.strip())
            for dir in dirs:
                K = np.loadtxt(f'{nyu_folder}/training/{dir}/cam.txt')
                files = sorted(glob.glob(f'{nyu_folder}/training/{dir}/*.jpg'))
                for i in range(frame_spacing, len(files) - frame_spacing):
                    self.items.append(SimpleNamespace(
                        rgb = files[i],
                        rgb_prev = files[i - frame_spacing],
                        rgb_next = files[i + frame_spacing]
                    ))

        elif set == 'val':
            dirs = []
            with open(f'{nyu_folder}/training/val.txt', 'rt') as f:
                for line in f:
                    dirs.append(line.strip())

        elif set == 'test':
            pass
    
    def __len__(self):
        pass

    def __getitem__(self, index):
        pass


# Example code
if __name__ == '__main__':
    nyu_folder = 'data/bian2022_split/nyu'
    set = 'train'
    frame_spacing = 1

    nyu = NYUDataset(nyu_folder, set, frame_spacing)
