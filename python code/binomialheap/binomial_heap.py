"""
binomial_heap.py
Corrected Python implementation of Binomial Heap.
Provides BinomialNode and BinomialHeap with basic operations:
- insert(key)
- extract_min()
- find_min()
- union_heaps(other)
- decrease_key(node, new_key)
- delete_node(node)
- level_order_traversal()
"""

from collections import deque
import sys
import random

INT_MAX = sys.maxsize
INT_MIN = -sys.maxsize - 1


class BinomialNode:
    def __init__(self, key: int):
        self.key = key
        self.degree = 0  # Number of children
        self.parent = None
        self.child = None
        self.sibling = None

    def __repr__(self):
        return f"BinomialNode(key={self.key}, degree={self.degree})"


class BinomialHeap:
    def __init__(self):
        self.head: BinomialNode | None = None

    def _link_trees(self, y: BinomialNode, z: BinomialNode):
        """Link two binomial trees of the same degree.
        Makes y a child of z (assuming z.key <= y.key)"""
        y.parent = z
        y.sibling = z.child
        z.child = y
        z.degree += 1

    def _merge_root_lists(self, h1: BinomialNode | None, h2: BinomialNode | None) -> BinomialNode | None:
        """Merge two root lists in order of increasing degree"""
        if not h1:
            return h2
        if not h2:
            return h1

        # Start with the tree of smaller degree
        if h1.degree <= h2.degree:
            merged = h1
            h1 = h1.sibling
        else:
            merged = h2
            h2 = h2.sibling

        curr = merged

        # Merge the rest by degree
        while h1 and h2:
            if h1.degree <= h2.degree:
                curr.sibling = h1
                h1 = h1.sibling
            else:
                curr.sibling = h2
                h2 = h2.sibling
            curr = curr.sibling

        # Attach remaining trees
        if h1:
            curr.sibling = h1
        else:
            curr.sibling = h2

        return merged

    def _consolidate(self, head: BinomialNode | None) -> BinomialNode | None:
        """Consolidate the heap so no two roots have the same degree"""
        if not head:
            return None

        prev = None
        curr = head
        next_node = curr.sibling

        while next_node:
            # Case 1 & 2: degrees are different, move forward
            if (curr.degree != next_node.degree or 
                (next_node.sibling and next_node.sibling.degree == curr.degree)):
                prev = curr
                curr = next_node
            # Case 3: curr.key <= next.key, link next under curr
            elif curr.key <= next_node.key:
                curr.sibling = next_node.sibling
                self._link_trees(next_node, curr)
            # Case 4: curr.key > next.key, link curr under next
            else:
                if prev is None:
                    head = next_node
                else:
                    prev.sibling = next_node
                self._link_trees(curr, next_node)
                curr = next_node

            next_node = curr.sibling

        return head

    def insert(self, key: int) -> BinomialNode:
        """Insert a new key into the heap"""
        new_node = BinomialNode(key)
        new_node.degree = 0
        
        # Merge with existing heap
        self.head = self._merge_root_lists(self.head, new_node)
        self.head = self._consolidate(self.head)
        
        return new_node

    def find_min(self) -> BinomialNode | None:
        """Find the node with minimum key"""
        if not self.head:
            return None
        
        min_node = self.head
        curr = self.head.sibling
        
        while curr:
            if curr.key < min_node.key:
                min_node = curr
            curr = curr.sibling
        
        return min_node

    def extract_min(self) -> int:
        """Extract and return the minimum key"""
        if not self.head:
            return INT_MAX

        # Find minimum node and its predecessor
        min_node = self.head
        min_prev = None
        curr = self.head
        prev = None

        while curr.sibling:
            if curr.sibling.key < min_node.key:
                min_node = curr.sibling
                min_prev = curr
            prev = curr
            curr = curr.sibling

        # Remove min_node from root list
        if min_node == self.head:
            self.head = min_node.sibling
        else:
            min_prev.sibling = min_node.sibling

        # Reverse the children list of min_node
        child = min_node.child
        new_head = None
        
        while child:
            next_child = child.sibling
            child.sibling = new_head
            child.parent = None
            new_head = child
            child = next_child

        # Merge the reversed children list with the main heap
        self.head = self._merge_root_lists(self.head, new_head)
        self.head = self._consolidate(self.head)

        return min_node.key

    def union_heaps(self, other: 'BinomialHeap') -> BinomialNode | None:
        """Union this heap with another heap"""
        self.head = self._merge_root_lists(self.head, other.head)
        self.head = self._consolidate(self.head)
        other.head = None
        return self.head

    def decrease_key(self, node: BinomialNode | None, new_key: int) -> BinomialNode | None:
        """Decrease the key of a node"""
        if node is None or new_key > node.key:
            return None

        node.key = new_key
        curr = node
        parent = curr.parent

        # Bubble up to maintain heap property
        while parent and curr.key < parent.key:
            # Swap keys
            curr.key, parent.key = parent.key, curr.key
            curr = parent
            parent = curr.parent

        return node

    def delete_node(self, node: BinomialNode | None) -> int:
        """Delete a specific node from the heap"""
        if node is None:
            return INT_MAX
        
        self.decrease_key(node, INT_MIN)
        return self.extract_min()

    def level_order_traversal(self) -> None:
        """Print level-order traversal of the heap"""
        if self.head is None:
            print()
            return

        q = deque()
        q.append((self.head, 0))
        cur_level = -1

        while q:
            node, level = q.popleft()

            if level > cur_level:
                if cur_level >= 0:
                    print()
                cur_level = level
                print(f"Level {cur_level}:", end=" ")

            print(node.key, end=" ")

            # Add child to queue
            if node.child is not None:
                q.append((node.child, level + 1))

            # Add sibling to queue (same level)
            if node.sibling is not None:
                q.append((node.sibling, level))

        print()

    def print_tree(self) -> None:
        """Print heap in tree format with branch characters
        Source - https://stackoverflow.com/a/... (Adrian Schneider, modified)
        License - CC BY-SA 4.0"""
        if self.head is None:
            print("(empty heap)")
            return
        
        # Print each root tree
        root = self.head
        tree_num = 0
        while root:
            print(f"\nBinomial Tree B{root.degree} (root: {root.key}):")
            self._print_subtree(root, "", True)
            root = root.sibling
            tree_num += 1
    
    def _print_subtree(self, node: BinomialNode, prefix: str, is_last: bool) -> None:
        """Recursively print a subtree with tree branch characters"""
        if node is None:
            return
        
        # Print current node
        connector = "└──" if is_last else "├──"
        print(f"{prefix}{connector}{node.key}")
        
        # Prepare prefix for children
        extension = "    " if is_last else "│   "
        new_prefix = prefix + extension
        
        # Get all children as a list
        children = []
        child = node.child
        while child:
            children.append(child)
            child = child.sibling
        
        # Print each child
        for i, child_node in enumerate(children):
            is_last_child = (i == len(children) - 1)
            self._print_subtree(child_node, new_prefix, is_last_child)


if __name__ == '__main__':
    random.seed(42)
    heap = BinomialHeap()
    
    print("Inserting values: ", end="")
    values = []
    for _ in range(10):
        k = random.randint(0, 99)
        values.append(k)
        heap.insert(k)
    print(values)
    
    print("\nHeap structure (tree view):")
    heap.print_tree()
    
    print("\n" + "="*60)
    print("Extracting minimum values:")
    print("="*60)
    while heap.head:
        min_k = heap.extract_min()
        print(f"\nExtracted: {min_k}")
        if heap.head:
            heap.print_tree()
    
    print("\n" + "="*60)
    print("Testing Union")
    print("="*60)
    heap1 = BinomialHeap()
    heap2 = BinomialHeap()
    
    for i in [5, 10, 15]:
        heap1.insert(i)
    for i in [3, 8, 20]:
        heap2.insert(i)
    
    print("\nHeap 1:")
    heap1.print_tree()
    print("\nHeap 2:")
    heap2.print_tree()
    
    heap1.union_heaps(heap2)
    print("\nAfter union:")
    heap1.print_tree()
    
    print("\n" + "="*60)
    print("Testing Decrease Key")
    print("="*60)
    heap3 = BinomialHeap()
    nodes = []
    for i in [50, 30, 20, 10]:
        node = heap3.insert(i)
        nodes.append(node)
    
    print("\nBefore decrease key:")
    heap3.print_tree()
    
    print("\nDecreasing key of node with value 50 to 5:")
    heap3.decrease_key(nodes[0], 5)
    heap3.print_tree()
    print(f"\nNew minimum: {heap3.find_min().key}")