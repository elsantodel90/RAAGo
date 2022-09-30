import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('Agg')
def floor_ceil(x, delta):
    base = 1
    while abs(base) <= abs(x):
        base += 1
    base *= -delta
    ret = base
    while (base-x) * (ret-x) >= 0:
        ret += delta
    return ret

def strict_floor(x):
    return floor_ceil(x, -1)
    
def strict_ceil(x):
    return floor_ceil(x, 1)

def categ(i):
    return "{} d".format(i+1) if i >= 0 else "{} k".format(-i)

def calculate_ticks(a,b):
    ticks = []
    names = []
    def put_rank(x):
        ticks.append(x)
        names.append("{:.3f}".format(x + (x>0) - (x<0)) if x != 0 else "1.000\n-1.000")
    for i in range(a,b):
        put_rank(i)
        ticks.append(i + 0.5)
        names.append(categ(i))
    put_rank(b)
    return ticks, names

def filterticks(a,b,parity):
    x,y = calculate_ticks(a,b)
    return x[parity::2], y[parity::2]

def calculate_minor_ticks(a,b):
    return filterticks(a,b,1)

def calculate_major_ticks(a,b):
    return filterticks(a,b,0)

def plot_data(rank_dates, rank_data, filename):
    min_rank = min(rank_data)
    max_rank = max(rank_data)
    a = strict_floor(min_rank)
    b = strict_ceil(max_rank)
    #plt.plot([1,2,3,4])
    NEXT_GAP = 0.15
    TO_JUMP = 0.6
    def adjust(limit, x):
        return limit if abs(x-limit) < TO_JUMP else x
    lower_limit = adjust(a, min_rank) - NEXT_GAP 
    upper_limit = adjust(b, max_rank) + NEXT_GAP
    fig, ax = plt.subplots()
    ax.tick_params(which='minor', length=0)
    plt.yticks([])
    plt.yticks(*calculate_minor_ticks(a,b),minor=True)
    plt.yticks(*calculate_major_ticks(a,b),minor=False)
    plt.plot(rank_dates, rank_data, marker="o")

    #plt.tick_params(axis='x', which='minor', bottom=False
    #plt.axes().yaxis.set_ticks([-1,0,1])#.set_minor_locator(matplotlib.ticker.MultipleLocator(1))
    #plt.axes().yaxis.grid(True)
    #  for i,tick in enumerate(plt.axes().yaxis.get_major_ticks()):
    #      if i % 2 == 1:
    #          tick.tick1line.set_markersize(0)
    #          tick.tick2line.set_markersize(0)
    #      else:
    #          tick.gridOn = True
    #
    #      #plt.axhspan(i, i+.2, facecolor='0.2', alpha=0.5)
    #plt.axes().xaxis.get_major_ticks()[1].tick1line.set_markersize(0)
    for i in range(a-1,b+1):
        if i%2 == 0:
            down = max(upper_limit, i)
            up   = min(lower_limit, i+1)
            plt.axhspan(i, i+1, facecolor='gray', alpha=0.25)
    plt.ylim(lower_limit, upper_limit)
    X_BORDER = 5
    plt.xlim(min(rank_dates)-X_BORDER, max(rank_dates)+X_BORDER)
    plt.xticks([])
    #plt.axes().xaxis.set_ticklabels([])
    #plt.axes().xaxis.set_ticks([])

    plt.savefig(filename)
    plt.close()
    return
    #fig = plt.figure(1)
    #plot = fig.add_subplot(111)
    #plot.tick_params(axis='both', which='major', labelsize=8)
    #plt.show()
    #plt.savefig(filename)
    #plt.close()

