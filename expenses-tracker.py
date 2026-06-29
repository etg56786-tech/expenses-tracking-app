import json

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


def save_categories(categories, filename="categories.json"):
    data = {name: category.ledger for name, category in categories.items()}
    with open(filename, "w") as f:
        json.dump(data, f)

def load_categories(filename="categories.json"):
    try:
        with open(filename, "r") as f:
            data = json.load(f)
        categories = {name: Category(name) for name in data}
        for name, ledger in data.items():
            categories[name].ledger = ledger
        return categories
    except FileNotFoundError:
        return {}


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
        try:

            category_name = str(command[1])
            categories[category_name] = Category(category_name)
            print(f"Category '{category_name}' created.")
        except IndexError:
            print("Please provide a category name. Usage: create <category_name>. Type 'help' for a list of commands.")

    elif command[0] == "deposit":
        try:
            category_name = str(command[1])
            amount = float(command[2])
            description = " ".join(command[3:]) if len(command) > 3 else ""
        except (IndexError, ValueError):
            print("Invalid command. Usage: deposit <category_name> <amount> [description]. Type 'help' for a list of commands.")
        if category_name in categories:
            categories[category_name].deposit(amount, description)
            print(f"Deposited {amount} into '{category_name}'.")
        else:
            #create category actually
            categories[category_name] = Category(category_name)
            categories[category_name].deposit(amount, description)
            print(f"Deposited {amount} into '{category_name}'. As the category did not exist, it has been created.")

    elif command[0] == "withdraw":
        category_name = command[1]
        amount = float(command[2])
        description = " ".join(command[3:]) if len(command) > 3 else ""
        if category_name in categories:
            if categories[category_name].withdraw(amount, description):
                print(f"Withdrew {amount} from '{category_name}'.")
            else:
                print(f"Insufficient funds in '{category_name}'.")
        else:
            print(f"Category '{category_name}' does not exist.")

    elif command[0] == "transfer":
        from_category = command[1]
        to_category = command[2]
        amount = float(command[3])
        if from_category in categories and to_category in categories:
            if categories[from_category].transfer(amount, categories[to_category]):
                print(f"Transferred {amount} from '{from_category}' to '{to_category}'.")
            else:
                print(f"Insufficient funds in '{from_category}'.")
        else:
            print("One or both categories do not exist. Perhaps try creating them first?")
    
    elif command[0] == "balance":
        category = command[1]
        #continue

    elif command[0] == "chart":
        try:
            chart = create_spend_chart(list(categories.values()))
            print(chart)
        except:
            print("Error creating chart. Make sure you have at least one category with expenses.")

    
    elif command[0] == "exit":
        active = False
        print("Exiting the Expenses Tracker.\n")
    
    else:
        print("Invalid command. Type 'help' for a list of commands.")


