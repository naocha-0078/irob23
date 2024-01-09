import gymnasium as gym
import random

env = gym.make("CartPole-v1", render_mode="human")

lr = 0.99  #learning rate
gamma = 1  #割引率

q = [[0, 0, 0, 0] for _ in range(16)]

obs, info = env.reset()
for i in range(10000):
    while True:
        action = random.randint(0, 3)
        if max(q[obs][action]) == q[obs][action]: break

    obs1, reward, terminated, truncated, info = env.step(action)
    q[obs][action] += lr * (reward + gamma * max(q[obs1][action]) - q[obs][action])
    obs = obs1

    if terminated or truncated:
        obs, info = env.reset()

env.close()