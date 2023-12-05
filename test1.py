import numpy as np

B = 0.342                   #トレッド
p0= np.array([[1],[0.5],[0]]) #真値
p = np.array(p0)            #推定値

def move_robo(p, dsl, dsr):
    dt = (dsr - dsl) / B
    r = (dsl + dsr) / (2*dt)
    dx = 2*r *np.sin(dt / 2) * np.cos(p[2,0] + dt /2)
    dy = 2*r *np.sin(dt / 2) * np.sin(p[2,0] + dt /2)

    return p + np.array([[dx],[dy],[dt]])

print(p0)
print(move_robo(p0, 1, 0.5))
