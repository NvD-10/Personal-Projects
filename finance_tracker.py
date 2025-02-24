from collections import defaultdict
from datetime import date, datetime
import json

class Transaction:
    def __init__(self, category: str, amount: float, day: date, discription = ""):
        self.__category = category
        self.__amount = amount
        self.__date = day.strftime("%B %d, %Y")
        self.__discription = discription
    
    def getCategory(self):
        return self.__category
    
    def getAmount(self):
        return self.__amount
    
    def getDate(self):
        return self.__date
    
    def getDiscription(self):
        return self.__discription
    
    def display(self):
        print(f"${self.__amount} on {self.__date} for {self.__category}")
        if self.__discription:
            print(f"Description: {self.__discription}")

class TransactionManager:
    def __init__(self):
        self.__transactions = defaultdict(list)
    
    def addTransaction(self, transaction: Transaction):
        self.__transactions[transaction.getCategory()].append(transaction)
    
    def getTransactions(self, category: str):
        if category in self.__transactions:
            for transaction in self.__transactions[category]:
                transaction.display()
        else:
            print(f"No transactions done for {category}")
    
    def getExpense(self, category: str):
        expense = 0
        if category in self.__transactions:
            for transaction in self.__transactions[category]:
                expense += transaction.getAmount()
        return expense
    
    def getTotalExpenses(self):
        if self.__transactions:
            total = 0
            for category in self.__transactions:
                expense = 0
                for transaction in self.__transactions[category]:
                    expense += transaction.getAmount()
                print(f"Total expense for {category}: {expense}")
                total += expense
            print(f"Total expenses: {total}")
        else:
            print("No transactions made yet")

    def generateReport(self):
        if self.__transactions:
            for category in self.__transactions:
                print(f"Category: {category}")
                for transaction in self.__transactions[category]:
                    transaction.display()
        else:
            print("No transactions made yet")
    
    def saveToFile(self):
        transactions = {key: [event.__dict__ for event in value] for key, value in self.__transactions.items()}
        with open("transactions.json", "w") as file:
            json.dump(transactions, file, indent=2)
    
    def loadFromFile(self):
        try:
            with open("transactions.json", "r") as file:
                transactions = json.load(file)
                self.__transactions = {
                    key: [Transaction(key, item['_Transaction__amount'],
                    datetime.strptime(item['_Transaction__date'], "%B %d, %Y"),
                    item['_Transaction__discription']) for item in value] for key, value in transactions.items()
                    }
        
        except FileNotFoundError:
            with open("transactions.json", "w") as file: pass
        except json.JSONDecodeError: pass
    
class Budget:
    def __init__(self, transaction_manager: TransactionManager):
        self.__budget = defaultdict(float)
        self.__transaction_manager = transaction_manager
    
    def setBudget(self, category: str, amount: float):
        self.__budget[category] += amount
    
    def getBudget(self, category: str):
        if category in self.__budget:
            return self.__budget[category]
        else:
            print(f"No budget set for {category}")
    
    def checkBudget(self, category: str):
        if category in self.__budget:
            expense = self.__transaction_manager.getExpense(category)
            if expense > self.__budget[category]:
                print(f"Budget exeeded for {category}! You spent {expense - self.__budget[category]} more")
            else:
                print(f"Within budget for {category}")
        else:
            print(f"No budget set for {category}")
    
    def generateReport(self):
        if self.__budget:
            for category in self.__budget:
                budget, expense = self.__budget[category], self.__transaction_manager.getExpense(category)
                print(f"Budget for {category}: {budget}")
                print(f"Total expense for {category}: {expense}")
                print(f"Final balance: {budget - expense}")
        else:
            print("No budget set yet")
        
    def saveToFile(self):
        with open("budget.json", "w") as file:
            json.dump(self.__budget, file, indent=2)
    
    def loadFromFile(self):
        try:
            with open("budget.json", "r") as file:
                self.__budget = json.load(file)
        
        except FileNotFoundError:
            with open("budget.json", "w") as file: pass
        except json.JSONDecodeError: pass

def menu():
    print("\nPersonal Finance Tracker")
    print("1. Add Transaction")
    print("2. View Transactions")
    print("3. View Total Expenses")
    print("4. Generate Transactions report")
    print("5. Set Budget")
    print("6. Get Budget")
    print("7. Check Budget")
    print("8. Generate Budget Report")
    print("9. Exit")

def main():
    transaction_manager = TransactionManager()
    transaction_manager.loadFromFile()
    budget = Budget(transaction_manager)
    budget.loadFromFile()
    while True:
        menu()
        choice = input("Choose an option (1-9): ")
        
        if choice == '1':
            try:
                category = input("Enter category: ")
                amount = float(input("Enter amount: "))
                discription = input("Enter discription(optional): ")
                transaction_manager.addTransaction(Transaction(category.capitalize(), amount, date.today(), discription))
                print("Transaction added successfully")
            except ValueError:
                print("Invalid input!")
        elif choice == '2':
            category = input("Enter category: ")
            transaction_manager.getTransactions(category.capitalize())
        elif choice == '3':
            transaction_manager.getTotalExpenses()
        elif choice == '4':
            transaction_manager.generateReport()
        elif choice == '5':
            try:
                category = input("Enter category: ")
                amount = float(input("Enter amount: "))
                budget.setBudget(category.capitalize(), amount)
                print("Your budget has been set successfully")
            except ValueError:
                print("Invalid input!")
        elif choice == '6':
            category = input("Enter category: ")
            budget.getBudget(category.capitalize())
        elif choice == '7':
            category = input("Enter category: ")
            budget.checkBudget(category.capitalize())
        elif choice == '8':
            budget.generateReport()
        elif choice == '9':
            transaction_manager.saveToFile()
            budget.saveToFile()
            print("Exiting the System...")
            break
        else:
            print("Invalid choice, please try again.")

main()