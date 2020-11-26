import os
import itertools
import statistics
import matplotlib.patches as patches
import matplotlib.pyplot as plt


class Node:
    def __init__(self, ranges):
        self.left = None
        self.right = None
        self.ranges = ranges
        self.instances = []

    def __str__(self):
        return f"Node(ranges={self.ranges}, num_instances={len(self.instances)})"

    def isLeaf(self):
        return not self.left and not self.right

class Tree:
    def __init__(self, ranges, min_range, split_k):
        if not ranges:
            raise ValueError("invalid ranges")
        if not min_range:
            raise ValueError("invalid min_range")
        if split_k < 2:
            raise ValueError("k should be larger then 1")
        if isinstance(min_range, int) or isinstance(min_range, float):
            min_range = [min_range] * len(ranges)
        if not isinstance(min_range, list):
            raise ValueError("invalid min_range type")
        if len(min_range) != len(ranges):
            raise ValueError("dimension mismatch: ranges and min_range")

        self.root = Node(ranges)
        self.min_ranges = min_range
        self.split_k = split_k

    def getRoot(self):
        return self.root

    def getDimensionCount():
        return len(self.min_ranges)

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
        elif (self._inRange(instance, node.left)):
            return self._find(instance, node.left)
        elif (self._inRange(instance, node.right)):
            return self._find(instance, node.right)
        raise ValueError('Node not found!')

    def _inRange(self, instance, node):
        return all([v >= r[0] and v < r[1] for v, r in zip(instance, node.ranges)])

    def _split(self, node):
        dim, value = self._getSplit(node)
        node.left = Node([((r[0], value) if i == dim else r) for i, r in enumerate(node.ranges)])
        node.right = Node([((value, r[1]) if i == dim else r) for i, r in enumerate(node.ranges)])
        while node.instances:
            self._add(node.instances.pop(), node)
        node.instances = []

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
            values = [x[dim] for x in node.instances]
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

    def __str__(self):
        return self.___str__(self.root, 0)

    def ___str__(self, node, depth):
        value = (("-" * (depth) * 2) + str(node))
        if node.left:
            value += "\n" + self.___str__(node.left, depth + 1)
        if node.right:
            value += "\n" + self.___str__(node.right, depth + 1)
        return value