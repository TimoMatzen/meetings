import random
from src.smarttree import Tree 
import matplotlib.patches as patches
import matplotlib.pyplot as plt


# constants
random.seed(1000)
num_samples = 100
ranges = [(0, 10), (10, 20)]
min_range = 0.1
split_k = 5

# create mock data
mock_data = [[r[0] + random.random() * (r[1] - r[0]) for r in ranges] for _ in range(num_samples)]
print(f"mock_data:\n {mock_data}")

# plotting
fig = plt.figure()
ax = plt.subplot()
ax.set_xlim(ranges[0][0], ranges[0][1])
ax.set_ylim(ranges[1][0], ranges[1][1])

def update_plot(tree, instances):
    ax.scatter([inst[0] for inst in instances], [inst[1] for inst in instances])

    for leaf in tree.getLeafs():
        x, y = leaf.ranges[0][0], leaf.ranges[1][0]
        w, h = leaf.ranges[0][1] - leaf.ranges[0][0], leaf.ranges[1][1] - leaf.ranges[1][0]
        rect = patches.Rectangle((x, y), w, h, linewidth=1, edgecolor='r', facecolor='none')
        ax.add_patch(rect)

    plt.draw()
    plt.pause(0.1)

# build tree
tree = Tree(ranges, min_range, split_k)

for i, instance in enumerate(mock_data):
    tree.add(instance)
    if i % 1 == 0 or i == len(mock_data) - 1:
        update_plot(tree, mock_data[:i+1])

print(tree)
plt.show()