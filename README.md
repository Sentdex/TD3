# Benchmarking TD3 and DDPG on PyBullet

This repo contains benchmark results for TD3 and DDPG using the [PyBullet](https://docs.google.com/document/d/10sXEhzFRSnvFcl3XxNGhnD4N2SedqwdAvK3dsihxVUA/edit#) reinforcement learning environments; specifically Ant, HalfCheetah, Hopper, InvertedPendulum, InvertedDoublePendulum, Reacher, and Walker2D. In the [TD3 paper](https://arxiv.org/abs/1802.09477), results were reported for the [MuJoCo](http://www.mujoco.org/) version of these environments. PyBullet is a free and open-source alternative to MuJoCo, whith no license fees and no hardware lock (MuJoCo personal licenses are limited to 3 physical machines, which means you cannot run simulations in the cloud, e.g. AWS/GCP/etc).

This repo itself is a fork of the [official TD3 code](https://github.com/sfujim/TD3/) from the original authors of the TD3 paper. Per the original repo, results were generated with Python 2.7 and PyTorch 0.4. Specific to this repo, PyBullet 2.4.8 was used. To obtain these results, run:
```
./run_experiments.sh
```

## Learning curves
Below are the learning curves for TD3, DDPG, and OurDDPG, using the algorithms in TD3.py, DDPG.py, and OurDDPG.py. Note the results for "DDPG" are *not* those presented in the TD3 paper, per the original README.

![HalfCheetahBulletEnv](plots/HalfCheetahBulletEnv-v0.png)
![HopperBulletEnv](plots/HopperBulletEnv-v0.png)
![Walker2DBulletEnv](plots/Walker2DBulletEnv-v0.png)
![AntBulletEnv](plots/AntBulletEnv-v0.png)
![ReacherBulletEnv](plots/ReacherBulletEnv-v0.png)
![InvertedPendulumBulletEnv](plots/InvertedPendulumBulletEnv-v0.png)
![InvertedDoublePendulumBulletEnv](plots/InvertedDoublePendulumBulletEnv-v0.png)

These plots were generated via:
```
python plot_results.py
```
Details of how the plots were generated can be found in the [TD3 paper](https://arxiv.org/abs/1802.09477) figure 5, and original README file (README_orig.md). In the TD3 paper, the authors mentioned that "[c]urves are smoothed uniformly for visual clarity", so I used `scipy.ndimage.uniform_filter(data, size=7)` -- the window size was chosen arbitrarily by me.

## Pre-trained models
Pre-trained models can be downloaded from here (TBD).

## Agent visualization
To visualize a saved agent, run the following:
```
python eval.py --policy TD3 --env_name HalfCheetahBulletEnv-v0 --filename TD3_HalfCheetahBulletEnv-v0_0 --visualize
```

For more details, please refer to the code in 'eval.py'.