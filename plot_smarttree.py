import random
from src import utils, parser
from src.parser import parse, read_file
from src.smarttree import Tree, Instance
from src.utils import get_user, plt_files
import matplotlib.patches as patches
import matplotlib.pyplot as plt

##### constants

# Data
random.seed(1000)
ranges = [(-90, 90), (-180, 180)]       # min and max value for each dimension
num_samples = 10000                     # number of instances

# Tree building
min_range = 0.1                         # do not split when a dimension becomes smaler then x
split_k = 5                             # split when a node has x instances

# Search
neighbor_radius = 0.01                  # max distance for an instance to be a neighbor; in euclidean space
neighbor_distance = neighbor_radius     # max distance for an instance to be a neighbor; per dimension

# Plotting
draw_interval = 100                     # draw every x instances
draw_delay = 0.1                        # time in seconds to wait after a draw

##### Create data

def get_data():
    cnt = 0
    path = 'data/Geolife Trajectories 1.3/Data'
    for file in plt_files(path):
        user_id = get_user(file)
        for lat, lon, _, d, t in read_file(file):
            if cnt >= num_samples:
                break
            if event := parse(user_id, lat, lon, d, t):
                cnt += 1
                yield Instance(event.user_id, [event.location.lat, event.location.lon])

def get_mock_data():
    return [Instance(i, [r[0] + random.random() * (r[1] - r[0]) for r in ranges]) for i in range(num_samples)]

data = get_data()
#data = get_mock_data()

##### Plotting
fig = plt.figure()
ax = plt.subplot()

plot_ranges = [(float('inf'), float('-inf')) for d in range(2)]
plotted_rectangles = set()
plotted_poi_items = []

def update_plot(tree, instances):
    ax.set_xlim(plot_ranges[0][0], plot_ranges[0][1])
    ax.set_ylim(plot_ranges[1][0], plot_ranges[1][1])

    ax.scatter([i.value[0] for i in instances], [i.value[1] for i in instances], c='blue')

    for leaf in tree.getLeafs():
        x, y = leaf.ranges[0][0], leaf.ranges[1][0]
        w, h = leaf.ranges[0][1] - leaf.ranges[0][0], leaf.ranges[1][1] - leaf.ranges[1][0]
        if (x, y, w, h) not in plotted_rectangles:
            plotted_rectangles.add((x, y, w, h))
            rect = patches.Rectangle((x, y), w, h, linewidth=1, edgecolor='grey', facecolor='none')
            ax.add_patch(rect)

    plt.draw()
    plt.pause(draw_delay)

def onclick(event):
    global plotted_poi_items
    while plotted_poi_items:
        plotted_poi_items.pop().remove()

    if not event.inaxes:
        return

    poi = Instance(None, [event.xdata, event.ydata])
    neighbors = tree.getNeigbors(poi, neighbor_distance, neighbor_radius, [0, 1] if neighbor_radius else [])

    #print(f"Point of interest: {str(poi)}")
    #print(f"Neighbors:\n {[str(x) for x in neighbors]}")

    plotted_poi_items.append(ax.scatter([poi.value[0]], [poi.value[1]], c='red'))
    plotted_poi_items.append(ax.scatter([n.value[0] for n in neighbors], [n.value[1] for n in neighbors], c='green'))
    x, y, w = poi.value[0] - neighbor_distance, poi.value[1] - neighbor_distance, neighbor_distance * 2
    plotted_poi_items.append(ax.add_patch(patches.Rectangle((x, y), w, w, linewidth=1, edgecolor='yellow', facecolor='none')))

    if neighbor_radius:
        plotted_poi_items.append(ax.add_patch(patches.Circle((poi.value[0], poi.value[1]), neighbor_radius, linewidth=1, edgecolor='red', facecolor='none')))

    plt.draw()

cid = fig.canvas.mpl_connect('button_press_event', onclick)

##### Build tree
tree = Tree(ranges, min_range, split_k)

plot_data = []
for i, instance in enumerate(data):
    tree.add(instance)

    plot_data.append(instance)
    if (i+1) % draw_interval == 0 or i == num_samples - 1:
        plot_ranges = [(min(plot_ranges[d][0], *[i.value[d] for i in plot_data]), max(plot_ranges[d][1], *[i.value[d] for i in plot_data])) for d in range(2)]
        update_plot(tree, plot_data)
        plot_data.clear()

#print(f"Tree: \n{tree}")

plt.show()