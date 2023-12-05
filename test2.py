import matplotlib.pyplot as plt
import numpy as np
import numpy.linalg as la

sigma = np.array([[1,-0.2],[-0.2,2]])
w, p  = la.eig(sigma)
lmd = np.diag(w)
theta = np.arange(0, np.pi * 2 + 0.2, 0.2)
c = np.array([np.cos(theta), np.sin(theta)])
x = p.dot((lmd ** 0.5).dot(c))
plt.figure().add_subplot().set_aspect('equal')
plt.plot(x[0,:],x[1,:])
plt.show()
