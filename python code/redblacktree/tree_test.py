from pathlib import Path
from red_black_tree import RedBlackTree


def main():
    """Main function for interactive tree testing"""
    
    tree = RedBlackTree()
    
    script_dir = Path(__file__).parent.absolute()
    input_file = script_dir / "input.txt"
    
    try:
        with open(input_file, 'r') as f:
            numbers = list(map(int, f.read().split()))
            for x in numbers:
                tree.insert(x)
        print(f"Loaded {len(numbers)} values from input.txt")
        tree.print_tree()
        tree.print_height()
    except FileNotFoundError:
        print(f"File not found: {input_file}")
        print("Starting with empty tree.")
    except ValueError:
        print("Invalid data in input file. Starting with empty tree.")
    
    print("\nCommands: insert x, delete x, sort, search x, min, max, successor x, predecessor x, height, tree, exit")
    
    while True:
        try:
            command_input = input("\n\nEnter command: ").strip().split()
            
            if not command_input:
                continue
            
            command = command_input[0].lower()
            
            if command == "exit":
                print("Goodbye!")
                break
            elif command == "insert":
                if len(command_input) > 1:
                    key = int(command_input[1])
                    tree.insert(key)
                    print(f"Inserted {key}")
                    tree.print_tree()
                else:
                    print("Usage: insert <number>")
            elif command == "delete":
                if len(command_input) > 1:
                    key = int(command_input[1])
                    node = tree.search(key)
                    if node is not None:
                        tree.remove(key)
                        print(f"Deleted {key}")
                        tree.print_tree()
                    else:
                        print(f"Key {key} not found in tree")
                else:
                    print("Usage: delete <number>")
            elif command == "sort":
                if tree.root is None:
                    print("\nTree is empty")
                else:
                    print("\nIn-order traversal (sorted):")
                    tree.sort()
            elif command == "search":
                if len(command_input) > 1:
                    key = int(command_input[1])
                    node = tree.search(key)
                    if node is not None:
                        print(f"\nNode with key {key} found")
                    else:
                        print(f"\nNode with key {key} does not exist")
                else:
                    print("Usage: search <number>")
            elif command == "min":
                tree.find_min_value()
            elif command == "max":
                tree.find_max_value()
            elif command == "successor":
                if len(command_input) > 1:
                    key = int(command_input[1])
                    tree.find_successor(key)
                else:
                    print("Usage: successor <number>")
            elif command == "predecessor":
                if len(command_input) > 1:
                    key = int(command_input[1])
                    tree.find_predecessor(key)
                else:
                    print("Usage: predecessor <number>")
            elif command == "height":
                tree.print_height()
            elif command == "tree":
                tree.print_tree()
            else:
                print("Invalid command! Try: insert, delete, sort, search, min, max, successor, predecessor, height, tree, exit")
        except ValueError:
            print("Invalid input. Please enter valid numbers.")
        except KeyboardInterrupt:
            print("\n\nProgram terminated by user.")
            break
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()