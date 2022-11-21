import matplotlib.pyplot as plt
from matplotlib import animation, rc
import random
import math

def main():
    import sys
    # check if this code is running in colab
    in_colab = 'google.colab' in sys.modules
    
    random.seed(1111)
    W, H = 120, 100
    # 200 birds on a WxH window
    x,y,dx,dy = gen_data(200, W, H)

    fig = plt.figure(figsize=(4*W/H, 4))
    anim = animation.FuncAnimation(fig, animate, 
                    fargs=(x, y, dx, dy, W, H),
                    frames=(60 if in_colab else None), 
                    repeat=False, interval=50)
    if in_colab:
        rc('animation', html='jshtml')
        return anim
    else:
        plt.show()

def animate(n, x, y, dx, dy, W, H):   
    NOISE = 0.3        # +/- direction noise radians
    R = 0.10*min(W, H) # neighbors within R
    V = 0.02*min(W, H) # velocity -> displacement in each time step  
    move_all(x, y, dx, dy, V, W, H)
    ax = [0.0]*len(x)
    ay = [0.0]*len(x)
    for k in range(len(x)):
        ax[k],ay[k] = neighbor_average_direction(x, y, dx, dy, k, R)
        t = math.atan2(ay[k],ax[k]) + (NOISE - 2*NOISE*random.random())
        ax[k] = math.cos(t)
        ay[k] = math.sin(t)
    dx[:] = ax   # update the orginal dir vector
    dy[:] = ay
    plt.clf()    # clear figure
    plt.quiver(x, y, dx, dy) # plot a 2D field of arrows
    plt.xlim((0, W))
    plt.ylim((0, H))

#-------------------------------------------

def gen_data(N, W, H):
    x = []
    y = []
    dx = []
    dy = []
    i = 1 
    while i <= N :
        Num_x = random.random() * W
        x.append(Num_x)
        Num_y = random.random() * H
        y.append(Num_y)
        Num_rad = random.random() * 2 * math.pi
        dx.append(math.cos(Num_rad))
        dy.append(math.sin(Num_rad))
        i = i + 1    
    return x , y , dx , dy 


#-------------------------------------------
def move_all(x, y, dx, dy, d, W, H):
    old_x = x.copy()
    old_y  = y.copy()
    x.clear()
    y.clear()
    D_dx = [ i * d for i in dx]
    D_dy = [ n * d for n in dy]
    for j in range(0 , len(old_x)) :
        if old_x[j] + D_dx[j] >= W :
            x.append(old_x[j] + D_dx[j] - W)
        elif old_x[j] + D_dx[j] <= 0 :
            x.append(old_x[j] + D_dx[j] + W)
        else :
            x.append(old_x[j] + D_dx[j])
    for k in range(0 , len(old_y)) :
        if old_y[k] + D_dy[k] >= H :
            y.append(old_y[k] + D_dy[k] - H)
        elif old_y[k] + D_dy[k] <= 0 :
            y.append(old_y[k] + D_dx[k] + H)
        else : 
            y.append(old_y[k] + D_dy[k])
#-------------------------------------------
def neighbor_average_direction(x, y, dx, dy, k, R):
    sigm_dx = []
    sigm_dy = []
    for i in range(0 , len(x)) :
        if (x[i] - x[k])**2 + (y[i] - y[k])**2 <= R**2 :
            sigm_dx.append(dx[i])
            sigm_dy.append(dy[i])
        else :
            continue
    mean_dx = sum(sigm_dx) / len(sigm_dx)
    mean_dy = sum(sigm_dy) / len(sigm_dy)
    return mean_dx , mean_dy

#-------------------------------------------
main()