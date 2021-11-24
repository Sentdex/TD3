import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style



style.use('dark_background')
fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)

def animate(i):
    exploit_scores_x = []
    exploit_scores_y = []
    with open("exploit_rwd.txt","r") as f:
        data = f.read()
        for xy in data.split("\n")[:-1]:
            x,y = xy.split(",")
            exploit_scores_x.append(float(x))
            exploit_scores_y.append(round(float(y),2))

    train_scores_x = []
    train_scores_y = []
    with open("train_rwd.txt","r") as f:
        data = f.read()
        for xy in data.split("\n")[:-1]:
            x,y = xy.split(",")
            train_scores_x.append(float(x))
            train_scores_y.append(round(float(y),2))

    ax1.clear()

    # horizontal line at 0, thin
    ax1.axhline(y=0, color='w', linewidth=0.5)
    
    ax1.plot(train_scores_x, train_scores_y, label="train")
    ax1.plot(exploit_scores_x, exploit_scores_y, label="exploit")

    ax1.set_xlabel('Episode')
    ax1.set_ylabel('Reward')
    ax1.legend(loc=4)

    # add title:
    ax1.set_title('TD3-Bittle-5')
    
    
ani = animation.FuncAnimation(fig, animate, interval=1000)
plt.show()
