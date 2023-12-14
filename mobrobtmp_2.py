import matplotlib.pyplot as plt
import numpy as np
import numpy.linalg as la
import math as m


sigma1 = np.array([[1,0],[0,2]])
w1, p1  = la.eig(sigma1)
lmd1 = np.diag(w1)

sigma2 = np.array([[2,0],[0,2]])
w2, p2  = la.eig(sigma2)
lmd2 = np.diag(w2)


sigma4 = np.linalg.inv(sigma1)
sigma5 = np.linalg.inv(sigma2)
sigma6 = np.linalg.inv(sigma1+sigma2)
print(sigma6)

w3, p3  = la.eig(sigma6)
lmd3 = np.diag(w3)

sigma7 = sigma1 + sigma2

mu1 = np.dot(sigma1 , np.linalg.inv(sigma7))
mu2 = np.dot(mu1, sigma2)

mu3 = np.dot(np.linalg.inv(sigma1),np.array([[2],[0]]))
mu4 = np.dot(np.linalg.inv(sigma2),np.array([[3],[0]]))
mu5 = mu3 + mu4

mu= np.dot(mu2, mu5)
print(mu)
# print(mu2)

# print(np.dot(np.array([[1,1],[1,2]]),np.array([[1],[1]])))

theta = np.arange(0, np.pi * 2 + 0.2, 0.2)
c = np.array([np.cos(theta), np.sin(theta)])

x1 = p1.dot((lmd1 ** 0.5).dot(c))
x2 = p2.dot((lmd2 ** 0.5).dot(c))
x3 = p3.dot((lmd3 ** 0.5).dot(c))

plt.figure().add_subplot().set_aspect('equal')

plt.plot(x1[0,:]+2,x1[1,:], color="red")
plt.text(0.9, 1.1, "bel_1", fontsize="xx-large", color="red")

plt.plot(x2[0,:]+3,x2[1,:], color="blue")
plt.text(3.5, 1.1, "bel_2", fontsize="xx-large", color="blue")

plt.plot(x3[0,:]+mu[0],x3[1,:], color="green")
plt.text(2.2, -0.7, "bel", fontsize="xx-large", color="green")

plt.savefig('fig2.jpg')
