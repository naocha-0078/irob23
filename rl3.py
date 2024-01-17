import gymnasium as gym
env = gym.make("CartPole-v1", render_mode="human")

lr = 0.99  #learning rate
gamma = 1  #割引率
pdiv, vdiv, adiv, avdiv = 10, 10, 10, 10
q = [[[[[0, 0, 0, 0, 0] for _ in range(avdiv)] for _ in range(adiv)] for _ in range(vdiv)] for _ in range(pdiv)]
# print(q)

obs, info = env.reset()
for i in range(1000):
    p, v, a, av = obs[0], obs[1], obs[2], obs[3]
    pd = int((p - (-4.80000021e+00)) / (4.80000021e+00 - (-4.80000021e+00)) * pdiv)
    vd = int((v - (-3.40282351e+38)) / (3.40282351e+38 - (-3.40282351e+38)) * vdiv)
    ad = int((a - (-4.18879031e-01)) / (4.18879031e-01 - (-4.18879031e-01)) * adiv)
    avd = int((av - (-3.40282351e+38)) / (3.40282351e+38 - (-3.40282351e+38)) * avdiv)
    action = int(q[pd][vd][ad][avd].index(max(q[pd][vd][ad][avd])))   #greedy法
    obs, reward, terminated, truncated, info = env.step(action)

    p1, v1, a1, av1 = obs[0], obs[1], obs[2], obs[3]
    pd1 = int((p1 - (-4.80000021e+00)) / (4.80000021e+00 - (-4.80000021e+00)) * pdiv)
    vd1 = int((v1 - (-3.40282351e+38)) / (3.40282351e+38 - (-3.40282351e+38)) * vdiv)
    ad1 = int((a1 - (-4.18879031e-01)) / (4.18879031e-01 - (-4.18879031e-01)) * adiv)
    avd1 = int((av1 - (-3.40282351e+38)) / (3.40282351e+38 - (-3.40282351e+38)) * avdiv)
    
    q[pd][vd][ad][avd][action] += lr * (reward + gamma * max(q[pd1][vd1][ad1][avd1]) - q[pd][vd][ad][avd][action])

    print(q)
    # print(p, v)
    # print(pd, vd)
    # print(p1, v1)

    if terminated or truncated:
        obs, info = env.reset()

env.close()