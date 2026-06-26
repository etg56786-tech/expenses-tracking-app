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

print("__________EXPENSES TRACKER__________")