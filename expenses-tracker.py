class Category:
    def __init__(self, name):
        self.name = name

        self.ledger = []

    def deposit(self, amt, description=""):
        self.ledger.append({"amount": amt, "description": description})

    def withdraw(self, amt, description=""):
        if self.check_funds(amt):
            self.ledger.append({"amount": (amt * -1), "description": description})
            return True
        else:
            return False

    def get_balance(self):
        total = 0
        for item in self.ledger:
            total += item["amount"]
        return total

    def transfer(self, amt, other_category):

        if self.check_funds(amt):
            self.withdraw(amt, f"Transfer to {other_category.name}")
            other_category.deposit(amt, f"Transfer from {self.name}")
            return True
        else:
            return False

    def check_funds(self, amt):
        if amt > self.get_balance():
            return False
        else:
            return True

    def __str__(self):
        lines = []
        title = self.name.center(30, "*")
        lines.append(title)
        for line in self.ledger:
            desc = line["description"][:23]
            amount = line["amount"]
            newLine = f"{desc:<23}{amount:>7.2f}"
            lines.append(newLine)
        total = f"Total: {self.get_balance()}"
        lines.append(total)
        return "\n".join(lines)


def create_spend_chart(categories):
    lines = []
    title = "Percentage spent by category"
    lines.append(title)
    categories_spent = []
    total_spent = 0
    for category in categories:
        spent = 0

        for item in category.ledger:
            if item["amount"] < 0:
                spent += abs(item["amount"])

        total_spent += spent

        categories_spent.append(spent)

    percentages = [(((num / total_spent) * 100) // 10) * 10 for num in categories_spent]

    for level in range(100, -1, -10):
        line = f"{level:>3}| "
        for percentage in percentages:
            if percentage >= level:
                line += "o  "
            else:
                line += "   "

        lines.append(line)
    seperator = ("    " + "-" * (1 + (3 * len(categories_spent))))
    lines.append(seperator)
    max_len = 0
    for category in categories:
        if len(category.name) > max_len:
            max_len = len(category.name)

    for i in range(max_len):
        row = "     "
        for category in categories:
            try:
                row += category.name[i]
                row += "  "
            except IndexError:
                row += "   "

        lines.append(row)

    return "\n".join(lines)

# add a CLI interface to the expenses tracker
active = True
categories = {}

print("____________EXPENSES TRACKER____________")
print("Welcome to the Expenses Tracker!")

while active:
    print("Enter a command to get started. Type 'help' for a list of commands.")
    command = input("> ").split()
    
    if len(command) == 0:
        print("No command entered. Type 'help' for a list of commands.")
        continue
    
    elif command[0] == "help":
        print("Available commands:")
        print("  create <category_name> - Create a new category")
        print("  deposit <category_name> <amount> [description] - Deposit money into a category")
        print("  withdraw <category_name> <amount> [description] - Withdraw money from a category")
        print("  transfer <from_category> <to_category> <amount> - Transfer money between categories")
        print("  balance <category_name> - Get the balance of a category")
        print("  chart - Create a spending chart for all categories")
        print("  exit - Exit the program")

    elif command[0] == "create":
        category_name = command[1]
        categories[category_name] = Category(category_name)
        print(f"Category '{category_name}' created.")

    elif command[0] == "deposit":
        category_name = command[1]
        amount = float(command[2])
        description = " ".join(command[3:]) if len(command) > 3 else ""
        if category_name in categories:
            categories[category_name].deposit(amount, description)
            print(f"Deposited {amount} into '{category_name}'.")
        else:
            print(f"Category '{category_name}' does not exist.") #create category actually
    
    elif command[0] == "exit":
        active = False
        print("Exiting the Expenses Tracker.")
    
    else:
        print("Invalid command. Type 'help' for a list of commands.")


