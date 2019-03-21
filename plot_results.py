# Code based on:
# https://studywolf.wordpress.com/2017/11/21/matplotlib-legends-for-mean-and-confidence-interval-plots/
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import colorConverter as cc
import numpy as np
from scipy import ndimage

def plot_mean_and_CI(mean, lb, ub, color_mean=None, color_shading=None):
    # plot the shaded range of the confidence intervals
    plt.fill_between(range(mean.shape[0]), ub, lb,
                     color=color_shading, alpha=.5)
    # plot the mean on top
    plt.plot(mean, color_mean)

class LegendObject(object):
    def __init__(self, facecolor='red', edgecolor='white', dashed=False):
        self.facecolor = facecolor
        self.edgecolor = edgecolor
        self.dashed = dashed
 
    def legend_artist(self, legend, orig_handle, fontsize, handlebox):
        x0, y0 = handlebox.xdescent, handlebox.ydescent
        width, height = handlebox.width, handlebox.height
        patch = mpatches.Rectangle(
            # create a rectangle that is filled with color
            [x0, y0], width, height, facecolor=self.facecolor,
            # and whose edges are the faded color
            edgecolor=self.edgecolor, lw=3)
        handlebox.add_artist(patch)
 
        # if we're creating the legend for a dashed line,
        # manually add the dash in to our rectangle
        if self.dashed:
            patch1 = mpatches.Rectangle(
                [x0 + 2*width/5, y0], width/5, height, facecolor=self.edgecolor,
                transform=handlebox.get_transform())
            handlebox.add_artist(patch1)
 
        return patch

# Load my results
envs = ['HalfCheetahBulletEnv-v0',
        'HopperBulletEnv-v0',
        'Walker2DBulletEnv-v0',
        'AntBulletEnv-v0',
        'InvertedPendulumBulletEnv-v0',
        'InvertedDoublePendulumBulletEnv-v0',
        'ReacherBulletEnv-v0']

# Plot and save to disk
for env in envs:
    fig = plt.figure(1, figsize=(12, 7))
    for algo, color in [('TD3', 'b'), ('DDPG', '#ffa500'), ('OurDDPG', 'g')]:  # #ffa500 is orange
        results = np.array([np.load(open('learning_curves/%s_%s_%d.npy' % (algo, env, i))) for i in range(10)])
        mean = np.mean(results, axis=0)
        std = np.std(results, axis=0)
        mean = ndimage.uniform_filter(mean, size=7)  # smooth for visual clarity
        std = ndimage.uniform_filter(std, size=7)
        ub = mean + std/4.
        lb = mean - std/4.

        plot_mean_and_CI(mean, ub, lb, color_mean=color, color_shading=color)

    plt.xticks([0., 40., 80., 120., 160., 200.], ['0.0', '0.2', '0.4', '0.6', '0.8', '1.0'])
     
    bg = np.array([1, 1, 1])  # background of the legend is white
    colors = ['b', '#ffa500', 'g']  # blue, orange, green
    # with alpha = .5, the faded color is the average of the background and color
    colors_faded = [(np.array(cc.to_rgb(color)) + bg) / 2.0 for color in colors]
     
    plt.legend([0, 1, 2], ['TD3', 'DDPG', 'our DDPG'],
               handler_map={
                   0: LegendObject(colors_faded[0], colors_faded[0]),
                   1: LegendObject(colors_faded[1], colors_faded[1]),
                   2: LegendObject(colors_faded[2], colors_faded[2]),
                })
     
    plt.title(env)
    plt.xlabel('Timesteps (1e6)')
    plt.ylabel('Average Return')
    plt.tight_layout()
    plt.grid()
    #plt.show()
    plt.savefig('plots/%s.png' % env)
    plt.clf()
    plt.cla()