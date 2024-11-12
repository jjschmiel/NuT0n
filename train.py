from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from envNuton import Nut0nEnv as Env
import tensorflow as tf

from tf_agents.agents.reinforce import reinforce_agent
from tf_agents.environments import tf_py_environment
from tf_agents.networks import actor_distribution_network
from tf_agents.replay_buffers import tf_uniform_replay_buffer
from tf_agents.trajectories import trajectory
from tf_agents.trajectories import policy_step
from tf_agents.specs import tensor_spec
from tf_agents.replay_buffers import reverb_replay_buffer
from tf_agents.replay_buffers import reverb_utils
from tf_agents.policies import py_tf_eager_policy
from tf_agents.drivers import py_driver
from tf_agents.replay_buffers import py_uniform_replay_buffer
from tf_agents.drivers import dynamic_step_driver

import tf_agents.policies as policies
import numpy as np
import pygame
import reverb

# Keep using keras-2 (tf-keras) rather than keras-3 (keras).


# suppress warning about CPU usage
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
os.environ['TF_USE_LEGACY_KERAS'] = '1'

BREAKOUT_REWARD = 1500000

# Hyper parameters
num_iterations = 1000  # @param {type:"integer"}
collect_episodes_per_iteration = 10  # @param {type:"integer"}
replay_buffer_capacity = 200000  # @param {type:"integer"}

FC_LAYER_PARAMS = (200, 100) #a tuple of ints representing the sizes of each hidden layer

learning_rate = 0.001  # @param {type:"number"}
num_eval_episodes = 5  # @param {type:"integer"}
eval_interval = 10  # @param {type:"integer"}
save_interval = 10
epsilon = 0.0000001

tf.compat.v1.enable_v2_behavior()



t_env = Env()
e_env = Env()

train_env = tf_py_environment.TFPyEnvironment(t_env)
eval_env = tf_py_environment.TFPyEnvironment(e_env)

actor_net = actor_distribution_network.ActorDistributionNetwork(
    train_env.observation_spec(),
    train_env.action_spec(),
    fc_layer_params=FC_LAYER_PARAMS
)

optimizer = tf.compat.v1.train.AdamOptimizer(learning_rate=learning_rate)#, epsilon=epsilon)
train_step_counter = tf.compat.v2.Variable(0)

pre_train_checkpoint = tf.train.Checkpoint(actor_net=actor_net,
                                           optimizer=optimizer)

checkpoint_directory = "tmp/training_checkpoints"
checkpoint_prefix = os.path.join(checkpoint_directory, "newly_trained_models")

manager = tf.train.CheckpointManager(pre_train_checkpoint,
                                     directory=checkpoint_prefix,
                                     checkpoint_name='save',
                                     max_to_keep=50)

tf_agent = reinforce_agent.ReinforceAgent(
    train_env.time_step_spec(),
    train_env.action_spec(),
    actor_network=actor_net,
    optimizer=optimizer,
    normalize_returns=True,
    train_step_counter=train_step_counter
)

tf_agent.initialize()

eval_policy = tf_agent.policy
collect_policy = tf_agent.collect_policy

def compute_avg_return(environment, policy, num_episodes=10):
    total_return = 0.0
    Env.graphics = True
    print("Computing average return...")

    for _ in range(num_episodes):
        print("Episode: {0}".format(_))

        time_step = environment.reset()
        episode_return = 0.0

        while not time_step.is_last():
            action_step = policy.action(time_step)
            time_step = environment.step(action_step.action)
            episode_return += time_step.reward
            #print("Episode return: {0}".format(episode_return))
        total_return += episode_return

    Env.graphics = False
    avg_return = total_return / num_episodes

    return avg_return.numpy()[0]

#OLD REPLAY BUFFER
replay_buffer = tf_uniform_replay_buffer.TFUniformReplayBuffer(
    data_spec=tf_agent.collect_data_spec,
    batch_size=train_env.batch_size,
    max_length=replay_buffer_capacity
)

print("replay_buffer data spec: {0}".format(replay_buffer.data_spec))

# Add an observer that adds to the replay buffer:
# replay_observer = [replay_buffer.add_batch]

# collect_steps_per_iteration = 10
# collect_op = dynamic_step_driver.DynamicStepDriver(
#   train_env,
#   tf_agent.collect_policy,
#   observers=replay_observer,
#   num_steps=collect_steps_per_iteration).run()

#OLD COLLECT EPISODE
def collect_episode(environment, policy, num_episodes):
    episode_counter = 0
    environment.reset()

    while episode_counter < num_episodes:
        time_step = environment.current_time_step()
        action_step = policy.action(time_step)
        #print("Action Step: {0}".format(action_step))
        next_time_step = environment.step(action_step.action)
        traj = trajectory.from_transition(time_step, action_step,
                                          next_time_step)
        print("Trajectory: {0}".format(traj))

        # Add trajectory to the replay buffer
        replay_buffer.add_batch(traj)

        if traj.is_boundary():
            episode_counter += 1

# def collect_episode(environment, policy, num_episodes):
#     print("Collecting episode...")
#     driver = py_driver.PyDriver(
#         environment,
#         py_tf_eager_policy.PyTFEagerPolicy(
#         policy, use_tf_function=True),
#         [r],
#         max_episodes=num_episodes)
#     initial_time_step = environment.reset()
#     driver.run(initial_time_step)


# BEGIN TRAINING
if __name__ == "__main__":
    # Reset the train step
    tf_agent.train_step_counter.assign(0)

    #print("Evaluating base policy:")
    #pre_train_avg = compute_avg_return(eval_env, tf_agent.policy)
    #print("Base return: {0}\n".format(pre_train_avg))

    manager.save()

    greedy = []
    collect = []

    # Evaluate the agent's policy once before training.
    avg_return = compute_avg_return(eval_env, tf_agent.policy, num_eval_episodes)
    returns = [avg_return]

    print("Beginning Training...")

    for _ in range(num_iterations):
        # Collect a few episodes using collect_policy and save to the replay buffer.
        collect_episode(
            train_env, tf_agent.collect_policy, collect_episodes_per_iteration)
        
        # Use data from the buffer and update the agent's network.
        experience = replay_buffer.gather_all()
        train_loss = tf_agent.train(experience=experience)
        replay_buffer.clear()

        step = tf_agent.train_step_counter.numpy()

        if step % save_interval == 0:
            print('step = {0}: loss = {1}'.format(step, train_loss.loss))

        if step % eval_interval == 0:
            avg_return = compute_avg_return(eval_env, tf_agent.policy, num_eval_episodes)
            print('step = {0}: Average Return = {1}'.format(step, avg_return))
            returns.append(avg_return)


    # OLD TRAINING LOOP
    # for _ in range(num_iterations):

    #     # Collect a few episodes using collect_policy and save to the replay buffer.
    #     collect_episode(train_env, tf_agent.collect_policy,
    #                     collect_episodes_per_iteration)

    #     # Use data from the buffer and update the agent's network.
    #     #print("replay_buffer.batch_size: {0}".format(replay_buffer._batch_size))
    #     experience = replay_buffer.gather_all()
    #     #print("reward: {0}".format(experience.reward.sum()))
    #     x = 0.0
    #     interations = 0
    #     for y in experience.reward:
    #         for z in y:
    #             interations += 1
    #             print("Reward {1}: {0}".format(z, interations))
    #             x += z
    #     print("{1} Total Iteration Reward: {0}".format(x, interations))

    #     train_loss = tf_agent.train(experience)
    #     #print("train loss: {0}".format(train_loss))
    #     replay_buffer.clear()

    #     step = tf_agent.train_step_counter.numpy()

    #     print("Training episode: {0}".format(step))

    #     #if step % save_interval == 0:
    #     manager.save()

    #     if step % eval_interval == 0:
    #         print("\n___Policy Evaluation___")
    #         print('step = {0}: loss = {1}'.format(step, train_loss.loss))
    #         print("Evaluating Greedy Policy...")
    #         avg_greedy =  (eval_env, tf_agent.policy)
    #         print('step = {0}: Greedy Avg Return = {1}'.format(step, avg_greedy))
    #         greedy.append(avg_greedy)
    #         print("Evaluating Collection Policy...")
    #         avg_collect = compute_avg_return(train_env, tf_agent.collect_policy)
    #         print(
    #             'step = {0}: Collection Avg Return = {1}'.format(step, avg_collect))
    #         collect.append(avg_greedy)
    #         print("___Resuming Training___\n")

    #         # Breakout of training if reward > BREAKOUT_REWARD
    #         print("average greedy: {0}".format(avg_greedy))
    #         print("BREAKOUT REWARD: {0}".format(BREAKOUT_REWARD))
    #         if avg_greedy > BREAKOUT_REWARD:
    #             break

    train_env.close()
    eval_env.close()

    # Data
    print("\nTotal training episodes: {0}".format(step))

    print("\nPolicy Rewards: ")
    for i in range(len(greedy)):
        episode = (i + 1) * eval_interval
        print("Greedy at episode {0}: reward = {1}".format(episode, greedy[i]))
        print("Collection at episode {0}: reward = {1}".format(episode, collect[i]))

