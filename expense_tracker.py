import json
from datetime import datetime

class Expense:
    def __init__(self, date, description, amount, category):
        self.date = date
        self.description = description
        self.amount = amount
        self.category = category

    def __str__(self):
        return f"Date: {self.date}, Description: {self.description}, Amount: R{self.amount:.2f}, Category: {self.category}"

class ExpenseTracker:
    def __init__(self):
        self.expenses = []
        self.categories = set()
        self.load_expenses()

    def validate_date(self, date_str):
        while True:
            try:
                datetime.strptime(date_str, "%Y-%m-%d")
                return date_str
            except ValueError:
                date_str = input("Invalid date format. Enter date (YYYY-MM-DD): ")

    def validate_description(self, description):
        while not description.strip():
            description = input("Invalid description. Enter a valid description: ")
        return description

    def validate_amount(self, amount):
        while True:
            try:
                amount = float(amount)
                if amount > 0:
                    return amount
                else:
                    raise ValueError
            except ValueError:
                amount = input("Invalid amount. Enter a positive number: ")

    def validate_category(self, category):
        while category not in self.categories:
            print("Available categories:", ", ".join(self.categories))
            category = input("Invalid category. Choose from available categories: ")
        return category

    def add_expense(self):
        date = self.validate_date(input("Enter date (YYYY-MM-DD): "))
        description = self.validate_description(input("Enter description: "))
        amount = self.validate_amount(input("Enter amount: "))
        if self.categories:
            print("Available categories:", ", ".join(self.categories))
        category = self.validate_category(input("Enter category: "))

        expense = Expense(date, description, amount, category)
        self.expenses.append(expense)
        self.categories.add(category)
        self.save_expenses()
        print("Expense added successfully!")

    def view_expenses(self):
        if not self.expenses:
            print("No expenses recorded.")
        else:
            for i, expense in enumerate(self.expenses, start=1):
                print(f"{i}. {expense}")

    def filter_expenses_by_category(self):
        if not self.categories:
            print("No categories available.")
            return
        print("Available categories:", ", ".join(self.categories))
        category = input("Enter category to filter by: ")
        while category not in self.categories:
            category = input("Invalid category. Choose from available categories: ")
        filtered_expenses = [expense for expense in self.expenses if expense.category == category]

        if not filtered_expenses:
            print("No expenses found for this category.")
        else:
            for expense in filtered_expenses:
                print(expense)

    def edit_expense(self):
        self.view_expenses()
        index = int(input("Enter the index of the expense to edit: ")) - 1
        if 0 <= index < len(self.expenses):
            expense = self.expenses[index]
            print(f"Editing expense: {expense}")
            expense.date = self.validate_date(input(f"Enter new date (current: {expense.date}): ") or expense.date)
            expense.description = self.validate_description(input(f"Enter new description (current: {expense.description}): ") or expense.description)
            expense.amount = self.validate_amount(input(f"Enter new amount (current: R{expense.amount:.2f}): ") or expense.amount)
            expense.category = self.validate_category(input(f"Enter new category (current: {expense.category}): ") or expense.category)
            self.save_expenses()
            print("Expense updated successfully.")
        else:
            print("Invalid expense index.")

    def total_expenses_by_category(self):
        category = input("Enter category to calculate total: ")
        while category not in self.categories:
            category = input("Invalid category. Choose from available categories: ")
        total = sum(expense.amount for expense in self.expenses if expense.category == category)
        print(f"Total expenses for {category}: R{total:.2f}")

    def sort_expenses(self):
        sort_by = input("Sort by (1) Date (2) Amount: ")
        if sort_by == '1':
            self.expenses.sort(key=lambda expense: datetime.strptime(expense.date, "%Y-%m-%d"))
        elif sort_by == '2':
            self.expenses.sort(key=lambda expense: expense.amount)
        else:
            print("Invalid choice.")
            return
        print("Expenses sorted.")
        self.view_expenses()

    def remove_expense(self):
        self.view_expenses()
        index = int(input("Enter the index of the expense to remove: ")) - 1
        if 0 <= index < len(self.expenses):
            removed_expense = self.expenses.pop(index)
            print(f"Removed expense: {removed_expense}")
            self.save_expenses()
        else:
            print("Invalid expense index.")

    def remove_expenses_by_category(self):
        if not self.categories:
            print("No categories available.")
            return
        print("Available categories:", ", ".join(self.categories))
        category = input("Enter category to remove expenses: ")
        while category not in self.categories:
            category = input("Invalid category. Choose from available categories: ")
        self.expenses = [expense for expense in self.expenses if expense.category != category]
        self.categories.remove(category)
        self.save_expenses()
        print(f"All expenses in the category {category} have been removed.")

    def save_expenses(self):
        with open("expenses.json", "w") as file:
            json.dump([vars(expense) for expense in self.expenses], file)

    def load_expenses(self):
        try:
            with open("expenses.json", "r") as file:
                data = json.load(file)
                for item in data:
                    self.expenses.append(Expense(**item))
                    self.categories.add(item["category"])
        except (FileNotFoundError, json.JSONDecodeError):
            pass

if __name__ == "__main__":
    tracker = ExpenseTracker()
    while True:
        print("\nExpense Tracker Menu:")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Filter Expenses by Category")
        print("4. Edit Expense")
        print("5. Calculate Total Expenses by Category")
        print("6. Sort Expenses")
        print("7. Remove Expense")
        print("8. Remove All Expenses in a Category")
        print("9. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            tracker.add_expense()
        elif choice == "2":
            tracker.view_expenses()
        elif choice == "3":
            tracker.filter_expenses_by_category()
        elif choice == "4":
            tracker.edit_expense()
        elif choice == "5":
            tracker.total_expenses_by_category()
        elif choice == "6":
            tracker.sort_expenses()
        elif choice == "7":
            tracker.remove_expense()
        elif choice == "8":
            tracker.remove_expenses_by_category()
        elif choice == "9":
            print("Exiting Expense Tracker.")
            break
        else:
            print("Invalid choice. Please try again.")
