# COMP1002 Final Assignment - Module 4: Sorting Delivery Records
# Author: Yashika Jethwani
# ID: 22519740

import time
import random
from Module1 import Graph
from Module2 import dsaHashTable

class delivery_record: # This class represents a single delivery record entry
    
    def __init__(self, customer_id='', customer_name='', address='', priority_level=0, status='', estimated_time=0):
        self.customer_id = customer_id              
        self.customer_name = customer_name          
        self.address = address                      
        self.priority_level = priority_level        
        self.status = status                        
        self.estimated_time = estimated_time        
class delivery_sorting_system: # This class implements sorting algorithms for delivery records
    
    def __init__(self):
        self.records = []                           # List to store delivery records
        self.comparison_count = 0                   # Counter for algorithm comparisons
        self.swap_count = 0                         # Counter for algorithm swaps
    
    def reset_counters(self): # This resets the performance counters
        self.comparison_count = 0
        self.swap_count = 0
    
    def add_record(self, record): # This adds a delivery record to the system
        if record is None:
            raise ValueError("Error: Cannot add None record")
        self.records.append(record)
    
    def clear_records(self): # This clears all delivery records from the system
        self.records = []
    
    def records_copy(self): # This creates a copy of current records for testing
        copied_records = []
        for record in self.records:
            new_record = delivery_record(
                record.customer_id,
                record.customer_name, 
                record.address,
                record.priority_level,
                record.status,
                record.estimated_time
            )
            copied_records.append(new_record)
        return copied_records
    

    def merge_two_lists(self, left_list, right_list): # This merges two sorted lists into one sorted list
        
        merged_list = []
        left_index = 0
        right_index = 0
        
        while left_index < len(left_list) and right_index < len(right_list):
            self.comparison_count += 1
            
            if left_list[left_index].estimated_time <= right_list[right_index].estimated_time:
                merged_list.append(left_list[left_index])
                left_index += 1
            else:
                merged_list.append(right_list[right_index])
                right_index += 1
        
        
        while left_index < len(left_list): # This adds remaining elements from left list
            merged_list.append(left_list[left_index])
            left_index += 1
        
        while right_index < len(right_list): # This adds remaining elements from right list
            merged_list.append(right_list[right_index])
            right_index += 1
        
        return merged_list

    def merge_sort(self, records_list): # This implements merge sort algorithm for delivery records based on estimated time
        
        if records_list is None:
            raise ValueError("Error: Cannot sort None list")
        
        if len(records_list) <= 1:
            return records_list
        
        middle_index = len(records_list) // 2 # This divides the list into two halves
        left_half = []
        right_half = []
        
        for i in range(middle_index): # This splits the records into left and right halves
            left_half.append(records_list[i])
        
        for i in range(middle_index, len(records_list)):
            right_half.append(records_list[i])
        
        
        left_sorted = self.merge_sort(left_half) # This recursively sorts both halves
        right_sorted = self.merge_sort(right_half)
        
        return self.merge_two_lists(left_sorted, right_sorted)
    
    def swap_records(self, records_list, index1, index2): # This swaps two records in the list
        
        if index1 != index2:
            self.swap_count += 1
            temp_record = records_list[index1]
            records_list[index1] = records_list[index2] 
            records_list[index2] = temp_record
    
    def partition_records(self, records_list, low_index, high_index): # This partitions the records list for quick sort using the last element as pivot
        
        pivot_record = records_list[high_index]  # This chooses last element as pivot
        smaller_element_index = low_index - 1    # Index of smaller element
        
        for current_index in range(low_index, high_index):
            self.comparison_count += 1
            
            if records_list[current_index].estimated_time <= pivot_record.estimated_time: # If current element is smaller than or equal to pivot
                smaller_element_index += 1
                self.swap_records(records_list, smaller_element_index, current_index)
        
        # This places pivot in correct position
        self.swap_records(records_list, smaller_element_index + 1, high_index)
        return smaller_element_index + 1
    
    def quick_sort(self, records_list, low_index=0, high_index=None): # This implements quick sort algorithm for delivery records based on estimated time
        
        if records_list is None:
            raise ValueError("Error: Cannot sort None list")
        
        if high_index is None:
            high_index = len(records_list) - 1
        
        if low_index < high_index:
            pivot_position = self.partition_records(records_list, low_index, high_index)
            
            
            self.quick_sort(records_list, low_index, pivot_position - 1) # This recursively sorts elements before and after the pivot
            self.quick_sort(records_list, pivot_position + 1, high_index)
        
        return records_list
    
    
    def random_records(self, size): # This generates random delivery records for testing
        
        if size <= 0:
            raise ValueError("Error: Size must be positive")
        
        self.clear_records()
        
        sample_names = [
            "Aarav Sharma", "Isha Verma", "Vihaan Patel", "Myra Singh", "Reyansh Mehta",
            "Anaya Reddy", "Arjun Das", "Kiara Nair", "Ayaan Gupta", "Meera Iyer",
            "Anvi Singh", "Rudra Chopra", "Diya Kapoor", "Krish Kumar", "Lucas Miller",
            "Olivia Clark", "Mateo Garcia", "Sophia Martinez", "Liam Smith", "Emma Johnson"
        ]
        
        sample_addresses = [
            "Palm Street", "Sunset Blvd", "Creek Ave", "Maple Road", "Garden Lane",
            "Lotus Street", "Oak Hill", "River Drive", "Pine Avenue", "Forest Path",
            "Neem Street", "Mango Street", "Hilltop Avenue", "Rosewood Road", "Ocean View"
        ]
        
        status = ["Delivered", "In Transit", "Delayed"]
        
        for i in range(size):
            customer_id = f"CUST{i:03d}"
            customer_name = sample_names[i % len(sample_names)]
            address = sample_addresses[i % len(sample_addresses)]
            priority_level = (i % 5) + 1  
            status = status[i % len(status)]
            estimated_time = random.randint(10, 120)  # Random time between 10-120 minutes
            
            record = delivery_record(customer_id, customer_name, address, priority_level, status, estimated_time)
            self.add_record(record)
        
        print(f"Generated {size} random delivery records")
    
    def nearlysorted_records(self, size): # This generates nearly sorted delivery records for testing
        
        self.random_records(size)
        
        sorted_records = self.records_copy()
        self.reset_counters()
        sorted_records = self.merge_sort(sorted_records)
        
        swap_count = max(1, size // 20)  
        
        for _ in range(swap_count):
            index1 = random.randint(0, size - 1)
            index2 = random.randint(0, size - 1)
            
            temp_record = sorted_records[index1]
            sorted_records[index1] = sorted_records[index2]
            sorted_records[index2] = temp_record
        
        self.records = sorted_records
        print(f"Generated {size} nearly sorted delivery records")
    
    def reversesorted_records(self, size): # This generates reverse sorted delivery records for testing
        
        self.random_records(size)
        
        sorted_records = self.records_copy()
        self.reset_counters()
        sorted_records = self.merge_sort(sorted_records)
        
        reversed_records = []
        for i in range(len(sorted_records) - 1, -1, -1):
            reversed_records.append(sorted_records[i])
        
        self.records = reversed_records
        print(f"Generated {size} reverse sorted delivery records")


    def estimated_time(self, customer_address, route_graph): # This calculates estimated delivery time using route planning or random assignment
        
        if route_graph is None:
            return random.randint(15, 90)  # Random time if no route graph available
        
        try: # This uses Dijkstra's algorithm from Module 1 to find shortest path
            shortest_paths = route_graph.dijkstra('WarehouseA')
            
            address_lower = customer_address.lower()
            if 'palm' in address_lower:
                destination = 'Palm Street'
            elif 'sunset' in address_lower:
                destination = 'Sunset Blvd'
            elif 'creek' in address_lower:
                destination = 'Creek Ave'
            elif 'maple' in address_lower:
                destination = 'Maple Road'
            elif 'garden' in address_lower:
                destination = 'Garden Lane'
            elif 'oak' in address_lower:
                destination = 'Oak Hill'
            elif 'pine' in address_lower:
                destination = 'Pine Avenue'
            else:
                destination = 'CentralStation'
            
            if destination in shortest_paths:
                path, estimated_time = shortest_paths[destination]
                if estimated_time != float('inf'):
                    return int(estimated_time)
        except Exception as e:
            print(f"Error calculating route time: {e}")
        
        return random.randint(20, 80)  
    
    def loadrecords_customerdata(self, customer_table, route_graph=None): # This loads delivery records from customer hash table with estimated times
        
        if customer_table is None:
            raise ValueError("Error: Customer table cannot be None")
        
        self.clear_records()
        
        active_customers = customer_table.active_customers()
        
        for customer_id, customer_data in active_customers:
            customer_name = customer_data[0]
            address = customer_data[1] 
            priority_level = customer_data[2]
            status = customer_data[3]
            
            estimated_time = self.estimated_time(address, route_graph) # This calculates estimated time using route planning or random assignment
            
            record = delivery_record(customer_id, customer_name, address, priority_level, status, estimated_time)
            self.add_record(record)
        
        print(f"Loaded {len(self.records)} delivery records from customer data")
    
    
    def sorting_performance(self, algorithm_name, records_copy): # This measures and returns the performance metrics of a sorting algorithm
        
        if algorithm_name is None or records_copy is None:
            raise ValueError("Error: Algorithm name and records cannot be None")
        
        self.reset_counters()
        start_time = time.time()
        
        if algorithm_name.lower() == 'merge':
            sorted_records = self.merge_sort(records_copy)
        elif algorithm_name.lower() == 'quick':
            sorted_records = self.quick_sort(records_copy)
        else:
            raise ValueError(f"Error: Unknown algorithm '{algorithm_name}'")
        
        end_time = time.time()
        execution_time = (end_time - start_time) * 1000  # Converting to milliseconds
        
        return {
            'algorithm': algorithm_name,
            'execution_time': execution_time,
            'comparisons': self.comparison_count,
            'swaps': self.swap_count,
            'sorted_records': sorted_records
        }
    
    def performance_analysis(self, dataset_sizes, data_conditions): # This runs comprehensive performance analysis on different dataset sizes and conditions
        
        print("Running performance analysis...")
        
        results = []
        
        for size in dataset_sizes:
            print(f"Testing dataset size: {size}")
            
            for condition in data_conditions:
                print(f"  {condition} data condition...")
                
                
                if condition == 'random':
                    self.random_records(size)
                elif condition == 'nearly_sorted':
                    self.nearlysorted_records(size)
                elif condition == 'reverse_sorted':
                    self.reversesorted_records(size)
                
                
                for algorithm in ['merge', 'quick']:
                    records_copy = self.records_copy()
                    
                    performance = self.sorting_performance(algorithm, records_copy)
                    performance['size'] = size
                    performance['condition'] = condition
                    results.append(performance)
                    
                    print(f"    {algorithm} sort: {performance['execution_time']:.2f}ms")
        
        return results
    
    def display_sorted_records(self, sorted_records, limit=10): # This displays sorted delivery records with optional limit
        
        if not sorted_records:
            print("No records")
            return
        
        print(f"\nSorted records (by estimated time):")
        
        for i in range(min(limit, len(sorted_records))):
            record = sorted_records[i]
            print(f"{record.customer_id}: {record.estimated_time}min")
        
        if len(sorted_records) > limit:
            print(f"... ({len(sorted_records)} total)")
    
    def performance_report(self, results): # This generates a comprehensive performance analysis report
        
        print("\nPerformance Report")
        print("-" * 40)
        
        
        for size in [100, 500, 1000]:
            if any(result['size'] == size for result in results):
                print(f"\nSize: {size}")
                
                for condition in ['random', 'nearly_sorted', 'reverse_sorted']:
                    merge_result = None
                    quick_result = None
                    
                    
                    for result in results:
                        if result['size'] == size and result['condition'] == condition:
                            if result['algorithm'] == 'merge':
                                merge_result = result
                            elif result['algorithm'] == 'quick':
                                quick_result = result
                    
                    if merge_result and quick_result:
                        print(f"{condition}: Merge {merge_result['execution_time']:.2f}ms, Quick {quick_result['execution_time']:.2f}ms")
        
        print("\nAnalysis:")
        print("Merge Sort: O(n log n) consistent")
        print("Quick Sort: O(n log n) average, O(n²) worst case")

def loadingcustomer_sorting(filename, customer_table): # This loads customer data from file into hash table for sorting analysis
    
    try:
        with open(filename, 'r') as file:
            for line in file:
                parts = line.strip().split(',')
                if len(parts) == 5:
                    customer_id, name, address, priority_level, status = parts
                    customer_table.insert_customer(customer_id, [name, address, int(priority_level), status])
        print(f"Loaded customer data from {filename}")
        return True
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
        return False
    except Exception as e:
        print(f"Error loading customer data: {e}")
        return False

def loadingroute_sorting(filename, route_graph): # This loads route data from file into graph for time estimation
    
    try:
        with open(filename, 'r') as file:
            for line in file:
                line = line.strip()
                if line and not line.startswith('#'):
                    parts = line.split(',')
                    if len(parts) == 3:
                        from_location, to_location, travel_time = parts
                        route_graph.add_edge(from_location.strip(), to_location.strip(), int(travel_time.strip()))
        print(f"Loaded route data from {filename}")
        return True
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")  
        return False
    except Exception as e:
        print(f"Error loading route data: {e}")
        return False

def main(): # This is the main function that runs the delivery records sorting system
    
    sorting_system = delivery_sorting_system()
    
    while True:
        print("\n1. Load data from file")
        print("2. Performance analysis")
        print("3. Exit")
        
        choice = input("Choice: ")
        
        if choice == '1':
            customer_table = dsaHashTable()
            route_graph = Graph()
            
            filename = input("Customer file: ")
            if not filename:
                filename = "customers.txt"
            
            if loadingcustomer_sorting(filename, customer_table):
                routes = input("Routes file (optional): ")
                if routes:
                    loadingroute_sorting(routes, route_graph)
                else:
                    route_graph = None
                
                sorting_system.loadrecords_customerdata(customer_table, route_graph)
                
                if len(sorting_system.records) > 0:
                    print("1. Merge Sort")
                    print("2. Quick Sort")
                    algo = input("Algorithm: ")
                    
                    records_copy = sorting_system.records_copy()
                    
                    if algo == '1':
                        result = sorting_system.sorting_performance('merge', records_copy)
                    elif algo == '2':
                        result = sorting_system.sorting_performance('quick', records_copy)
                    else:
                        print("Invalid")
                        continue
                    
                    print(f"\n{result['algorithm']} - Time: {result['execution_time']:.2f}ms")
                    print(f"Comparisons: {result['comparisons']}, Swaps: {result['swaps']}")
                    
                    display = input("Show records? (y/n): ")
                    if display == 'y':
                        sorting_system.display_sorted_records(result['sorted_records'])
        
        elif choice == '2':
            dataset_sizes = [100, 500, 1000]
            data_conditions = ['random', 'nearly_sorted', 'reverse_sorted']
            
            results = sorting_system.performance_analysis(dataset_sizes, data_conditions)
            sorting_system.performance_report(results)
        
        elif choice == '3':
            print("Exiting...")
            break
        
        else:
            print("Invalid")

if __name__ == "__main__":
    main()