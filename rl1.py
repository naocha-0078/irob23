import gymnasium as gym
env = gym.make("MountainCar-v0", render_mode="human")

<<<<<<< HEAD
lr = 0.99  #learning rate
gamma = 1  #割引率
pdiv, vdiv = 10, 10
q = [[[0, 0, 0] for _ in range(vdiv)] for _ in range(pdiv)]
# print(q)

obs, info = env.reset()
for i in range(100000):
    p, v = obs[0], obs[1]
    if i % 10 == 0 or p > 0.25: env.render()
    pd = int((p - (-1.21)) / (0.61 - (-1.21)) * pdiv)
    vd = int((v - (-0.071)) / (0.071 - (-0.071)) * vdiv)
    action = q[pd][vd].index(max(q[pd][vd]))   #greedy法
    obs, reward, terminated, truncated, info = env.step(action)

    p1, v1 = obs[0], obs[1]
    pd1 = int((p1 - (-1.21)) / (0.61 - (-1.21)) * pdiv)
    vd1 = int((v1 - (-0.071)) / (0.071 - (-0.071)) * vdiv)

    q[pd][vd][action] += lr * (reward + gamma * max(q[pd1][vd1]) - q[pd][vd][action])

    print(q)
    print(p, v)
    print(pd, vd)
    print(p1, v1)

    if terminated or truncated:
        obs, info = env.reset()

=======
obs, info = env.reset()
for _ in range(1000):
    env.render()
    action = env.action_space.sample()
    obs, reward, terminated, truncated, info = env.step(action)

    if term or truncated:
        obs, info = env.reset()
>>>>>>> 68924db8ab194964ed9c8d5d58737deffb95dd29
env.close()