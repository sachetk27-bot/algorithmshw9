import random
from typing import Optional


class Node:
    def __init__(self, key: int, is_head: bool = False):
        self.key: int = key
        self.isHead: bool = is_head
        self.right: Optional[Node] = None
        self.left: Optional[Node] = None
        self.up: Optional[Node] = None
        self.down: Optional[Node] = None

    def __repr__(self) -> str:
        return f"Head" if self.isHead else f"Node({self.key})"


class SkipList:
    def __init__(self):
        self.head0 = Node(0, is_head=True)
        self.headh = self.head0
        self.level = 0
        random.seed()

    def flip_coin(self) -> bool:
        return random.randint(0, 1) == 1

    def print_list(self) -> None:
        head = self.headh
        level = self.level
        print("Skip list current state is:")
        while head is not None:
            print(f"Level {level} :", end="")
            tmp = head.right
            while tmp is not None:
                print(f" {tmp.key}", end="")
                tmp = tmp.right
            print()
            head = head.down
            level -= 1
        print()

    def find(self, key: int) -> Optional[Node]:
        """Find a node with given key; if not found return the node after which insertion should happen at lowest level"""
        print(f"Starting to search {key} ....")
        tmp = self.headh
        
        while tmp is not None:
            if tmp.right is not None and tmp.right.key <= key:
                print("Go right")
                tmp = tmp.right
            elif tmp.down is not None:
                print("Go down")
                tmp = tmp.down
            else:
                break
        
        if tmp is not None and not tmp.isHead and tmp.key == key:
            print("Found the key")
            return tmp
        else:
            print("Not found.")
            return tmp

    def _create_node(self, key: int) -> Node:
        return Node(key)

    def _create_head(self) -> Node:
        return Node(0, is_head=True)

    def _insert_new_level(self, tmp: Node) -> None:
        newnode = self._create_node(tmp.key)
        tmp.up = newnode
        newnode.down = tmp

        leftone = tmp.left
        while leftone is not None and not leftone.isHead and leftone.up is None:
            leftone = leftone.left
        
        if leftone is None:
            return

        if leftone.isHead and leftone.up is None:
            newhead = self._create_head()
            leftone.up = newhead
            newhead.down = leftone
            newhead.right = newnode
            newnode.left = newhead
            self.headh = newhead
            self.level += 1
        else:
            leftone = leftone.up
            newnode.right = leftone.right
            leftone.right = newnode
            if newnode.right is not None:
                newnode.right.left = newnode
            newnode.left = leftone

        if self.flip_coin():
            self._insert_new_level(newnode)

    def insert(self, key: int) -> None:
        tmp = self.find(key)
        if tmp is None:
            print("Error: bad find() result")
            return
        if not tmp.isHead and tmp.key == key:
            print(f"Item {key} already present in the list.")
            self.print_list()
            return

        newnode = self._create_node(key)
        newnode.left = tmp
        if tmp.right is not None:
            newnode.right = tmp.right
            newnode.right.left = newnode
        tmp.right = newnode

        if self.flip_coin():
            self._insert_new_level(newnode)

        self.print_list()

    def _check_head(self) -> None:
        tmp = self.headh
        while tmp is not None and tmp.right is None and tmp.down is not None:
            tmpdown = tmp.down
            tmpdown.up = None
            tmp.down = None
            tmp = tmpdown
            self.level -= 1
        self.headh = tmp

    def delete(self, key: int) -> None:
        tmp = self.find(key)
        if tmp is None or tmp.isHead or tmp.key != key:
            print("No such Item.")
            self.print_list()
            return
        
        while tmp is not None:
            tmpup = tmp.up
            if tmp.left is not None:
                tmp.left.right = tmp.right
            if tmp.right is not None:
                tmp.right.left = tmp.left
            tmp.left = tmp.right = tmp.up = tmp.down = None
            tmp = tmpup
        
        self._check_head()
        self.print_list()

    def run_cli(self) -> None:
        print("Simple SkipList CLI. Commands: insert x, delete x, find x, print, quit")
        while True:
            try:
                line = input("\nEnter your command: ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\nExiting...")
                break
            if not line:
                continue
            parts = line.split()
            cmd = parts[0].lower()
            if cmd == 'insert' and len(parts) > 1:
                try:
                    k = int(parts[1])
                except ValueError:
                    print("Invalid number")
                    continue
                self.insert(k)
            elif cmd == 'delete' and len(parts) > 1:
                try:
                    k = int(parts[1])
                except ValueError:
                    print("Invalid number")
                    continue
                self.delete(k)
            elif cmd == 'find' and len(parts) > 1:
                try:
                    k = int(parts[1])
                except ValueError:
                    print("Invalid number")
                    continue
                result = self.find(k)
                if result and not result.isHead and result.key == k:
                    print(f"Key {k} exists in the list")
                else:
                    print(f"Key {k} not found in the list")
                print()
            elif cmd == 'print':
                self.print_list()
            elif cmd == 'quit':
                print("Goodbye!")
                break
            else:
                print("Please enter a valid command: insert x, delete x, find x, print, quit")


if __name__ == '__main__':
    sl = SkipList()
    sl.run_cli()