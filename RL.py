import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F

import gymnasium as gym
import numpy as np
import pandas as pd
import gymnasium as gym

class DQN(nn.Module):
    def __init__(self, n_observations, n_actions) -> None:
        super().__init__()
        self.Layer1 = nn.Linear(n_observations, 128)
        self.Layer2 = nn.Linear(128, 128)
        self.Layer3 = nn.Linear(128, n_actions)

    def forward(self, input):
        input = F.relu(self.Layer1(input))
        input = F.relu(self.Layer2(input))
        return self.Layer3(input)
    
def actionMaker(explorationChance:float, actionSpace:int, memory:np.ndarray, time:int):
    """explorationChance, needs to be a number between 0 and 1 for probability"""
    randomDecimal = np.random.rand
    action
    if randomDecimal > explorationChance:
        action = np.random.randint(0, actionSpace)
    else:
        action = memory[time][numberOfColumns - 1]

actionMaker(0.5, 2, )



env = gym.make("CartPole-v1", render_mode="human")
observation, info = env.reset()
observationSize = len(observation)

DQN_model = DQN(observationSize, env.action_space.n)
optimization = optim.SGD(DQN_model.parameters(), lr=1e-3)
loss_function = nn.HuberLoss()

memory_Size = 0
numberOfColumns = 2 * observationSize + 1
memory = np.zeros((1000, numberOfColumns))
#2 for the old and new states stats, 1 for whcih action taken, reward not recroded since it is always 1

#for _ in range(1000):
while(not terminated):
    #action = env.action_space.sample()  # agent policy that uses the observation and info

    observation, reward, terminated, truncated, info = env.step(action)

    pred = DQN_model(observation)

    for i in range(env.observation_space):
        memory[memory_Size][i] = observation[i]
        memory[memory_Size][i + env.observation_space] = pred[i + env.observation_space]
        memory[memory_Size][numberOfColumns - 1] = action
    
    memory_Size += 1

    if terminated or truncated:
        loss = loss_function(pred, )
        memory_Size = 0
        memory = 

        observation, info = env.reset()

env.close()