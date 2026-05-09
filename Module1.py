# COMP1002 Final Assignment - Module 1: Graph-Based Route Planning
# Author: Yashika Jethwani  
# Student ID: 22519740


class GraphNode:

    def __init__(self, label):
        self.label = label          
        self.visited = False       # tracks if node has been visited
        self.edges = []            
    
    def add_edge(self, node, weight):  # This adds a connection to another node with given weight
        
        if node is None:
            raise ValueError("Cannot add edge to None node")
        if weight < 0:
            raise ValueError("Edge weight cannot be negative")
        
        self.edges.append((node, weight))  # This store as tuple (destination_node, travel_time)
    
    def get_edges(self): # This returns all edges connected to this node
        
        return self.edges
    
    def mark_visited(self): # This marks the node as visited during graph traversal
        
        self.visited = True
    
    def mark_unvisited(self): # This resets the node to unvisited state
        
        self.visited = False  


class Graph: # This class represents the entire graph structure using an adjacency list
    
    def __init__(self):
        self.nodes = {}  # This is a dictionary to store all nodes - {label: GraphNode_object}
    
    def add_node(self, label): # This creates a new node with given label if it doesn't exist.
        
        if label is None or label == "":
            raise ValueError("Error: Node label cannot be None or empty")
        
        if label not in self.nodes:
            self.nodes[label] = GraphNode(label)  # This creates new GraphNode object
    
    def add_edge(self, from_node, to_node, weight): # This adds an undirected edge between two nodes with given weight
        
        if from_node is None or to_node is None:
            raise ValueError("Error: Node labels cannot be None")
        if weight < 0:
            raise ValueError("Error: Edge weight cannot be negative")
        if from_node == to_node:
            raise ValueError("Error: Self-loops are not allowed")
        
        self.add_node(from_node) # This ensures from_node exists
        self.add_node(to_node) # This ensures to_node exists
        
        # This adds edges in both directions, since this is an undirected graph
        
        self.nodes[from_node].add_edge(self.nodes[to_node], weight) # from_node - to_node
        
        self.nodes[to_node].add_edge(self.nodes[from_node], weight) # to_node - from_node
    
    def dequeue(self, queue): # This removes the first item from the queue (FIFO) and returns it
        
        if len(queue) == 0:
            raise IndexError("Error: Cannot dequeue from empty queue")
        
        first_item = queue[0]
        
        for i in range(len(queue) - 1):
            queue[i] = queue[i + 1]
        
        del queue[-1]
        
        return first_item
    
    def find_shortest_distance_node(self, distances, unvisited_nodes): # This finds the unvisited node with the smallest distance
        
        if len(unvisited_nodes) == 0:
            return None
        
        shortest_distance = float('inf')
        shortest_node = None
        
        for node in unvisited_nodes: # Linear search through unvisited nodes
            if distances[node] < shortest_distance:
                shortest_distance = distances[node]
                shortest_node = node
        
        return shortest_node
    
    def remove_from_list(self, target_list, item_to_remove): # This removes the first occurrence of item_to_remove from target_list
        
        new_list = []
        item_found = False
        
        for element in target_list: # This creates new list without the target item
            if element != item_to_remove or item_found:
                new_list.append(element)
            else:
                item_found = True  # Remove only first occurrence
        
        while len(target_list) > 0: # This clears the original list
            del target_list[0]
        
        for element in new_list:
            target_list.append(element)
        
        if not item_found:
            raise ValueError(f"Error: Item {item_to_remove} not found in list")
    
    def sorting_keys(self, dictionary): # This sorts the keys of a dictionary using bubble sort
        
        keys = []
        
        for key in dictionary: # Extracting all keys into a list
            keys.append(key)
        
        for i in range(len(keys)):
            for j in range(len(keys) - 1 - i):
                if keys[j] > keys[j + 1]:
                    
                    temp = keys[j]
                    keys[j] = keys[j + 1]
                    keys[j + 1] = temp
        
        return keys
    
    def find_index(self, target_list, item): # This finds the index of an item in a list, returns -1 if not found
        
        for i in range(len(target_list)):
            if target_list[i] == item:
                return i
        return -1  # Item not found
    
    def membership_check(self, target_list, item): # This checks if an item exists in a list, returns True/False
        
        for element in target_list:
            if element == item:
                return True
        return False
    
    def BFS(self, start):
        
        if start is None:
            raise ValueError("Error: Start node cannot be None")
        if start not in self.nodes:
            raise ValueError(f"Error: Start node '{start}' does not exist in graph")
        
        self.reset_to_unvisited() # This resets all nodes to unvisited state
        
        queue = []              # This is a queue to store nodes to visit: (node_object, level)
        result = []             # Final result: (node_label, level)
        
        queue.append((self.nodes[start], 0))
        self.nodes[start].mark_visited()
        
        while len(queue) > 0:
            current_node, level = self.dequeue(queue) # This removes the first item from the queue
            
            result.append((current_node.label, level)) # This adds current node and its level to result
            
            for neighbor, weight in current_node.get_edges(): # This explores all neighbors of current node
                
                if not neighbor.visited:
                    neighbor.mark_visited()              # Mark as visited
                    queue.append((neighbor, level + 1))  # Add to queue with next level
        
        return result
    
    def reset_to_unvisited(self): # This resets all nodes in the graph to unvisited state
        for node in self.nodes.values():
            node.mark_unvisited()
    
    def DFS(self, start): # This performs DFS to detect cycles in the graph starting from a given node
        
        if start is None:
            raise ValueError("Error: Start node cannot be None")
        if start not in self.nodes:
            raise ValueError(f"Error: Start node '{start}' does not exist in graph")
        
        self.reset_to_unvisited()
        
        def dfs_recursive_helper(node, parent, path): # This is the recursive helper function for DFS cycle detection
            
            node.mark_visited() # Marking current node as visited
            path.append(node.label)  # Adding current node to path
            
            for neighbor, weight in node.get_edges():
                if not neighbor.visited: # If neighbor is not yet visited, continue DFS
                    
                    cycle = dfs_recursive_helper(neighbor, node, path)
                    if cycle:  # If cycle is found in recursive call, return it
                        return cycle
                elif neighbor != parent and self.membership_check(path, neighbor.label):
                    
                    cycle_start_index = self.find_index(path, neighbor.label)
                    if cycle_start_index != -1: 
                        
                        cycle = [] 
                        for i in range(cycle_start_index, len(path)): # Collecting cycle from path
                            cycle.append(path[i])
                        cycle.append(neighbor.label)  # Completing the cycle
                        return cycle
            
            path.pop()
            return None 
        
        for node in self.nodes.values(): 
            if not node.visited:
                cycle = dfs_recursive_helper(node, None, [])  # Start DFS with no parent
                if cycle:
                    return cycle  # Return first cycle found
        
        return None  # No cycles found in entire graph

    
    def dijkstra(self, start): # This implements dijkstra's algorithm for finding shortest paths from start node to all other nodes
        
        if start is None:
            raise ValueError("Error: Start node cannot be None")
        if start not in self.nodes:
            raise ValueError(f"Error: Start node '{start}' does not exist in graph")
        
        distances = {}          # Storing shortest distance to each node
        previous_node = {}      # Storing previous node in shortest path (for path reconstruction)
        unvisited_nodes = []    # This is a list of nodes we haven't processed yet
        
        for node_label in self.nodes: # THis initializes distances and previous nodes for all nodes
            distances[node_label] = float('inf')  
            previous_node[node_label] = None      
            unvisited_nodes.append(node_label)    
        
        distances[start] = 0
        
        while len(unvisited_nodes) > 0:
            
            current_node = self.find_shortest_distance_node(distances, unvisited_nodes) # This finds the unvisited node with the smallest distance
            
            if current_node is None or distances[current_node] == float('inf'):
                break
                
            self.remove_from_list(unvisited_nodes, current_node) # This removes current node from unvisited list
            
            for neighbor, edge_weight in self.nodes[current_node].get_edges(): # This explores all neighbors of current node
                
                if self.membership_check(unvisited_nodes, neighbor.label): # This is to only consider neighbors that are still unvisited
                    
                    new_distance = distances[current_node] + edge_weight
                    
                    if new_distance < distances[neighbor.label]: # If the new path is shorter, updating the distance and previous node
                        distances[neighbor.label] = new_distance
                        previous_node[neighbor.label] = current_node
        
        final_paths = {} 
        for destination in self.nodes:
            if distances[destination] == float('inf'):
                final_paths[destination] = ([], float('inf'))
            else:
                path = []
                current = destination
                
                while current is not None:
                    path.insert(0, current)  # Inserting at beginning to reverse order
                    current = previous_node[current]
                final_paths[destination] = (path, distances[destination])
        
        return final_paths
    
    def print_graph(self): # This prints the entire graph structure in a readable format
        print("Graph Structure:")
        
        sorted_labels = self.sorting_keys(self.nodes)
        
        for label in sorted_labels:
            node = self.nodes[label]
            if len(node.edges) > 0:
                
                edge_info = []
                for neighbor, weight in node.edges:
                    edge_info.append(f"{neighbor.label}({weight})")
                print(f"{label} -> {edge_info}")
            else:
                print(f"{label} -> []") # This node has no connections


def test_graph_algorithms():
    try:
        g = Graph()
        
        g.add_edge('A', 'B', 5)   # A connecting to B with weight 5
        g.add_edge('A', 'C', 3)   # A connecting to C with weight 3
        g.add_edge('B', 'D', 2)   # B connecting to D with weight 2
        g.add_edge('C', 'D', 4)   # C connecting to D with weight 4
        g.add_edge('C', 'E', 7)   # C connecting to E with weight 7
        g.add_edge('D', 'F', 1)   # D connecting to F with weight 1
        g.add_edge('E', 'F', 3)   # E connecting to F with weight 3
        g.add_edge('E', 'G', 6)   # E connecting to G with weight 6
        g.add_edge('F', 'G', 2)   # F connecting to G with weight 2
        g.add_node('H')           # H has no edges
        
        g.print_graph()
        
        # Test 1: BFS - Finding all reachable nodes and their levels from A
        print("\nBFS from A:")
        bfs_result = g.BFS('A')
        for node, level in bfs_result:
            print(f"Node {node}: Level {level}")
        
        # Test 2: DFS - Checking if there are any cycles in the graph
        print("\nDFS Cycle Detection:")
        cycle = g.DFS('A')
        if cycle:
            cycle_string = ""
            for i in range(len(cycle)):
                if i > 0:
                    cycle_string += " -> "
                cycle_string += cycle[i]
            print(f"Cycle found: {cycle_string}")
        else:
            print("No cycle detected")
        
        # Test 3: Dijkstra - Finding shortest paths from A to all other nodes
        print("\nDijkstra's Shortest Paths from A:")
        shortest_paths = g.dijkstra('A')
        # Sorting the destinations 
        sorted_destinations = g.sorting_keys(shortest_paths)
        
        for destination in sorted_destinations:
            path, cost = shortest_paths[destination]
            if len(path) > 0:
                # Manually create path string
                path_string = ""
                for i in range(len(path)):
                    if i > 0:
                        path_string += " -> "
                    path_string += path[i]
                print(f"To {destination}: {path_string}, Cost: {cost}")
            else:
                print(f"To {destination}: No path available")
                
    except Exception as e:
        print(f"Error occurred: {e}")
        raise

if __name__ == "__main__":
    test_graph_algorithms() 