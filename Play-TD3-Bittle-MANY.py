from __future__ import division
import torch
import gc
from collections import deque
import os
import carb
from omni.isaac.python_app import OmniKitHelper
import numpy as np
import omni
from omni.isaac.dynamic_control import _dynamic_control
from omni.isaac.utils.scripts.nucleus_utils import find_nucleus_server
import utils
import TD3_4 as TD3
import argparse
import time



LOAD_MODEL = "252.7424256414175-rwd-episode-835"


MAX_EPISODES = 100_000
MAX_STEPS = 3000
BITTLE_MOVE_DEQUESIZE = 10
HM_RANDOM_EPISODES = 10

MAX_BUFFER = 1_000_000   
MAX_TOTAL_REWARD = 300
BITTLE_COUNT = 20

parser = argparse.ArgumentParser()
parser.add_argument("--policy_name", default="TD3")					# Policy name
parser.add_argument("--env_name", default="BittleTD3")			    # OpenAI gym environment name
parser.add_argument("--seed", default=0, type=int)					# Sets Gym, PyTorch and Numpy seeds
parser.add_argument("--start_timesteps", default=1e4, type=int)		# How many time steps purely random policy is run for
parser.add_argument("--eval_freq", default=5e3, type=float)			# How often (time steps) we evaluate
parser.add_argument("--max_timesteps", default=1e9, type=float)		# Max time steps to run environment for
parser.add_argument("--save_models", action="store_true")			# Whether or not models are saved
parser.add_argument("--expl_noise", default=0.1, type=float)		# Std of Gaussian exploration noise
parser.add_argument("--batch_size", default=512, type=int)			# Batch size for both actor and critic
parser.add_argument("--discount", default=0.99, type=float)			# Discount factor 
parser.add_argument("--tau", default=0.005, type=float)				# Target network update rate
parser.add_argument("--policy_noise", default=0.2, type=float)		# Noise added to target policy during critic update
parser.add_argument("--noise_clip", default=0.5, type=float)		# Range to clip target policy noise
parser.add_argument("--policy_freq", default=2, type=int)			# Frequency of delayed policy updates
args = parser.parse_args()

file_name = "%s_%s_%s" % (args.policy_name, args.env_name, str(args.seed))
print("---------------------------------------")
print("Settings: %s" % (file_name))
print("---------------------------------------")

if not os.path.exists("results"):
    os.makedirs("results")
if args.save_models and not os.path.exists("pytorch_models"):
    os.makedirs("pytorch_models")

torch.manual_seed(args.seed)
np.random.seed(args.seed)

state_dim = 12 #env.observation_space.shape[0]
action_dim = 8 #env.action_space.shape[0] 
max_action = 1.1 #float(env.action_space.high[0])

if args.policy_name == "TD3": policy = TD3.TD3(state_dim, action_dim, max_action)

if LOAD_MODEL:
    policy.load(LOAD_MODEL,"models")


replay_buffer = utils.ReplayBuffer(max_size=5_000_000)

total_timesteps = 0
timesteps_since_eval = 0
episode_num = 0
done = True

t0 = time.time()

recent_rewards = deque(maxlen=100)


CONFIG = {
    "experience": f'{os.environ["EXP_PATH"]}/omni.isaac.sim.python.kit',
    "renderer": "RayTracedLighting",
    "headless": False,
}

JOINTS =   [
            "left_back_shoulder_joint",
            "left_back_knee_joint",
            "left_front_shoulder_joint",
            "left_front_knee_joint",
            "right_back_shoulder_joint",
            "right_back_knee_joint",
            "right_front_shoulder_joint",
            "right_front_knee_joint"]



kit = OmniKitHelper(config=CONFIG)

with open("recent_rewards.txt","w") as f:
    pass

largest_average_rwd = 0

for _ep in range(MAX_EPISODES):

    do_random = False
    stage = kit.get_stage()
    result, nucleus_server = find_nucleus_server()
    if result is False:
        carb.log_error("Could not find nucleus server with /Isaac folder")

    asset_path = nucleus_server + "/Isaac/20-Bittles-very-long-6.usd"
    omni.usd.get_context().open_stage(asset_path)
    kit.play()
    kit.update(1.0 / 60.0)

    dc = _dynamic_control.acquire_dynamic_control_interface()

    print('EPISODE :- ', _ep)

    bittle_starting_poses = {}
    bittle_prev_rewards = {}
    bittle_states = {}
    bittle_actions = {}
    bittle_action_hist = {}
    
    for step in range(MAX_STEPS):

        for bittle_num in range(BITTLE_COUNT):
            art = dc.get_articulation(f"/bittle_{bittle_num:02d}")
            chassis = dc.get_articulation_root_body(art)

            pose = dc.get_rigid_body_pose(chassis)

            if step == 0:
                bittle_starting_poses[bittle_num] = pose.p
                bittle_prev_rewards[bittle_num] = 0
                bittle_action_hist[bittle_num] = deque(maxlen=BITTLE_MOVE_DEQUESIZE)

            observation = np.float32([dof_state[0] for dof_state in dc.get_articulation_dof_states(art, _dynamic_control.STATE_ALL)]  + [p for p in pose.r]  )

            state = np.float32(observation)
            bittle_states[bittle_num] = state
            action = policy.select_action(observation)
            bittle_actions[bittle_num] = action
            bittle_action_hist[bittle_num].append(action)

            for idx,j in enumerate(JOINTS):
                dof_ptr = dc.find_articulation_dof(art, j)
                dc.wake_up_articulation(art)
                new_position = action[idx] # get the action for that specific index
                dc.set_dof_position_target(dof_ptr, new_position)


        kit.update(1.0 / 60.0)


        for bittle_num in range(BITTLE_COUNT):

            art = dc.get_articulation(f"/bittle_{bittle_num:02d}")
            chassis = dc.get_articulation_root_body(art)

            new_observation = np.float32([dof_state[0] for dof_state in dc.get_articulation_dof_states(art, _dynamic_control.STATE_ALL)]  + [p for p in pose.r]  )
            pose = dc.get_rigid_body_pose(chassis)

            start_x = bittle_starting_poses[bittle_num][0]
            start_y = bittle_starting_poses[bittle_num][1]

            current_x = pose.p[0]
            current_y = pose.p[1]

            total_reward = ((current_y - start_y) - (abs(start_x-current_x)))/10.0
            reward = total_reward - bittle_prev_rewards[bittle_num]
            bittle_prev_rewards[bittle_num] = total_reward
            new_state = np.float32(new_observation)

    gc.collect()
    recent_rewards.append(total_reward)
