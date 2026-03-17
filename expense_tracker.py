"""
PROJECT ORIGIN & LEARNING OBJECTIVES
═════════════════════════════════════════════════════════════

This Expense Tracker was created as a practical learning exercise in Python
to demonstrate fundamental programming concepts:

    • Data persistence (JSON file storage)
    • Object manipulation (dictionaries, lists)
    • Date/time handling
    • User input validation & error handling
    • File I/O operations (JSON and CSV export)
    • Report generation and data analysis
    • Clean code structure with reusable functions

A beginner-friendly yet functional tool for personal finance tracking.
═════════════════════════════════════════════════════════════
"""

import json
import os
import csv
from datetime import datetime
from collections import defaultdict

# File to store transactions
# Using JSON format for simplicity and human-readability
DATA_FILE = "transactions.json"

# Transaction categories
# Organized by type (income/expense) for easy filtering and reporting
CATEGORIES = {
    "income": ["Salary", "Freelance", "Investment", "Bonus"],
    "expense": ["Food", "Transport", "Entertainment", "Utilities", "Shopping", "Healthcare", "Education", "Other"]
}


def load_transactions():
    """
    Load transactions from JSON file
    Returns empty list if file doesn't exist (first-time user )
    """
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return []


def save_transactions(transactions):
    """
    Save transactions to JSON file
    Uses indentation for human-readable format (easier to debug and review)
    """
    with open(DATA_FILE, 'w') as f:
        json.dump(transactions, f, indent=2)


def add_transaction(amount, category, description, transaction_type):
    """
    Add a new transaction (income or expense)
    
    Design Decision: Each transaction is stored as a dictionary with metadata
    including the date to enable historical tracking and monthly reporting.
    
    Args:
        amount: Transaction amount (float)
        category: Transaction category (from CATEGORIES)
        description: Transaction description (str)
        transaction_type: "income" or "expense"
    """
    transactions = load_transactions()
    
    # Create transaction record with current date
    # Date format YYYY-MM-DD allows easy sorting and filtering


    transaction = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "amount": amount,
        "category": category,
        "description": description,
        "type": transaction_type
    }
    
    transactions.append(transaction)
    save_transactions(transactions)
    print(f"✓ {transaction_type.capitalize()} of ${amount:.2f} added successfully!")


def view_transactions():
    """
    Display all transactions in a formatted table
    Shows complete transaction history to help users understand their finances
    """
    transactions = load_transactions()
    
    if not transactions:
        print("\n📭 No transactions found. Start by adding an income or expense!")
        return
    
    print("\n" + "="*85)
    print(f"{'Date':<12} {'Type':<8} {'Category':<18} {'Amount':<12} {'Description':<30}")
    print("="*85)
    
    # Display each transaction in table format
    for txn in transactions:
        print(f"{txn['date']:<12} {txn['type']:<8} {txn['category']:<18} ${txn['amount']:<11.2f} {txn['description']:<30}")
    
    print("="*85)
    print(f"Total transactions: {len(transactions)}\n")



def get_monthly_summary(year=None, month=None):
    """
    Generate monthly summary report
    Demonstrates data analysis: filtering, aggregation, and financial calculations
    
    Args:
        year: Year (defaults to current)
        month: Month (defaults to current)
    """
    if year is None or month is None:
        today = datetime.now()
        year = year or today.year
        month = month or today.month
    
    transactions = load_transactions()

    
    # Filter transactions by month and year using list comprehension
    # Design Decision: Separates monthly data for focused financial analysis


    monthly_txns = [
        t for t in transactions
        if datetime.strptime(t['date'], "%Y-%m-%d").year == year and
        datetime.strptime(t['date'], "%Y-%m-%d").month == month
    ]
    
    if not monthly_txns:
        print(f"\n📅 No transactions found for {year}-{month:02d}")
        return
    
    # Aggregate data by category using defaultdict(float)
    # Design Decision: Provides easy zero-initialization for missing categories


    income_by_category = defaultdict(float)
    expense_by_category = defaultdict(float)
    total_income = 0
    total_expense = 0
    
    # Calculate totals - demonstrates data aggregation pattern

    
    for txn in monthly_txns:
        if txn['type'] == 'income':
            income_by_category[txn['category']] += txn['amount']
            total_income += txn['amount']
        else:
            expense_by_category[txn['category']] += txn['amount']
            total_expense += txn['amount']
    
    # Print report
    print("\n" + "="*50)
    print(f"MONTHLY SUMMARY - {year}-{month:02d}")
    print("="*50)
    
    if income_by_category:
        print("\n📈 INCOME:")
        for category, amount in sorted(income_by_category.items()):
            print(f"  {category:<20} ${amount:>10.2f}")
        print(f"  {'TOTAL INCOME':<20} ${total_income:>10.2f}")
    
    if expense_by_category:
        print("\n📉 EXPENSES:")
        for category, amount in sorted(expense_by_category.items()):
            print(f"  {category:<20} ${amount:>10.2f}")
        print(f"  {'TOTAL EXPENSES':<20} ${total_expense:>10.2f}")
    
    print("\n" + "-"*50)
    net = total_income - total_expense
    status = "✓ SURPLUS" if net > 0 else "✗ DEFICIT" if net < 0 else "= BALANCED"
    print(f"NET: ${net:>10.2f}  {status}")
    print("="*50 + "\n")


def display_categories():
    """Display available transaction categories with unique numbering"""
    print("\n" + "="*40)
    print("AVAILABLE CATEGORIES")
    print("="*40)
    print("\n💰 INCOME:")
    for i, cat in enumerate(CATEGORIES['income'], 1):
        print(f"  {i}. {cat}")
    
    print("\n💸 EXPENSE:")
    for i, cat in enumerate(CATEGORIES['expense'], len(CATEGORIES['income']) + 1):
        print(f"  {i}. {cat}")
    print("="*40)


def display_welcome():
    """
    Display welcome message with project overview
    
    """
    print("\n" + "="*65)
    print("┌" + "─"*63 + "┐")
    print("│" + " "*15 + "📊 EXPENSE TRACKER SYSTEM 📊" + " "*27 + "│")
    print("│" + " "*12 + "Manage Your Personal Finances" + " "*24 + "│")
    print("└" + "─"*63 + "┘")
    print("="*65)
    print("\n🎯 A Python Learning Project demonstrating:")
    print("   • Data persistence with JSON files")
    print("   • Financial calculations and reporting")
    print("   • Data export to CSV (spreadsheet-compatible)")
    print("   • Robust user input validation")
    print("="*65)


def export_to_csv():
    """
    Export all transactions to CSV file
    Demonstrates file I/O with different formats (JSON -> CSV)
    Useful for external analysis in spreadsheet applications like Excel
    """
    transactions = load_transactions()
    
    if not transactions:
        print("\n📭 No transactions to export.")
        return
    
    # Generate unique filename with timestamp to avoid overwrites
    csv_filename = f"transactions_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    
    try:
        with open(csv_filename, 'w', newline='') as csvfile:
            fieldnames = ['Date', 'Type', 'Category', 'Amount', 'Description']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            # Write header row
            writer.writeheader()
            
            # Write each transaction
            for txn in transactions:
                writer.writerow({
                    'Date': txn['date'],
                    'Type': txn['type'].capitalize(),
                    'Category': txn['category'],
                    'Amount': f"${txn['amount']:.2f}",
                    'Description': txn['description']
                })
        
        print(f"\n✓ Transactions exported successfully to '{csv_filename}'")
        print(f"  Total rows exported: {len(transactions)}")
    except IOError as e:
        print(f"Error exporting to CSV: {e}")


def main_menu():
    """Display main menu with all available options"""
    print("\n" + "="*50)
    print("MAIN MENU - Select an option:")
    print("="*50)
    print("1. Add Income")
    print("2. Add Expense")
    print("3. View All Transactions")
    print("4. Monthly Summary Report")
    print("5. View Categories")
    print("6. Export to CSV")
    print("7. Exit")
    print("="*50)


def main():
    """Main application loop - entry point of the program"""
    display_welcome()
    
    while True:
        main_menu()
        choice = input("\nSelect an option (1-7): ").strip()
        
        if choice == "1":
            # Add income - allows user to record earnings
            print("\n💰 ADD INCOME TRANSACTION")
            print("─" * 40)
            display_categories()
            
            try:
                cat_choice = int(input("\nSelect income category number: "))
                if cat_choice < 1 or cat_choice > len(CATEGORIES['income']):
                    raise IndexError
                category = CATEGORIES['income'][cat_choice - 1]
                amount = float(input("Enter amount: $"))
                description = input("Enter description (e.g., 'March salary'): ")
                if not description.strip():
                    raise ValueError("❌ Error: Description cannot be empty.")
                add_transaction(amount, category, description, "income")
            except ValueError as e:
                if "cannot be empty" in str(e):
                    print(str(e))
                else:
                    print("❌ Invalid input. Please enter a valid number.")
            except IndexError:
                print("❌ Invalid category selection. Please try again.")
        
        elif choice == "2":
            # Add expense - allows user to record spending
            print("\n💸 ADD EXPENSE TRANSACTION")
            print("─" * 40)
            display_categories()
            
            try:
                cat_choice = int(input("\nSelect expense category number: "))
                income_count = len(CATEGORIES['income'])
                if cat_choice < income_count + 1 or cat_choice > income_count + len(CATEGORIES['expense']):
                    raise IndexError
                category = CATEGORIES['expense'][cat_choice - income_count - 1]
                amount = float(input("Enter amount: $"))
                description = input("Enter description (e.g., 'Weekly groceries'): ")
                if not description.strip():
                    raise ValueError("❌ Error: Description cannot be empty.")
                add_transaction(amount, category, description, "expense")
            except ValueError as e:
                if "cannot be empty" in str(e):
                    print(str(e))
                else:
                    print("❌ Invalid input. Please enter a valid number.")
            except IndexError:
                print("❌ Invalid category selection. Please try again.")
        
        elif choice == "3":
            # View all transactions - display complete history
            print("\n📋 ALL TRANSACTIONS")
            view_transactions()
        
        elif choice == "4":
            # Monthly summary - financial analysis for specific month
            print("\n📊 MONTHLY SUMMARY REPORT")
            print("─" * 40)
            try:
                year = int(input("Enter year (press Enter for current): ") or datetime.now().year)
                month = int(input("Enter month 1-12 (press Enter for current): ") or datetime.now().month)
                if 1 <= month <= 12:
                    get_monthly_summary(year, month)
                else:
                    print("❌ Invalid month. Please enter a number between 1-12.")
            except ValueError:
                print("❌ Invalid input. Please enter a valid year and month.")
        
        elif choice == "5":
            # View categories - display available transaction types
            display_categories()
        
        elif choice == "6":
            # Export to CSV - generate spreadsheet file
            print("\n📤 EXPORT TO CSV")
            print("─" * 40)
            export_to_csv()
        
        elif choice == "7":
            # Exit - graceful program termination
            print("\n" + "="*50)
            print("Thank you for using Expense Tracker! 👋")
            print("Your data has been saved securely. See you next time!")
            print("="*50 + "\n")
            break
        
        else:
            print("❌ Invalid choice. Please select an option from 1 to 7.")


if __name__ == "__main__":
    main()
