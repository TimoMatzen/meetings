import statistics
import math


class Instance():
    def __init__(self, id, value):
        self.id = id
        self.value = value

    def __str__(self):
        return f"Instance(id={self.id}, value={self.value})"

class Node:
    def __init__(self, ranges):
        self.left = None
        self.right = None
        self.ranges = ranges
        self.instances = []

    def isLeaf(self):
        return not self.left and not self.right

    def __str__(self):
        return f"Node(ranges={self.ranges}, n={len(self.instances)})"


class Tree:
    def __init__(self, ranges, min_range=0, split_k=2):
        if not ranges:
            raise ValueError("invalid ranges")
        if isinstance(min_range, int) or isinstance(min_range, float):
            min_range = [min_range] * len(ranges)
        if not isinstance(min_range, list) or any(not isinstance(x, int) and not isinstance(x, float) for x in min_range):
            raise ValueError("invalid min_range type, should be int, float, List[int] or List[float]")
        if any(x < 0 for x in min_range):
            raise ValueError("min_range can not be negative")
        if len(min_range) != len(ranges):
            raise ValueError("dimension mismatch: ranges and min_range")
        if split_k < 2:
            raise ValueError("k should be larger then 1")
        self.root = Node(ranges)
        self.min_ranges = min_range
        self.split_k = split_k

    def getNeigbors(self, instance, max_dim_dis, euclidean_dis=None, euclidean_dims=None):
        if isinstance(max_dim_dis, int) or isinstance(max_dim_dis, float):
            max_dim_dis = [max_dim_dis] * self.getDimensionCount()
        if not isinstance(max_dim_dis, list):
            raise ValueError("invalid max_dim_dis type")
        if any(x < 0 for x in max_dim_dis):
            raise ValueError("max_dim_dis can not be negative")
        if len(instance.value) != len(max_dim_dis):
            raise ValueError("dimension mismatch: instance.value and max_dim_dis")
        if euclidean_dis is None:
            euclidean_dis = 0
        if euclidean_dis < 0:
            raise ValueError("euclidean_dis should be positive")
        if euclidean_dims is None:
            euclidean_dims = []
        if not isinstance(euclidean_dims, list) or any(not isinstance(x, int) or int(x) < 0 or int(x) >= self.getDimensionCount() for x in euclidean_dims):
            raise ValueError("invalid euclidean_dims")

        area = [(x-r, x+r) for x, r in zip(instance.value, max_dim_dis)]
        neighbors = [i for leaf in self._getLeafsInArea(area, self.root) for i in leaf.instances \
            if all([r[0] <= v < r[1] for r, v in zip(area, i.value)]) and \
               math.sqrt(sum((instance.value[d] - i.value[d]) ** 2 for d in euclidean_dims)) <= euclidean_dis
        ]

        return neighbors

    def _getLeafsInArea(self, area, node):
        if node.isLeaf():
            yield node
        else:
            if all([a[0] <= r[1] for a, r in zip(area, node.left.ranges)]):
                yield from self._getLeafsInArea(area, node.left)
            if all([a[1] >= r[0] for a, r in zip(area, node.right.ranges)]):
                yield from self._getLeafsInArea(area, node.right)

    def add(self, instance):
        self._add(instance, self.root)

    def _add(self, instance, node):
        leaf = self._find(instance, node)
        leaf.instances.append(instance)
        if self._shouldSplit(leaf):
            self._split(leaf)

    def find(self, instance):
        return self._find(instance, self.root)

    def _find(self, instance, node):
        if node.isLeaf():
            return node
        elif (self._inNode(instance, node.left)):
            return self._find(instance, node.left)
        elif (self._inNode(instance, node.right)):
            return self._find(instance, node.right)
        raise ValueError('Node not found!')

    def _inNode(self, instance, node):
        return all([v >= r[0] and v < r[1] for v, r in zip(instance.value, node.ranges)])

    def _split(self, node):
        dim, value = self._getSplit(node)
        node.left = Node([((r[0], value) if i == dim else r) for i, r in enumerate(node.ranges)])
        node.right = Node([((value, r[1]) if i == dim else r) for i, r in enumerate(node.ranges)])
        while node.instances:
            self._add(node.instances.pop(), node)

    def _shouldSplit(self, node):
        return len(node.instances) >= self.split_k and \
            any(r[1] - r[0] > mr * 2 for mr, r in zip(self.min_ranges, node.ranges))

    def _getSplit(self, node):
        best_dim = -1
        best_score = float('-inf')
        best_split_point = float('-inf')
        for dim in range(len(node.ranges)):
            if node.ranges[dim][1] - node.ranges[dim][0] < self.min_ranges[dim] * 2:
                continue
            values = [x.value[dim] for x in node.instances]
            score = statistics.variance(values)
            if score > best_score:
                best_dim = dim
                best_score = score
                best_split_point = statistics.mean(values)
        
        if best_split_point - node.ranges[best_dim][0] < self.min_ranges[best_dim]:
            best_split_point = node.ranges[best_dim][0] + self.min_ranges[best_dim]
        if node.ranges[best_dim][1] - best_split_point < self.min_ranges[best_dim]:
            best_split_point = node.ranges[best_dim][1] - self.min_ranges[best_dim]

        return best_dim, best_split_point

    def getLeafs(self):
        return self._getLeafs(self.root)

    def _getLeafs(self, node): 
        if node.isLeaf():
            yield node
        if node.left:
            yield from self._getLeafs(node.left)
        if node.right:
            yield from self._getLeafs(node.right)

    def getDimensionCount(self):
        return len(self.min_ranges)

    def __str__(self):
        return self.___str__(self.root, 0)

    def ___str__(self, node, depth):
        value = (("-" * (depth) * 2) + str(node))
        if node.left:
            value += "\n" + self.___str__(node.left, depth + 1)
        if node.right:
            value += "\n" + self.___str__(node.right, depth + 1)
        return value