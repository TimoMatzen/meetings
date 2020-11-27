import random
from src.smarttree import Tree, Instance
import matplotlib.patches as patches
import matplotlib.pyplot as plt


# constants
random.seed(1000)
num_samples = 300
ranges = [(0, 10), (10, 20)]
min_range = 0.1
split_k = 5

# create mock data
mock_data = [Instance(i, [r[0] + random.random() * (r[1] - r[0]) for r in ranges]) for i in range(num_samples)]
print(f"mock_data:\n {[str(x) for x in mock_data]}")

# plotting
fig = plt.figure()
ax = plt.subplot()
ax.set_xlim(ranges[0][0], ranges[0][1])
ax.set_ylim(ranges[1][0], ranges[1][1])

def update_plot(tree, instances):
    ax.scatter([i.value[0] for i in instances], [i.value[1] for i in instances], c='blue')

    for leaf in tree.getLeafs():
        x, y = leaf.ranges[0][0], leaf.ranges[1][0]
        w, h = leaf.ranges[0][1] - leaf.ranges[0][0], leaf.ranges[1][1] - leaf.ranges[1][0]
        rect = patches.Rectangle((x, y), w, h, linewidth=1, edgecolor='grey', facecolor='none')
        ax.add_patch(rect)

    plt.draw()
    plt.pause(0.1)

# build tree
tree = Tree(ranges, min_range, split_k)

for i, instance in enumerate(mock_data):
    tree.add(instance)
    if i % 1000 == 0 or i == len(mock_data) - 1:
        update_plot(tree, mock_data[:i+1])

print(f"Tree: \n{tree}")

# find neighbors
poi = Instance(None, [4, 16])
max_dist = 1
neighbors = tree.getNeigbors(poi, max_dist)

print(f"Point of interest: {str(poi)}")
print(f"Neighbors:\n {[str(x) for x in neighbors]}")

ax.scatter([poi.value[0]], [poi.value[1]], c='red')
x, y = poi.value[0] - max_dist, poi.value[1] - max_dist
w, h = max_dist * 2, max_dist * 2
rect = patches.Rectangle((x, y), w, h, linewidth=1, edgecolor='red', facecolor='none')
ax.add_patch(rect)
plt.draw()

plt.show()