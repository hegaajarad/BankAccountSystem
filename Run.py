# Ramzi jarad
# Bank Accounts System
import json
from tabulate import tabulate

class Client:
    def __init__(self, id, name, balance=None):
        self.id = id
        self.name = name
        if balance is None:
            self.balance = {"ILS": 0, "USD": 0, "JOD": 0}
        else:
            self.balance = balance

    def deposit(self, currency, amount):
        self.balance[currency] += amount

    def withdraw(self, currency, amount):
        if amount > self.balance[currency]:
            return False
        self.balance[currency] -= amount
        return True

    def __str__(self):
        balance_str = ", ".join([f"{k}: {v}" for k, v in self.balance.items()])
        return f"{self.id}: {self.name}, balance: {balance_str}"

class Bank:
    def __init__(self, clients_file="clients.json"):
        self.clients_file = clients_file
        self.clients = []
        self.load_clients()

    def save_clients(self):
        with open(self.clients_file, "w") as f:
            json.dump([vars(c) for c in self.clients], f)

    def load_clients(self):
        try:
            with open(self.clients_file, "r") as f:
                data = json.load(f)
                self.clients = [Client(**c) for c in data]
        except FileNotFoundError:
            pass

    def add_client(self, name):
        id = len(self.clients) + 1
        client = Client(id, name)
        self.clients.append(client)
        self.save_clients()
        return client

    def remove_client(self, id):
        for i, client in enumerate(self.clients):
            if client.id == id:
                self.clients.pop(i)
                self.save_clients()
                return True
        return False

    def display_clients(self):
        table = [[c.id, c.name] for c in self.clients]
        headers = ["ID", "Client Name"]
        print(tabulate(table, headers, tablefmt="fancy_grid"))

    def get_client(self, id):
        for client in self.clients:
            if client.id == id:
                return client
        return None

    def get_balance(self, id):
        client = self.get_client(id)
        if client is None:
            return None
        return [[client.id, client.name, client.balance["ILS"], client.balance["USD"], client.balance["JOD"]]]

    def update_balance(self, id):
        client = self.get_client(id)
        if client is None:
            return False
        while True:
            action = input("[1] Deposit\n[2] Withdraw?\n==>: ")
            currency = input("Enter currency (ILS, USD, JOD): ").upper()
            if currency not in ["ILS", "USD", "JOD"]:
                print("Invalid currency")
                continue
            if action == "1":
                amount = float(input(f"Enter amount to deposit in {currency}: "))
                client.deposit(currency, amount)
                self.save_clients()
                return True
            elif action == "2":
                amount = float(input(f"Enter amount to withdraw in {currency}: "))
                if client.withdraw(currency, amount):
                    self.save_clients()
                    return True
                else:
                    print("Insufficient funds")
            else:
                print("Invalid action")

bank = Bank()

print("\n\t\t #### Bank Accounts System ####")
while True:
    print("\n", "=="*10)
    print("Menu:")
    print("1. Add client")
    print("2. Remove client")
    print("3. Display clients")
    print("4. Get client balance")
    print("5. Update client balance")
    print("6. Quit")
    choice = input("Enter choice: ")

    # Add client
    if choice == "1":
        name = input("Enter client name: ")
        client = bank.add_client(name)
        print(f"Added client with ID {client.id}")

    # Remove client
    elif choice == "2":
        id = int(input("Enter client ID: "))
        if bank.remove_client(id):
            print("Removed client")
        else:
            print("Client not found")

    # Display clients
    elif choice == "3":
        bank.display_clients()

    # Get client balance
    elif choice == "4":
        id = int(input("Enter client ID: "))
        balance = bank.get_balance(id)
        if balance is None:
            print("Client not found")
        else:
            headers = ["ID", "Client Name", "ILS Balance", "USD Balance", "JOD Balance"]
            print(tabulate(balance, headers, tablefmt="fancy_grid"))

    # Update client balance
    elif choice == "5":
        id = int(input("Enter client ID: "))
        if bank.update_balance(id):
            print("Updated balance")
        else:
            print("Client not found or invalid input")

    # Quit
    elif choice == "6":
        break

    # Invalid choice
    else:
        print("Invalid choice")
