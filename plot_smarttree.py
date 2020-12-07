import random
from src.smarttree import Tree, Instance
import matplotlib.patches as patches
import matplotlib.pyplot as plt


# constants
random.seed(1000)
num_samples = 100              # number of instances in the mock data
ranges = [(0, 10), (10, 20)]    # min and max value for each dimension
min_range = 0.1                 # do not split when a dimension becomes smaler then x  
split_k = 5                     # split when a node has x instances 
neighbor_distance = 1           # max distance for an instance to be a neighbor; per dimension
neighbor_radius = 1             # max distance for an instance to be a neighbor; in euclidean space
draw_interval = 100             # draw every x instances
draw_delay = 0.1                # time in seconds to wait after a draw


# create mock data
mock_data = [Instance(i, [r[0] + random.random() * (r[1] - r[0]) for r in ranges]) for i in range(num_samples)]
#print(f"mock_data:\n {[str(x) for x in mock_data]}")

# plotting
fig = plt.figure()
ax = plt.subplot()
ax.set_xlim(ranges[0][0], ranges[0][1])
ax.set_ylim(ranges[1][0], ranges[1][1])

plotted_rectangles = set()
plotted_poi_items = []

def update_plot(tree, instances):
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

# build tree
tree = Tree(ranges, min_range, split_k)

for i, instance in enumerate(mock_data):
    tree.add(instance)
    if (i+1) % draw_interval == 0 or i == len(mock_data) - 1:
        update_plot(tree, mock_data[i+1-draw_interval:i+1])

#print(f"Tree: \n{tree}")

plt.show()