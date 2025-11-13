from enum import Enum


class Color(Enum):
    """Enum for node colors"""
    RED = 0
    BLACK = 1


class Node:
    """Node class for Red-Black Tree"""
    
    def __init__(self, key: int):
        """
        Initialize a node
        
        Args:
            key: Integer key value for the node
        """
        self.key = key
        self.color = Color.RED
        self.left = None
        self.right = None
        self.parent = None


class RedBlackTree:
    """Red-Black Tree implementation with insertion, deletion, and search"""
    
    def __init__(self):
        """Initialize empty Red-Black Tree"""
        self.root = None
    
    def left_rotate(self, x: Node) -> None:
        """
        Perform left rotation on node x
        
        Args:
            x: Node to rotate
        """
        if x is None or x.right is None:
            return
            
        y = x.right
        x.right = y.left
        
        if y.left is not None:
            y.left.parent = x
        
        y.parent = x.parent
        
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        
        y.left = x
        x.parent = y
    
    def right_rotate(self, y: Node) -> None:
        """
        Perform right rotation on node y
        
        Args:
            y: Node to rotate
        """
        if y is None or y.left is None:
            return
            
        x = y.left
        y.left = x.right
        
        if x.right is not None:
            x.right.parent = y
        
        x.parent = y.parent
        
        if y.parent is None:
            self.root = x
        elif y == y.parent.left:
            y.parent.left = x
        else:
            y.parent.right = x
        
        x.right = y
        y.parent = x
    
    def insert(self, key: int) -> None:
        """
        Insert a key into the tree
        
        Args:
            key: Key to insert
        """
        z = Node(key)
        
        y = None
        x = self.root
        
        while x is not None:
            y = x
            if z.key < x.key:
                x = x.left
            else:
                x = x.right
        
        z.parent = y
        
        if y is None:
            self.root = z
        elif z.key < y.key:
            y.left = z
        else:
            y.right = z
        
        self.fix_insert(z)
    
    def fix_insert(self, z: Node) -> None:
        """
        Fix Red-Black Tree properties after insertion
        
        Args:
            z: Newly inserted node
        """
        while z != self.root and z.parent is not None and z.parent.color == Color.RED:
            if z.parent.parent is None:
                break
                
            if z.parent == z.parent.parent.left:
                y = z.parent.parent.right
                if y is not None and y.color == Color.RED:
                    z.parent.color = Color.BLACK
                    y.color = Color.BLACK
                    z.parent.parent.color = Color.RED
                    z = z.parent.parent
                else:
                    if z == z.parent.right:
                        z = z.parent
                        self.left_rotate(z)
                    if z.parent is not None and z.parent.parent is not None:
                        z.parent.color = Color.BLACK
                        z.parent.parent.color = Color.RED
                        self.right_rotate(z.parent.parent)
            else:
                y = z.parent.parent.left
                if y is not None and y.color == Color.RED:
                    z.parent.color = Color.BLACK
                    y.color = Color.BLACK
                    z.parent.parent.color = Color.RED
                    z = z.parent.parent
                else:
                    if z == z.parent.left:
                        z = z.parent
                        self.right_rotate(z)
                    if z.parent is not None and z.parent.parent is not None:
                        z.parent.color = Color.BLACK
                        z.parent.parent.color = Color.RED
                        self.left_rotate(z.parent.parent)
        
        if self.root is not None:
            self.root.color = Color.BLACK
    
    def delete(self, key: int) -> None:
        """
        Delete a key from the tree
        
        Args:
            key: Key to delete
        """
        z = self.search(key)
        if z is None:
            return
        
        y = None
        x = None
        x_parent = None
        
        if z.left is None or z.right is None:
            y = z
        else:
            y = self.successor(z)
        
        if y.left is not None:
            x = y.left
        else:
            x = y.right
        
        if x is not None:
            x.parent = y.parent
        else:
            x_parent = y.parent
        
        if y.parent is None:
            self.root = x
        elif y == y.parent.left:
            y.parent.left = x
        else:
            y.parent.right = x
        
        if y != z:
            z.key = y.key
        
        if y.color == Color.BLACK:
            if x is not None:
                self.fix_delete(x)
            elif x_parent is not None:
                self.fix_delete_null(x_parent)
    
    def remove(self, key: int) -> None:
        """Alias for delete() method for compatibility with tests"""
        self.delete(key)
    
    def fix_delete(self, x: Node) -> None:
        """
        Fix Red-Black Tree properties after deletion
        
        Args:
            x: Node where fixing starts
        """
        while x is not None and x != self.root and x.color == Color.BLACK:
            if x.parent is None:
                break
                
            if x == x.parent.left:
                w = x.parent.right
                if w is None:
                    break
                if w.color == Color.RED:
                    w.color = Color.BLACK
                    x.parent.color = Color.RED
                    self.left_rotate(x.parent)
                    w = x.parent.right
                if w is None:
                    break
                if (w.left is None or w.left.color == Color.BLACK) and \
                   (w.right is None or w.right.color == Color.BLACK):
                    w.color = Color.RED
                    x = x.parent
                else:
                    if w.right is None or w.right.color == Color.BLACK:
                        if w.left is not None:
                            w.left.color = Color.BLACK
                        w.color = Color.RED
                        self.right_rotate(w)
                        w = x.parent.right
                    if w is not None:
                        if w.right is not None:
                            w.right.color = Color.BLACK
                        w.color = x.parent.color
                        x.parent.color = Color.BLACK
                        self.left_rotate(x.parent)
                    x = self.root
            else:
                w = x.parent.left
                if w is None:
                    break
                if w.color == Color.RED:
                    w.color = Color.BLACK
                    x.parent.color = Color.RED
                    self.right_rotate(x.parent)
                    w = x.parent.left
                if w is None:
                    break
                if (w.right is None or w.right.color == Color.BLACK) and \
                   (w.left is None or w.left.color == Color.BLACK):
                    w.color = Color.RED
                    x = x.parent
                else:
                    if w.left is None or w.left.color == Color.BLACK:
                        if w.right is not None:
                            w.right.color = Color.BLACK
                        w.color = Color.RED
                        self.left_rotate(w)
                        w = x.parent.left
                    if w is not None:
                        if w.left is not None:
                            w.left.color = Color.BLACK
                        w.color = x.parent.color
                        x.parent.color = Color.BLACK
                        self.right_rotate(x.parent)
                    x = self.root
        
        if x is not None:
            x.color = Color.BLACK
    
    def fix_delete_null(self, parent: Node) -> None:
        """
        Fix Red-Black Tree properties when deleting a node with null child
        
        Args:
            parent: Parent of the deleted node
        """
        x = None
        while parent is not None and parent != self.root:
            if parent.parent is None:
                break
                
            if parent == parent.parent.left:
                w = parent.parent.right
                if w is None:
                    break
                if w.color == Color.RED:
                    w.color = Color.BLACK
                    parent.parent.color = Color.RED
                    self.left_rotate(parent.parent)
                    w = parent.parent.right
                if w is None:
                    break
                if (w.left is None or w.left.color == Color.BLACK) and \
                   (w.right is None or w.right.color == Color.BLACK):
                    w.color = Color.RED
                    parent = parent.parent
                else:
                    if w.right is None or w.right.color == Color.BLACK:
                        if w.left is not None:
                            w.left.color = Color.BLACK
                        w.color = Color.RED
                        self.right_rotate(w)
                        if parent.parent is not None:
                            w = parent.parent.right
                    if w is not None and parent.parent is not None:
                        if w.right is not None:
                            w.right.color = Color.BLACK
                        w.color = parent.parent.color
                        parent.parent.color = Color.BLACK
                        self.left_rotate(parent.parent)
                    break
            else:
                w = parent.parent.left
                if w is None:
                    break
                if w.color == Color.RED:
                    w.color = Color.BLACK
                    parent.parent.color = Color.RED
                    self.right_rotate(parent.parent)
                    w = parent.parent.left
                if w is None:
                    break
                if (w.right is None or w.right.color == Color.BLACK) and \
                   (w.left is None or w.left.color == Color.BLACK):
                    w.color = Color.RED
                    parent = parent.parent
                else:
                    if w.left is None or w.left.color == Color.BLACK:
                        if w.right is not None:
                            w.right.color = Color.BLACK
                        w.color = Color.RED
                        self.left_rotate(w)
                        if parent.parent is not None:
                            w = parent.parent.left
                    if w is not None and parent.parent is not None:
                        if w.left is not None:
                            w.left.color = Color.BLACK
                        w.color = parent.parent.color
                        parent.parent.color = Color.BLACK
                        self.right_rotate(parent.parent)
                    break
    
    def search(self, key: int) -> Node:
        """
        Search for a key in the tree
        
        Args:
            key: Key to search for
            
        Returns:
            Node with the key or None if not found
        """
        temp = self.root
        while temp is not None and temp.key != key:
            if key < temp.key:
                temp = temp.left
            else:
                temp = temp.right
        return temp
    
    def find_min(self, node: Node) -> Node:
        """
        Find node with minimum key in subtree
        
        Args:
            node: Root of subtree
            
        Returns:
            Node with minimum key
        """
        if node is None:
            return None
        temp = node
        while temp.left is not None:
            temp = temp.left
        return temp
    
    def find_max(self, node: Node) -> Node:
        """
        Find node with maximum key in subtree
        
        Args:
            node: Root of subtree
            
        Returns:
            Node with maximum key
        """
        if node is None:
            return None
        temp = node
        while temp.right is not None:
            temp = temp.right
        return temp
    
    def get_height(self, x: Node) -> int:
        """
        Get height of subtree rooted at x
        
        Args:
            x: Root of subtree
            
        Returns:
            Height of subtree
        """
        if x is None:
            return -1
        else:
            left_height = self.get_height(x.left)
            right_height = self.get_height(x.right)
            return max(left_height, right_height) + 1
    
    def find_min_value(self) -> None:
        """Print minimum value in tree"""
        if self.root is None:
            print("\nTree empty")
            return
        
        node = self.find_min(self.root)
        if node is not None:
            print(f"\nMinimum value in the tree is: {node.key}")
        else:
            print("\nThe tree is empty")
    
    def find_max_value(self) -> None:
        """Print maximum value in tree"""
        if self.root is None:
            print("\nTree empty")
            return
        
        node = self.find_max(self.root)
        if node is not None:
            print(f"\nMaximum value in the tree is: {node.key}")
        else:
            print("\nThe tree is empty")
    
    def print_height(self) -> None:
        """Print height of tree"""
        if self.root is None:
            print("\nTree empty")
            return
        
        height = self.get_height(self.root)
        if height == -1:
            print("\nThe tree is empty")
        else:
            print(f"\nThe height of the tree is: {height}")
    
    def successor(self, node: Node) -> Node:
        """
        Find successor of a node
        
        Args:
            node: Node to find successor for
            
        Returns:
            Successor node or None
        """
        if node is None:
            return None
        if node.right is not None:
            return self.find_min(node.right)
        else:
            y = node.parent
            while y is not None and node == y.right:
                node = y
                y = y.parent
            return y
    
    def predecessor(self, node: Node) -> Node:
        """
        Find predecessor of a node
        
        Args:
            node: Node to find predecessor for
            
        Returns:
            Predecessor node or None
        """
        if node is None:
            return None
        if node.left is not None:
            return self.find_max(node.left)
        
        temp = node.parent
        while temp is not None and node == temp.left:
            node = temp
            temp = temp.parent
        return temp
    
    def find_successor(self, key: int) -> None:
        """
        Find and print successor of a key
        
        Args:
            key: Key to find successor for
        """
        node = self.search(key)
        if node is not None:
            succ = self.successor(node)
            if succ is not None:
                print(f"\nThe Successor of {key} is : {succ.key}")
            else:
                print("\nNo successor for requested key")
        else:
            print("\nThe requested key does not exist")
    
    def find_predecessor(self, key: int) -> None:
        """
        Find and print predecessor of a key
        
        Args:
            key: Key to find predecessor for
        """
        node = self.search(key)
        if node is not None:
            pred = self.predecessor(node)
            if pred is not None:
                print(f"\nThe Predecessor of {key} is : {pred.key}")
            else:
                print("\nNo predecessor for requested key")
        else:
            print("\nThe requested key does not exist")
    
    def sort(self) -> None:
        """Print tree in sorted (in-order) manner"""
        self.in_order_traversal(self.root)
    
    def in_order_traversal(self, node: Node) -> None:
        """
        In-order traversal of tree
        
        Args:
            node: Current node
        """
        if node is None:
            return
        
        self.in_order_traversal(node.left)
        color_str = "Red" if node.color == Color.RED else "Black"
        print(f"( {node.key} , {color_str} )")
        self.in_order_traversal(node.right)
    
    def print_tree(self) -> None:
        """Print tree structure in a visual format"""
        if self.root is None:
            print("Tree is empty")
            return
        print("\n" + "="*60)
        print("TREE STRUCTURE:")
        print("="*60)
        self._print_tree_helper(self.root, "", True)
        print("="*60 + "\n")
    
    def _print_tree_helper(self, node: Node, prefix: str, is_tail: bool) -> None:
        """
        Helper function to print tree structure recursively
        
        Args:
            node: Current node
            prefix: Prefix for indentation
            is_tail: Whether this is the last child
        """
        if node is None:
            return
        
        color_indicator = "🔴" if node.color == Color.RED else "⚫"
        
        print(prefix + ("└── " if is_tail else "├── ") + f"{color_indicator} {node.key}")
        
        has_left = node.left is not None
        has_right = node.right is not None
        
        extension = "    " if is_tail else "│   "
        
        if has_left:
            self._print_tree_helper(node.left, prefix + extension, not has_right)
        if has_right:
            self._print_tree_helper(node.right, prefix + extension, True)
    
    def print_tree_compact(self) -> None:
        """Print tree structure in a more compact format"""
        if self.root is None:
            print("Tree is empty")
            return
        print("\nTree (In-Order): ", end="")
        self._compact_helper(self.root)
        print()
    
    def _compact_helper(self, node: Node) -> None:
        """
        Helper function to print tree in compact format
        
        Args:
            node: Current node
        """
        if node is None:
            return
        
        self._compact_helper(node.left)
        color_char = "R" if node.color == Color.RED else "B"
        print(f"({node.key}{color_char}) ", end="")
        self._compact_helper(node.right)