#!/bin/bash

# Script to reproduce results

for ((i=0;i<10;i+=1))
do 
	python2 main.py \
	--policy_name "TD3" \
	--env_name "HalfCheetahBulletEnv-v0" \
	--seed $i \
	--start_timesteps 10000

	python2 main.py \
	--policy_name "TD3" \
	--env_name "HopperBulletEnv-v0" \
	--seed $i \
	--start_timesteps 1000

	python2 main.py \
	--policy_name "TD3" \
	--env_name "Walker2DBulletEnv-v0" \
	--seed $i \
	--start_timesteps 1000

	python2 main.py \
	--policy_name "TD3" \
	--env_name "AntBulletEnv-v0" \
	--seed $i \
	--start_timesteps 10000

	python2 main.py \
	--policy_name "TD3" \
	--env_name "InvertedPendulumBulletEnv-v0" \
	--seed $i \
	--start_timesteps 1000

	python2 main.py \
	--policy_name "TD3" \
	--env_name "InvertedDoublePendulumBulletEnv-v0" \
	--seed $i \
	--start_timesteps 1000

	python2 main.py \
	--policy_name "TD3" \
	--env_name "ReacherBulletEnv-v0" \
	--seed $i \
	--start_timesteps 1000
done
