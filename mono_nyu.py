#!/usr/bin/env python3
"""
mono_nyu.py

Adapter class to use Bian et al.'s NYU Dataset classes in monodepth2
"""

import numpy as np
import copy
import glob
import random
import os

# Append monodepth2 and sc_depth_pl search paths
import sys
sys.path.insert(0, 'monodepth2')
sys.path.insert(0, 'sc_depth_pl')

from monodepth2.datasets.mono_dataset import MonoDataset
from sc_depth_pl.datasets.train_folders import TrainFolder
from sc_depth_pl.datasets.validation_folders import ValidationSet
from sc_depth_pl.datasets.test_folder import TestSet


class NYUDataset(MonoDataset):
    # monodepth2 calling convention:
    # trainer.py:
    # dataset(                  - Dataset class loaded from hardcoded dict(!)
    #   self.opt.data_path      - path to the training data
    #   train_filenames         - readlines(fpath.format("train")), splits txt file
    #   self.opt.height         - input image height (192)
    #   self.opt.width          - input image width (640)
    #   self.opt.frame_ids      - frames to load ([0, -1, 1])
    #   4                       - num_scales
    #   is_train=True           - True: training set; False: validation set
    #   img_ext=img_ext         - '.png' or '.jpg'
    # )
    #
    # evaluate_depth.py:
    # datasets.KITTIRAWDataset( - Dataset class hardcoded(!)
    #   opt.data_path           - path to the training data
    #   filenames               - readlines(os.path.join(splits_dir, opt.eval_split, "test_files.txt"))
    #   encoder_dict['height']  - trained input width
    #   encoder_dict['width']   - trained input height
    #   [0]                     - frames to load
    #   4                       - num_scales
    #   is_train=False          - 
    #   img_ext                 - unspecified, defaults to '.jpg'
    # )

    # NYU dataset class parameters:
    #   data_path               - nyu root folder (contains training/, testing/)
    #   is_train_val            - True if validation set (set by subclass)

    def __init__(self, *args, **kwargs):
        super(NYUDataset, self).__init__(*args, **kwargs)

        self.full_res_shape = (640, 480)
        self.side_map = None  # ??

        # Since monodepth uses a single intrinsic matrix, load from first scene...(?)
        K = np.loadtxt(f'{self.data_path}/training/basement_0001a/cam.txt')
        K[0, :] = K[0, :] / 640
        K[1, :] = K[1, :] / 480
        self.K = np.block([
            [K, np.zeros((3, 1))],
            [np.zeros((1, 3)), 1]
        ])

        # Override self.filenames
        # monodepth2 line format:
        # <folder> [<int:frame_index> <side>]
        if self.nyu_set() == 'trainval':
            # Generate filenames for set
            self.img_ext = '.jpg'
            self.filenames = []
            s = 'train' if self.is_train else 'val'
            with open(f'{self.data_path}/training/{s}.txt', 'rt') as f:
                folders = f.readlines()
            for folder in folders:
                folder = folder.strip()
                files = sorted(glob.glob(f'{self.data_path}/training/{folder}/*.jpg'))
                start = -min(self.frame_idxs)
                end = len(files) - max(self.frame_idxs)
                for i in range(start, end):
                    self.filenames.append(f'training/{folder} {i:06d} l')
            random.shuffle(self.filenames)
            # print(self.filenames[0:10])
        else:
            # Generate filenames for test images
            self.img_ext = '.png'
            self.filenames = []
            files = sorted(glob.glob(f'{self.data_path}/testing/color/*.png'))
            indices = [int(os.path.basename(f).strip('.png')) for f in files]
            for i in indices:
                self.filenames.append(f'testing/color {i:04d} l')
            random.shuffle(self.filenames)
            print(self.filenames[0:10])
    
    def check_depth(self):
        return self.nyu_set() == 'trainval' and self.is_train


class NYUTrainValSet(NYUDataset):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def nyu_set(self):
        return 'trainval'

class NYUTestSet(NYUDataset):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def nyu_set(self):
        return 'test'


# Example code
if __name__ == '__main__':
    # trainer.py:
    # dataset(                  - Dataset class loaded from hardcoded dict(!)
    #   self.opt.data_path      - path to the training data
    #   train_filenames         - readlines(fpath.format("train")), splits txt file
    #   self.opt.height         - input image height (192)
    #   self.opt.width          - input image width (640)
    #   self.opt.frame_ids      - frames to load ([0, -1, 1])
    #   4                       - num_scales
    #   is_train=True           - True: training set; False: validation set
    #   img_ext=img_ext         - '.png' or '.jpg'
    # )
    #
    # evaluate_depth.py:
    # datasets.KITTIRAWDataset( - Dataset class hardcoded(!)
    #   opt.data_path           - path to the training data
    #   filenames               - readlines(os.path.join(splits_dir, opt.eval_split, "test_files.txt"))
    #   encoder_dict['height']  - trained input width
    #   encoder_dict['width']   - trained input height
    #   [0]                     - frames to load
    #   4                       - num_scales
    #   is_train=False          - 
    #   img_ext                 - unspecified, defaults to '.jpg'
    # )

    kwargs_common = {
        'data_path': 'data/bian2022_split/nyu',
        'filenames': [],  # Will be overridden
        'height': 480,
        'width': 640,
        'num_scales': 4
    }
    
    kwargs_train = copy.deepcopy(kwargs_common)
    kwargs_train['frame_idxs'] = [0, -1, 1]
    kwargs_train['is_train'] = True
    kwargs_train['img_ext'] = '.jpg'

    kwargs_val = copy.deepcopy(kwargs_common)
    kwargs_val['frame_idxs'] = [0, -1, 1]
    kwargs_val['is_train'] = False
    kwargs_val['img_ext'] = '.jpg'

    kwargs_test = copy.deepcopy(kwargs_common)
    kwargs_test['frame_idxs'] = [0]
    kwargs_test['is_train'] = False
    kwargs_test['img_ext'] = '.jpg'

    nyu_train = NYUTrainValSet(**kwargs_train)
    nyu_val = NYUTrainValSet(**kwargs_val)
    nyu_test = NYUTestSet(**kwargs_test)
