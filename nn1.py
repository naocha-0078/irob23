import torch
import torch.nn as nn
import numpy as np
import matplotlib.pyplot as plt

N = 1000
x = np.random.random((N, 2)).astype(np.float32) * 6 - 3

tf = ((x[:, 0]  ** 2 / 4 + x[:, 1] ** 2 / (1.5 ** 1) < 1) & (x[:, 0] ** 2 + x[:, 1] ** 2 > 1)) #楕円式

y = np.zeros((N, 2))
y[:] = [0, 1]
y[tf] = [1, 0]

xt = torch.from_numpy(x)
yt = torch.from_numpy(y)


for i in range(100):

    print(i)

    model = nn.Sequential(
    nn.Linear(2, 10),
    nn.ReLU(),
    nn.Linear(10, 2),
    nn.Softmax(dim=1)
    )

    loss_fn = nn.CrossEntropyLoss() #loss関数を作成する関数、returnがloss関数
    opt = torch.optim.Adam(model.parameters())

    plt.title("upper: grand truth, lower: prediction")
    plt.axis("off")


    axs = plt.subplot(2, 1, 1)
    plt.scatter(x[tf][:, 0], x[tf][:, 1], 15)
    plt.scatter(x[tf == False][:, 0], x[tf == False][:, 1], 15)
    plt.xlim(-3, 3)
    plt.ylim(-3, 3)
    axs.set_aspect("equal", "box")

    
    pred = model(xt)
    loss = loss_fn(pred, yt)
    print(loss)

    for i in range(10000):
        pred = model(xt)
        loss = loss_fn(pred, yt)
        opt.zero_grad()
        loss.backward()
        opt.step()
        if i % 100 == 0:
            print(i)

        if i % 10000 == 0:
            print(loss)


    pred = model(xt)
    loss = loss_fn(pred, yt)
    print(loss)

    tf2 = pred[:, 0] > pred[:, 1]
    
    axs = plt.subplot(2, 1, 2)
    plt.scatter(x[tf2][:, 0], x[tf2][:, 1], 15)
    plt.scatter(x[tf2 == False][:, 0], x[tf2 == False][:, 1], 15)
    plt.xlim(-3, 3)
    plt.ylim(-3, 3)
    axs.set_aspect("equal", "box")
    plt.show(block=False)
    plt.pause(3)
    plt.close()
