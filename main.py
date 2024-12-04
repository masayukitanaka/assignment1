import csv
from datetime import datetime
import os

class ExpenseTracker:
    def __init__(self, filename='expenses.csv'):
        """
        Initialize the expense tracker with a filename for saving/loading expenses
        """
        self.expenses = []
        self.monthly_budget = 0
        self.filename = filename
        self.load_expenses()

    def add_expense(self):
        """
        Prompt user to add a new expense and validate input
        """
        while True:
            try:
                date_str = self.get_valid_date()
                category = self.get_non_empty_input("Enter expense category (e.g., Food, Travel): ")
                amount = self.get_positive_float("Enter expense amount: ")
                description = self.get_non_empty_input("Enter expense description: ")

                # Create expense dictionary
                expense = {
                    'date': date_str,
                    'category': category,
                    'amount': amount,
                    'description': description
                }

                # Add expense to list
                self.expenses.append(expense)
                print("Expense added successfully!")
                break

            except Exception as e:
                print(f"An error occurred: {e}")

    def get_valid_date(self):
        while True:
            date_str = input("Enter expense date (YYYY-MM-DD): ")
            try:
                datetime.strptime(date_str, '%Y-%m-%d')
                return date_str
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD.")

    def get_non_empty_input(self, prompt):
        while True:
            value = input(prompt).strip()
            if value:
                return value
            print("Input cannot be empty.")

    def get_positive_float(self, prompt):
        while True:
            try:
                value = float(input(prompt))
                if value > 0:
                    return value
                print("Amount must be a positive number.")
            except ValueError:
                print("Invalid amount. Please enter a numeric value.")

    def view_expenses(self):
        """
        Display all recorded expenses
        """
        if not self.expenses:
            print("No expenses recorded yet.")
            return

        print("\n--- Recorded Expenses ---")
        print("Date\t\tCategory\tAmount\t\tDescription")
        print("-" * 60)
        
        for expense in self.expenses:
            print(f"{expense['date']}\t{expense['category']}\t\t${expense['amount']:.2f}\t\t{expense['description']}")

    def set_budget(self):
        """
        Allow user to set monthly budget
        """
        while True:
            try:
                budget = float(input("Enter your monthly budget: $"))
                if budget <= 0:
                    print("Budget must be a positive number.")
                    continue
                
                self.monthly_budget = budget
                print(f"Monthly budget set to ${budget:.2f}")
                break
            except ValueError:
                print("Invalid budget. Please enter a numeric value.")

    def track_budget(self):
        """
        Calculate and display budget tracking information
        """
        if self.monthly_budget == 0:
            print("No monthly budget set. Would you like to set a budget? [y/n]")
            if input().lower() == 'y':
                self.set_budget()
            return

        total_expenses = sum(expense['amount'] for expense in self.expenses)
        remaining_balance = self.monthly_budget - total_expenses

        print("\n--- Budget Tracking ---")
        print(f"Monthly Budget: ${self.monthly_budget:.2f}")
        print(f"Total Expenses: ${total_expenses:.2f}")
        
        if total_expenses > self.monthly_budget:
            print("WARNING: You have exceeded your budget!")
            print(f"Over Budget By: ${abs(remaining_balance):.2f}")
        else:
            print(f"Remaining Balance: ${remaining_balance:.2f}")

    def save_expenses(self):
        """
        Save expenses to a CSV file
        """
        try:
            with open(self.filename, 'w', newline='') as csvfile:
                # Include budget in the first row
                csvfile.write(f"Monthly Budget,{self.monthly_budget}\n")
                
                # Write expenses
                fieldnames = ['date', 'category', 'amount', 'description']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(self.expenses)
            
            print(f"Expenses saved to {self.filename}")
        except Exception as e:
            print(f"Error saving expenses: {e}")

    def load_expenses(self):
        """
        Load expenses from CSV file if it exists
        """
        if not os.path.exists(self.filename):
            return

        try:
            with open(self.filename, 'r') as csvfile:
                # Read budget from first line
                budget_line = csvfile.readline().strip()
                budget_parts = budget_line.split(',')
                if len(budget_parts) > 1:
                    self.monthly_budget = float(budget_parts[1])

                # Read expenses
                reader = csv.DictReader(csvfile)
                self.expenses = list(reader)

                # Convert amount to float
                for expense in self.expenses:
                    expense['amount'] = float(expense['amount'])

            print(f"Expenses loaded from {self.filename}")
        except Exception as e:
            print(f"Error loading expenses: {e}")

    def show_menu(self):
        print("\n--- Personal Expense Tracker ---")
        print("[1] Add Expense")
        print("[2] View Expenses")
        print("[3] Track Budget")
        print("[4] Save Expenses")
        print("[5] Exit")

    def run(self):
        """
        Main menu-driven interface for the expense tracker
        """
        while True:
            self.show_menu()
            choice = input("Enter your choice (1-5): ")

            if choice == '1':
                self.add_expense()
            elif choice == '2':
                self.view_expenses()
            elif choice == '3':
                self.track_budget()
            elif choice == '4':
                self.save_expenses()
            elif choice == '5':
                self.save_expenses()
                print("Exiting Expense Tracker. Goodbye!")
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 5.")

def main():
    tracker = ExpenseTracker()
    tracker.run()

if __name__ == "__main__":
    main()