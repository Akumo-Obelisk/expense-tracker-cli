import json
from tkinter import *
from tkinter import messagebox
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
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return date_str
        except ValueError:
            return None

    def validate_description(self, description):
        return description.strip()

    def validate_amount(self, amount):
        try:
            amount = float(amount)
            if amount > 0:
                return amount
            else:
                return None
        except ValueError:
            return None

    def add_expense(self, date, description, amount, category):
        date = self.validate_date(date)
        if not date:
            return "Invalid date format. Use YYYY-MM-DD."
        
        if not self.validate_description(description):
            return "Description cannot be empty."
        
        amount = self.validate_amount(amount)
        if not amount:
            return "Amount must be a positive number."
        
        if category not in self.categories:
            return "Category is not valid."

        expense = Expense(date, description, amount, category)
        self.expenses.append(expense)
        self.categories.add(category)
        self.save_expenses()
        return "Expense added successfully!"

    def view_expenses(self):
        return [str(expense) for expense in self.expenses]

    def filter_expenses_by_category(self, category):
        filtered_expenses = [expense for expense in self.expenses if expense.category == category]
        return [str(expense) for expense in filtered_expenses]

    def edit_expense(self, index, date, description, amount, category):
        if 0 <= index < len(self.expenses):
            expense = self.expenses[index]
            expense.date = self.validate_date(date) if date else expense.date
            expense.description = description if description else expense.description
            expense.amount = self.validate_amount(amount) if amount else expense.amount
            expense.category = category if category else expense.category
            self.save_expenses()
            return "Expense updated successfully!"
        else:
            return "Invalid expense index."

    def total_expenses_by_category(self, category):
        total = sum(expense.amount for expense in self.expenses if expense.category == category)
        return f"Total expenses for {category}: R{total:.2f}"

    def sort_expenses(self, by="date"):
        if by == "date":
            self.expenses.sort(key=lambda expense: datetime.strptime(expense.date, "%Y-%m-%d"))
        elif by == "amount":
            self.expenses.sort(key=lambda expense: expense.amount)
        return self.view_expenses()

    def remove_expense(self, index):
        if 0 <= index < len(self.expenses):
            removed_expense = self.expenses.pop(index)
            self.save_expenses()
            return f"Removed expense: {removed_expense}"
        else:
            return "Invalid expense index."

    def remove_expenses_by_category(self, category):
        self.expenses = [expense for expense in self.expenses if expense.category != category]
        self.categories.remove(category)
        self.save_expenses()
        return f"All expenses in the category {category} have been removed."

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


class ExpenseTrackerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.tracker = ExpenseTracker()

        # Frame for input fields
        self.input_frame = Frame(root)
        self.input_frame.grid(row=0, column=0, padx=10, pady=10)

        self.date_label = Label(self.input_frame, text="Date (YYYY-MM-DD):")
        self.date_label.grid(row=0, column=0)
        self.date_entry = Entry(self.input_frame)
        self.date_entry.grid(row=0, column=1)

        self.desc_label = Label(self.input_frame, text="Description:")
        self.desc_label.grid(row=1, column=0)
        self.desc_entry = Entry(self.input_frame)
        self.desc_entry.grid(row=1, column=1)

        self.amount_label = Label(self.input_frame, text="Amount:")
        self.amount_label.grid(row=2, column=0)
        self.amount_entry = Entry(self.input_frame)
        self.amount_entry.grid(row=2, column=1)

        self.category_label = Label(self.input_frame, text="Category:")
        self.category_label.grid(row=3, column=0)
        self.category_entry = Entry(self.input_frame)
        self.category_entry.grid(row=3, column=1)

        self.add_button = Button(self.input_frame, text="Add Expense", command=self.add_expense)
        self.add_button.grid(row=4, columnspan=2)

        self.output_frame = Frame(root)
        self.output_frame.grid(row=1, column=0, padx=10, pady=10)

        self.output_text = Text(self.output_frame, width=50, height=10)
        self.output_text.grid(row=0, column=0)

        self.view_button = Button(root, text="View Expenses", command=self.view_expenses)
        self.view_button.grid(row=2, column=0, padx=10, pady=10)

        self.sort_button = Button(root, text="Sort by Date", command=self.sort_expenses)
        self.sort_button.grid(row=3, column=0, padx=10, pady=10)

        self.filter_button = Button(root, text="Filter by Category", command=self.filter_expenses)
        self.filter_button.grid(row=4, column=0, padx=10, pady=10)

    def add_expense(self):
        date = self.date_entry.get()
        description = self.desc_entry.get()
        amount = self.amount_entry.get()
        category = self.category_entry.get()

        result = self.tracker.add_expense(date, description, amount, category)
        messagebox.showinfo("Add Expense", result)

        self.clear_inputs()

    def view_expenses(self):
        expenses = self.tracker.view_expenses()
        self.display_output("\n".join(expenses))

    def sort_expenses(self):
        expenses = self.tracker.sort_expenses()
        self.display_output("\n".join(expenses))

    def filter_expenses(self):
        category = self.category_entry.get()
        expenses = self.tracker.filter_expenses_by_category(category)
        self.display_output("\n".join(expenses))

    def display_output(self, text):
        self.output_text.delete(1.0, END)
        self.output_text.insert(END, text)

    def clear_inputs(self):
        self.date_entry.delete(0, END)
        self.desc_entry.delete(0, END)
        self.amount_entry.delete(0, END)
        self.category_entry.delete(0, END)


if __name__ == "__main__":
    root = Tk()
    app = ExpenseTrackerGUI(root)
    root.mainloop()
