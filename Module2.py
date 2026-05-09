# COMP1002 Final Assignment - Module 2: Hash-Based Customer Lookup
# Author: Yashika Jethwani
# ID: 22519740

class dsaHashEntry:  # This class represents a single hash table entry
    def __init__(self, customer_id='', data=None):
        self.customer_id = customer_id    # Stores unique customer ID
        self.data = data                  # Store corresponding customer data (list)
        self.state = 0                    # 0 = empty, 1 = used/active, 2 = deleted

    def is_active(self): # This checks if this table entry is actively used (not empty or deleted).
        return self.state == 1

class dsaHashTable: # This is for hash table implementation for customer lookup
    def __init__(self, size=101):
        self.size = size                       # Size of the hash table
        self.count = 0                         # Number of active entries
        self.table = [dsaHashEntry() for _ in range(size)]  # Create table with empty entries

    def _hash(self, customer_id): # This computes the hash value for a given customer ID (modulo-based hashing).
        return sum(ord(char) for char in customer_id) % self.size

    def insert_customer(self, customer_id, value_list): # This inserts a new customer into the hash table using linear probing to resolve collisions.
        index = self._hash(customer_id)
        start_index = index
        steps = 0

        print(f"Inserting key='{customer_id}' - Initial idx={index}", end='')

        while self.table[index].state == 1: # Linear probing to resolve collisions
            if self.table[index].customer_id == customer_id:
                print(f"\nError: Customer with ID '{customer_id}' already exists.")
                return False    
            print(f"\nCollision at index {index}, probing...")
            index = (index + 1) % self.size
            steps += 1
            if index == start_index:
                print("Error: Hash table is full.")   # If we loop back to the start, it means the table is full
                return False

        self.table[index] = dsaHashEntry(customer_id, value_list)
        self.table[index].state = 1             # Marking as active/used
        self.count += 1
        print(f" - Inserted at index {index}, step={steps}")
        return True

    def search_customer(self, customer_id): # This searches for a customer by ID using linear probing.

        index = self._hash(customer_id)
        start_index = index
        while self.table[index].state != 0:
            if self.table[index].is_active() and self.table[index].customer_id == customer_id:
                return self.table[index].data   
            index = (index + 1) % self.size
            if index == start_index:
                break                          
        return None

    def delete_customer(self, customer_id): # This deletes a customer by marking the entry as deleted (state=2).
        
        index = self._hash(customer_id)
        start_index = index
        while self.table[index].state != 0:
            if self.table[index].is_active() and self.table[index].customer_id == customer_id:
                self.table[index].state = 2     
                self.count -= 1
                return True
            index = (index + 1) % self.size
            if index == start_index:
                break
        return False

    def active_customers(self): # This returns a list of tuples containing customer IDs and their data for all active customers.
        
        return [(entry.customer_id, entry.data) for entry in self.table if entry.is_active()]



def load_file(filename, customertable): # This Loads customer data from a file into the hash table.
    try:
        with open(filename, 'r') as file:
            for line in file:
                parts = line.strip().split(',')
                if len(parts) == 5:
                    customer_id, name, address, num_items, status = parts
                    customertable.insert_customer(customer_id, [name, address, int(num_items), status])
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        exit(1)

def file_update(filename, customertable): # This updates the file with the current state of active customers in the hash table.
    with open(filename, 'w') as file:
        for customer_id, data in customertable.active_customers():
            line = f"{customer_id},{data[0]},{data[1]},{data[2]},{data[3]}\n"
            file.write(line)


def add_customer(customertable, filename): # This function adds a new customer to the hash table and updates the file.
    customer_id = input("Enter Customer ID: ").strip()
    name = input("Enter Name: ").strip()
    address = input("Enter Address: ").strip()
    try:
        num_items = int(input("Enter Priority Level (1-5): ").strip())
    except ValueError:
        print("Invalid input. (Priority Level) must be an integer.")
        return
    status = input("Enter Status (e.g., Delivered/In Transit/Delayed): ").strip()

    inserted = customertable.insert_customer(customer_id, [name, address, num_items, status])
    if inserted:
        file_update(filename, customertable)
        print("Customer details added and file updated successfully.")
    else:
        print("Failed to add customer details.")

# Main function
def main():
    print("CUSTOMER LOOKUP SYSTEM")

    filename = input("Enter customer file name (e.g., customers.txt): ")
    customertable = dsaHashTable()
    load_file(filename, customertable)

    while True:
        print("\nMenu:")
        print("1. Search customer")
        print("2. Delete customer")
        print("3. Add new customer")
        print("4. Exit")
        choice = input("Enter your choice (1/2/3/4): ")

        if choice == '1':
            customer_id = input("Enter Customer ID to search: ")
            result = customertable.search_customer(customer_id)
            if result:
                print(f"Customer '{customer_id}' found:")
                print(f"  Name          : {result[0]}")
                print(f"  Address       : {result[1]}")
                print(f"  Priority Level: {result[2]}")
                print(f"  Status        : {result[3]}")
            else:
                print("Customer ID not found.")

        elif choice == '2':
            customer_id = input("Enter Customer ID to delete: ")
            deleted = customertable.delete_customer(customer_id)
            if deleted:
                file_update(filename, customertable)
                print("Deleted successfully and file updated.")
            else:
                print("Customer ID not found or already deleted.")

        elif choice == '3':
            add_customer(customertable, filename)

        elif choice == '4':
            print("Exiting!!!!")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
