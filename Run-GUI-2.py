# # Ramzi jarad
# # Bank Accounts System
# # GUI Interface

import tkinter as tk
from tkinter import messagebox
import json
from tabulate import tabulate
from tkinter import ttk

class Client:
    def __init__(self, id, name, balance=None):
        self.id = id
        self.name = name
        if balance is None:
            self.balance = {"ILS": 0, "USD": 0, "JOD": 0}
        else:
            self.balance = balance

    def deposit(self, currency, amount):
        if amount < 0:
            return False
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

class BankApp:
    def __init__(self, bank):
        self.bank = bank
        self.window = tk.Tk()
        self.window.title("Bank Accounts System")

        self.build_main_menu()

        self.window.mainloop()

    def build_main_menu(self):
        main_frame = tk.Frame(self.window)
        main_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(main_frame, text="Bank Accounts System", font=("Helvetica", 16)).pack(pady=10)

        tk.Button(main_frame, text="1. Add client", command=self.add_client).pack(fill=tk.X, padx=50, pady=5)
        tk.Button(main_frame, text="2. Remove client", command=self.remove_client).pack(fill=tk.X, padx=50, pady=5)
        tk.Button(main_frame, text="3. Display clients", command=self.display_clients).pack(fill=tk.X, padx=50, pady=5)
        tk.Button(main_frame, text="4. Get client balance", command=self.get_client_balance).pack(fill=tk.X, padx=50, pady=5)
        tk.Button(main_frame, text="5. Update client balance", command=self.update_client_balance).pack(fill=tk.X, padx=50, pady=5)
        tk.Button(main_frame, text="6. Quit", command=self.window.quit).pack(fill=tk.X, padx=50, pady=5)

    def add_client(self):
        new_window = tk.Toplevel(self.window)
        new_window.title("Add client")

        tk.Label(new_window, text="Enter client name: ").grid(row=0, column=0, padx=10, pady=5)
        name_entry = tk.Entry(new_window)
        name_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Button(new_window, text="Add", command=lambda: self.add_client_action(new_window, name_entry)).grid(row=1, column=0, columnspan=2, pady=10)

    def add_client_action(self, window, name_entry):
        name = name_entry.get()
        if len(name) == 0:
            messagebox.showerror("Error", "Please enter a client name")
        else:
            client = self.bank.add_client(name)
            messagebox.showinfo("Success", f"Added client with ID {client.id}")
            window.destroy()

    def remove_client(self):
        new_window = tk.Toplevel(self.window)
        new_window.title("Remove client")

        tk.Label(new_window, text="Enter client ID: ").grid(row=0, column=0, padx=10, pady=5)
        id_entry = tk.Entry(new_window)
        id_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Button(new_window, text="Remove", command=lambda: self.remove_client_action(new_window, id_entry)).grid(row=1, column=0, columnspan=2, pady=10)

    def remove_client_action(self, window, id_entry):
        try:
            id = int(id_entry.get())
            if self.bank.remove_client(id):
                messagebox.showinfo("Success", "Removed client")
                window.destroy()
            else:
                messagebox.showerror("Error", "Client not found")
        except ValueError:
            messagebox.showerror("Error", "Invalid client ID")

    def display_clients(self):
        def update_clients():
            tree.delete(*tree.get_children())
            for client in self.bank.clients:
                tree.insert("", tk.END, values=(
                    client.id, client.name, client.balance["ILS"], client.balance["USD"], client.balance["JOD"]))
            tree.after(5000, update_clients)

        clients = self.bank.clients
        if not clients:
            messagebox.showerror("Error", "No clients found")
            return
        new_window = tk.Toplevel(self.window)
        new_window.title("Display clients")

        tree = ttk.Treeview(new_window)
        tree["columns"] = ("id", "name", "ils", "usd", "jod")
        tree.column("#0", width=0, stretch=tk.NO)
        tree.column("id", width=50, minwidth=50, anchor=tk.CENTER)
        tree.column("name", width=150, minwidth=150, anchor=tk.CENTER)
        tree.column("ils", width=100, minwidth=100, anchor=tk.CENTER)
        tree.column("usd", width=100, minwidth=100, anchor=tk.CENTER)
        tree.column("jod", width=100, minwidth=100, anchor=tk.CENTER)

        tree.heading("#0", text="", anchor=tk.CENTER)
        tree.heading("id", text="ID", anchor=tk.CENTER)
        tree.heading("name", text="Client Name", anchor=tk.CENTER)
        tree.heading("ils", text="ILS Balance", anchor=tk.CENTER)
        tree.heading("usd", text="USD Balance", anchor=tk.CENTER)
        tree.heading("jod", text="JOD Balance", anchor=tk.CENTER)

        for client in clients:
            tree.insert("", tk.END, values=(
                client.id, client.name, client.balance["ILS"], client.balance["USD"], client.balance["JOD"]))

        tree.pack(fill=tk.BOTH, expand=True)

        # start the refresh cycle
        tree.after(5000, update_clients)

    def get_client_balance(self):
        new_window = tk.Toplevel(self.window)
        new_window.title("Get client balance")

        tk.Label(new_window, text="Enter client ID: ").grid(row=0, column=0, padx=10, pady=5)
        id_entry = tk.Entry(new_window)
        id_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Button(new_window, text="Get Balance",
                  command=lambda: self.get_client_balance_action(new_window, id_entry)).grid(row=1, column=0,
                                                                                             columnspan=2, pady=10)

    def get_client_balance_action(self, window, id_entry):
        try:
            id = int(id_entry.get())
            balance = self.bank.get_balance(id)
            if balance is None:
                messagebox.showerror("Error", "Client not found")
            else:
                headers = ["ID", "Client Name", "ILS Balance", "USD Balance", "JOD Balance"]
                result = f"{headers[0]}: {balance[0][0]}, {headers[1]}: {balance[0][1]}, {headers[2]}: {balance[0][2]}, {headers[3]}: {balance[0][3]}, {headers[4]}: {balance[0][4]}"
                messagebox.showinfo("Balance", result)
        except ValueError:
            messagebox.showerror("Error", "Invalid client ID")

    def update_client_balance(self):
        new_window = tk.Toplevel(self.window)
        new_window.title("Update client balance")

        tk.Label(new_window, text="Enter client ID: ").grid(row=0, column=0, padx=10, pady=5)
        id_entry = tk.Entry(new_window)
        id_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Button(new_window, text="Update Balance",
                  command=lambda: self.update_client_balance_action(new_window, id_entry)).grid(row=1, column=0,
                                                                                                columnspan=2, pady=10)

    def update_client_balance_action(self, window, id_entry):
        try:
            id = int(id_entry.get())
            client = self.bank.get_client(id)
            if client is None:
                messagebox.showerror("Error", "Client not found")
                return

            window.destroy()
            new_window = tk.Toplevel(self.window)
            new_window.title("Update client balance")

            tk.Label(new_window, text=f"Client: {client.name} (ID: {client.id})").grid(row=0, column=0, columnspan=2,
                                                                                       padx=10, pady=5)

            tk.Label(new_window, text="Action: ").grid(row=1, column=0, padx=10, pady=5)
            action_var = tk.StringVar(new_window)
            action_var.set("Deposit")
            tk.OptionMenu(new_window, action_var, "Deposit", "Withdraw").grid(row=1, column=1, padx=10, pady=5)

            tk.Label(new_window, text="Currency: ").grid(row=2, column=0, padx=10, pady=5)
            currency_var = tk.StringVar(new_window)
            currency_var.set("ILS")
            tk.OptionMenu(new_window, currency_var, "ILS", "USD", "JOD").grid(row=2, column=1, padx=10, pady=5)

            tk.Label(new_window, text="Amount: ").grid(row=3, column=0, padx=10, pady=5)
            amount_entry = tk.Entry(new_window)
            amount_entry.grid(row=3, column=1, padx=10, pady=5)

            tk.Button(new_window, text="Submit",
                      command=lambda: self.update_balance_submit(new_window, client, action_var.get(),
                                                                 currency_var.get(), amount_entry)).grid(row=4,
                                                                                                         column=0,
                                                                                                         columnspan=2,
                                                                                                         pady=10)

        except ValueError:
            messagebox.showerror("Error", "Invalid client ID")

    def update_balance_submit(self, window, client, action, currency, amount_entry):
        try:
            amount = float(amount_entry.get())
            if action == "Deposit":
                if amount < 0:
                    messagebox.showerror("Error", "Invalid amount")
                    return
                else:
                    client.deposit(currency, amount)
            elif action == "Withdraw":
                if client.withdraw(currency, amount):
                    self.bank.save_clients()
                else:
                    messagebox.showerror("Error", "Insufficient funds")
                    return
            self.bank.save_clients()
            messagebox.showinfo("Success", "Updated balance")
            window.destroy()
        except ValueError:
            messagebox.showerror("Error", "Invalid amount")

if __name__ == '__main__':
    bank = Bank()
    app = BankApp(bank)