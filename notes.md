NYU v2
======

https://cs.nyu.edu/~silberman/datasets/nyu_depth_v2.html


Downloads
=========

Labeled dataset: http://horatio.cs.nyu.edu/mit/silberman/nyu_depth_v2/nyu_depth_v2_labeled.mat
    - MAT file. Variables: see web page for description.
        - images: HxWx3xN matrix
        - scenes: Nx1 array, name of scene in which image N is taken
        - sceneTypes: Nx1 type of scene
        - rawDepths: HxWxN. Depths in m reprojected onto RGB image
            - depths: HxWxN. Inpainted depths

Raw dataset: https://cs.nyu.edu/~silberman/datasets/nyu_depth_v2.html#raw_parts
    - Extremely large
    - Not post-processed (e.g. RGB and Depth synchronization)

Toolbox: http://cs.nyu.edu/~silberman/code/toolbox_nyu_depth_v2.zip
    - `camera_params.m`: Kinect camera parameters
    - `get_synched_frames.m`: only for raw dataset, I hope?