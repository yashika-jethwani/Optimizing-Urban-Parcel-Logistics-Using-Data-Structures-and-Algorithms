# COMP1002 Final Assignment - Module 3: Heap-Based Parcel Scheduling
# Author: Yashika Jethwani
# ID: 22519740


from Module1 import Graph
from Module2 import dsaHashTable

class delivery_request_entry: # This class represents a single heap entry for delivery scheduling
    
    def __init__(self, priority=0.0, customer_id='', estimated_time=0):
        self.priority = priority            # Computed priority score
        self.customer_id = customer_id      # Customer ID for the delivery
        self.estimated_time = estimated_time # Estimated delivery time in minutes

class parcel_scheduling_heap: # This class implements a max-heap for parcel scheduling based on priority
    
    def __init__(self):
        self.heap_array = []                    # Array to store heap entries
        self.heap_size = 0                      # Current number of elements in heap
        
    def insert(self, delivery_request, customer_table, route_graph=None): # This function inserts a new delivery request into the heap with priority calculation
        try:
            customer_id = delivery_request['customer_id']
            destination = delivery_request.get('destination', '')
            
            print(f"\nINSERTING DELIVERY REQUEST")
            print(f"Customer ID: {customer_id}")
            print(f"Destination: {destination}")
            
            # Calculate estimated time using Module 1 or using provided time by the user
            if route_graph and 'warehouse' in delivery_request and destination:
                warehouse = delivery_request['warehouse']
                print(f"Calculating route from {warehouse} to {destination} using Module 1...")
                
                try:
                    shortest_paths = route_graph.dijkstra(warehouse)
                    if destination in shortest_paths:
                        path, estimated_time = shortest_paths[destination]
                        if estimated_time == float('inf'):
                            print(f"Error: No route available from {warehouse} to {destination}")
                            print("Available destinations:", list(shortest_paths.keys()))
                            return False
                        
                        path_str = ' → '.join(path) if len(path) > 1 else path[0] if path else "No path" # This Displays path calculation details
                        print(f"Shortest path found: {path_str}")
                        print(f"Estimated time from Module 1 Dijkstra: {estimated_time} minutes")
                    else:
                        print(f"Error: Destination '{destination}' not found in graph")
                        available_nodes = list(route_graph.nodes.keys())
                        print(f"Available locations: {available_nodes}")
                        return False
                except Exception as e:
                    print(f"Error calculating route using Module 1: {e}")
                    return False
            elif route_graph and 'warehouse' in delivery_request:
                # Get customer info to map address to destination
                customer_info = customer_table.search_customer(customer_id)
                if customer_info is None:
                    print(f"Error: Customer '{customer_id}' not found in database")
                    return False
                
                customer_address = customer_info[1]
                destination = self.address_to_route_location(customer_address)
                warehouse = delivery_request['warehouse']
                
                print(f"Mapped customer address '{customer_address}' to destination: {destination}")
                print(f"Calculating route from {warehouse} to {destination} using Module 1...")
                
                try:
                    shortest_paths = route_graph.dijkstra(warehouse)
                    if destination in shortest_paths:
                        path, estimated_time = shortest_paths[destination]
                        if estimated_time == float('inf'):
                            print(f"Error: No route available from {warehouse} to {destination}")
                            print("Available destinations:", list(shortest_paths.keys()))
                            return False
                        
                        path_str = ' → '.join(path) if len(path) > 1 else path[0] if path else "No path" # This Displays path calculation details
                        print(f"Shortest path found: {path_str}")
                        print(f"Estimated time from Module 1 Dijkstra: {estimated_time} minutes")
                    else:
                        print(f"Error: Destination '{destination}' not found in graph")
                        available_nodes = list(route_graph.nodes.keys())
                        print(f"Available locations: {available_nodes}")
                        return False
                except Exception as e:
                    print(f"Error calculating route using Module 1: {e}")
                    return False
            else: # Using manually provided estimated time
                estimated_time = delivery_request.get('estimated_time', 0)
                print(f"Using provided estimated time by the user: {estimated_time} minutes")
            
            if estimated_time <= 0:
                print("Error: Estimated time must be greater than 0")
                return False
            
            
            customer_info = customer_table.search_customer(customer_id) # This retrieves customer data from the hash table
            if customer_info is None:
                print(f"Error: Customer '{customer_id}' not found in database")
                return False
                
            customer_priority = customer_info[2]  # Priority level (1-5)
            customer_status = customer_info[3]    # Delivery status
            
            print(f"Customer Priority Level: {customer_priority}")
            print(f"Customer Status: {customer_status}")
            
            
            if customer_status.strip().lower() != 'in transit': #This only process deliveries with 'In Transit' status
                print(f"Skipping: Customer status is '{customer_status}' (not 'In Transit')")
                return False
            
            # This calculates the priority using the given formula: Priority = (6 - P) + 1000/T
            calculated_priority = (6 - customer_priority) + (1000.0 / estimated_time)
            print(f"Priority Calculation: (6 - {customer_priority}) + (1000 / {estimated_time}) = {calculated_priority:.2f}")
            
            
            new_entry = delivery_request_entry(calculated_priority, customer_id, estimated_time) #This creates a new delivery request entry
            
            
            self.heap_array.append(new_entry) # This adds new entry to the heap array
            self.heap_size += 1
            
            self.tree_up(self.heap_size - 1) # Restoring heap property by trickling up
            
            print(f"Successfully inserted: {customer_id} with priority {calculated_priority:.2f}")
            self.print_heapstate()
            return True
            
        except KeyError as e:
            print(f"Error: Missing key in delivery request - {e}")
            return False
        except Exception as e:
            print(f"Error during insertion: {e}")
            return False
        
    def swaping(self, index1, index2): # This function swaps two entries in the heap array.
        
        self.heap_array[index1], self.heap_array[index2] = self.heap_array[index2], self.heap_array[index1]
        
    def tree_up(self, index): # This function maintains the max-heap property by moving the element at index up the tree.
        
        while index > 0:
            parent_index = (index - 1) // 2
            
            # If current element has higher priority than parent,it swaps them
            if self.heap_array[index].priority > self.heap_array[parent_index].priority:
                self.swaping(index, parent_index)
                index = parent_index
            else:
                break 

    
    def tree_down(self, index): #This function restores the max-heap property by moving the element at index down the tree.
        
        while True:
            left_child = 2 * index + 1
            right_child = 2 * index + 2
            largest = index
            
            if (left_child < self.heap_size and 
                self.heap_array[left_child].priority > self.heap_array[largest].priority):
                largest = left_child
                
            if (right_child < self.heap_size and 
                self.heap_array[right_child].priority > self.heap_array[largest].priority):
                largest = right_child
            if largest != index:
                self.swaping(index, largest)
                index = largest
            else:
                break  
    
    def print_heapstate(self): # This function prints the current state of the heap.
        print(f"\n--- HEAP STATE (Size: {self.heap_size}) ---")
        if self.heap_size == 0:
            print("Heap is empty")
        else:
            for i in range(self.heap_size):
                entry = self.heap_array[i]
                print(f"Index {i}: Customer {entry.customer_id} - Priority: {entry.priority:.2f} - Time: {entry.estimated_time}min")
        print(" END HEAP STATE \n")
    
    def priority(self): # This function extracts the highest priority delivery request from the heap.
        
        try:
            if self.heap_size == 0:
                print("Error: Cannot extract from empty heap")
                return None
                
            print(f"\nEXTRACTING HIGHEST PRIORITY DELIVERY")
            
            max_entry = self.heap_array[0]
            print(f"Extracting: Customer {max_entry.customer_id}")
            print(f"Priority: {max_entry.priority:.2f}")
            print(f"Estimated Time: {max_entry.estimated_time} minutes")
            
            # This moves last element to root
            self.heap_array[0] = self.heap_array[self.heap_size - 1]
            self.heap_size -= 1
            self.heap_array.pop()  # Removeing the last element
            
            # This restores heap property if heap is not empty
            if self.heap_size > 0:
                self.tree_down(0)
            
            print(f"Successfully extracted: {max_entry.customer_id}")
            self.print_heapstate()
            return max_entry
            
        except Exception as e:
            print(f"Error during extraction: {e}")
            return None
    
    
    def warehouse_name(self, warehouse_input):
        """This function maps user warehouse input to actual warehouse names in the graph"""
        warehouse_mapping = {
            'warehouse': 'WarehouseA',
            'warehouser': 'WarehouseA', 
            'warehousea': 'WarehouseA',
            'warehouse a': 'WarehouseA',
            'warehouse-a': 'WarehouseA',
            'warehouseb': 'WarehouseB',
            'warehouse b': 'WarehouseB', 
            'warehouse-b': 'WarehouseB',
            'distribution': 'DistributionHub',
            'hub': 'DistributionHub',
            'central': 'CentralStation',
            'station': 'CentralStation'
        }
        
        key = warehouse_input.lower().strip()
        return warehouse_mapping.get(key, 'WarehouseA')  # Setting Default to WarehouseA
    
    def address_to_route_location(self, customer_address): # This function maps customer address to route location names based on predefined mappings.
        
        address_mapping = {
            'palm street': 'Palm Street',
            'sunset blvd': 'Sunset Blvd', 
            'creek ave': 'Creek Ave',
            'maple road': 'Maple Road',
            'garden lane': 'Garden Lane',
            'lotus street': 'Lotus Street',
            'oak hill': 'Oak Hill',
            'river drive': 'River Drive',
            'pine avenue': 'Pine Avenue',
            'forest path': 'Forest Path',
            'neem street': 'Neem Street',
            'mango street': 'Mango Street',
            'hilltop avenue': 'Hilltop Avenue',
            'rosewood road': 'Rosewood Road',
            'ocean view': 'Ocean View',
            'crescent lane': 'Crescent Lane',
            'westlake road': 'Westlake Road',
            'orchard drive': 'Orchard Drive',
            'aspen circle': 'Aspen Circle',
            'beach ave': 'Beach Ave',
            'beach avenue': 'Beach Ave',
            'pinecrest drive': 'Pine Avenue',  
            'oakwood court': 'Oak Hill',      
            'willow way': 'Forest Path',      
            'elm lane': 'Garden Lane',        
            'orchard drive': 'Orchard Drive',
            'highland blvd': 'Hilltop Avenue', 
            'ocean drive': 'Ocean View',       
            'persimmon road': 'Rosewood Road', 
            'evergreen lane': 'Forest Path',   
            'cedar ridge': 'Forest Path',      
            'lakewood avenue': 'Creek Ave',    
            'broad street': 'CentralStation', 
            'bay street': 'Ocean View',        
            'oak drive': 'Oak Hill',           
            'birch lane': 'Forest Path',       
            'redwood path': 'Forest Path',     
            'maple way': 'Maple Road',         
            'spruce court': 'Forest Path',     
            'coconut lane': 'Lotus Street',    
        }
        
        address_lower = customer_address.lower().strip() # Converting to lowercase and check for matches
        
        if address_lower in address_mapping:
            return address_mapping[address_lower]
        
        for key, location in address_mapping.items():
            if key in address_lower or any(word in address_lower for word in key.split()):
                return location
        
        if 'street' in address_lower:
            if 'palm' in address_lower:
                return 'Palm Street'
            elif 'pine' in address_lower:
                return 'Pine Avenue'
            elif 'oak' in address_lower:
                return 'Oak Hill'
            elif 'maple' in address_lower:
                return 'Maple Road'
            else:
                return 'CentralStation'
        elif 'avenue' in address_lower or 'ave' in address_lower:
            if 'sunset' in address_lower:
                return 'Sunset Blvd'
            elif 'creek' in address_lower:
                return 'Creek Ave'
            else:
                return 'Pine Avenue'
        elif 'road' in address_lower:
            return 'Maple Road'
        elif 'lane' in address_lower:
            return 'Garden Lane'
        elif 'drive' in address_lower:
            return 'River Drive'
    
    def is_empty(self): # This function checks if the heap is empty.
        
        return self.heap_size == 0

def loading_customerdata(filename, customer_table): # This function loads customer data from a file into the hash table.
    try:
        with open(filename, 'r') as file:
            for line in file:
                parts = line.strip().split(',')
                if len(parts) == 5:
                    customer_id, name, address, priority_level, status = parts
                    customer_table.insert_customer(customer_id, [name, address, int(priority_level), status])
        print(f"Customer data loaded successfully from {filename}")
        return True
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
        return False
    except Exception as e:
        print(f"Error loading customer data: {e}")
        return False

def loading_graphdata(filename, route_graph): # This function loads route data from a file into the graph using Module 1's methods.
    
    try:
        with open(filename, 'r') as file:
            print(f"Loading route data from {filename}...")
            for line_num, line in enumerate(file, 1):
                line = line.strip()
                if line and not line.startswith('#'):  
                    parts = line.split(',')
                    if len(parts) == 3:
                        from_location, to_location, travel_time = parts
                        from_location = from_location.strip()
                        to_location = to_location.strip()
                        travel_time = int(travel_time.strip())
                        
                        route_graph.add_edge(from_location, to_location, travel_time)
                        print(f"  Added route: {from_location} ↔ {to_location} ({travel_time} min)")
                    else:
                        print(f"  Error: Invalid format on line {line_num}: {line}")
        
        print(f"Route data loaded successfully from {filename}")
        print("\nLoaded Graph Structure:")
        route_graph.print_graph()
        return True
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
        return False
    except ValueError as e:
        print(f"Error: Invalid travel time format - {e}")
        return False
    except Exception as e:
        print(f"Error loading route data: {e}")
        return False

def delivery_request(): # This function gets delivery request input from the user with automatic address mapping.
    
    try:
        print("\n ENTER DELIVERY REQUEST ")
        customer_id = input("Enter Customer ID: ").strip()
        if not customer_id:
            print("Error: Customer ID cannot be empty")
            return None
            
        print("\nChoose input method:")
        print("1. Use Module 1 (Route Planning) - Auto-calculate from warehouse to customer address")
        print("2. Manual input - Enter estimated time directly")
        
        choice = input("Enter choice (1/2): ").strip()
        
        if choice == '1':
            return {
                'customer_id': customer_id,
                'warehouse': 'WarehouseA'  
            }
        
        elif choice == '2':
            estimated_time_str = input("Enter Estimated Delivery Time (minutes): ").strip()
            estimated_time = int(estimated_time_str)
            
            if estimated_time <= 0:
                print("Error: Estimated time must be positive")
                return None
                
            return {
                'customer_id': customer_id,
                'estimated_time': estimated_time
            }
        
        else:
            print("Invalid choice")
            return None
            
    except ValueError:
        print("Error: Invalid input")
        return None
    except Exception as e:
        print(f"Error getting delivery request: {e}")
        return None

def main(): # This is the main function that runs the parcel scheduling system.
    
    print("PARCEL SCHEDULING SYSTEM")
    
    customer_table = dsaHashTable()
    
    customer_filename = input("Enter customer data filename (e.g., customers.txt): ").strip() # Loading customer data from file
    if not loading_customerdata(customer_filename, customer_table):
        print("Failed to load customer data. Exiting.")
        return
    
    route_graph = Graph()
    
    use_routes = input("Do you want to use Module 1 route planning? (y/n): ").strip().lower()
    if use_routes == 'y':
        route_filename = input("Enter route data filename (e.g., routes.txt): ").strip()
        if not route_filename:
            route_filename = "routes.txt"  
            
        if loading_graphdata(route_filename, route_graph):
            print("Ready!")
        else:
            print("Failed to load route data. You can still use manual time input.")
            route_graph = None
    else:
        route_graph = None
        print("Using manual time input mode only.")
    
    parcel_heap = parcel_scheduling_heap()
    
    while True:
        print("\n=== MENU ===")
        print("1. Add delivery request")
        print("2. Process next delivery (extract highest priority)")
        print("3. View heap status")
        print("4. Process all deliveries")
        print("5. Exit")                                 
    
        choice = input("Enter your choice (1-5): ").strip()  
    
        if choice == '1':
            request = delivery_request()
            if request:
                parcel_heap.insert(request, customer_table, route_graph)
    
        elif choice == '2':
            if parcel_heap.is_empty():
                print("No deliveries in queue")
            else:
                extracted = parcel_heap.priority()
                if extracted:
                    print(f"Next delivery: Customer {extracted.customer_id}")
    
        elif choice == '3':
            parcel_heap.print_heapstate()
    
        elif choice == '4':
            print("\n PROCESSING ALL DELIVERIES IN PRIORITY ORDER ")
            delivery_count = 0
            while not parcel_heap.is_empty():
                extracted = parcel_heap.priority()
                if extracted:
                    delivery_count += 1
                    print(f"Delivery {delivery_count}: Customer {extracted.customer_id}")
    
            if delivery_count == 0:
                print("No deliveries to process")
            else:
                print(f"Processed {delivery_count} deliveries successfully")
    
        elif choice == '5':   
            print("Exiting Parcel Scheduling System")
            break
    
        else:
            print("Invalid choice. Please try again.")
    
    
    
    
if __name__ == "__main__":
    main()