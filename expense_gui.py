import tkinter as tk
from tkinter import ttk
import csv
from datetime import datetime

# ---------- FUNCTIONS ----------

def load_expenses():
    for row in tree.get_children():
        tree.delete(row)
    try:
        with open("expenses.csv", "r") as file:
            for i, row in enumerate(csv.reader(file)):
                tag = 'even' if i % 2 == 0 else 'odd'
                tree.insert("", tk.END, values=row, tags=(tag,))
    except:
        pass


def add_expense():
    amount = amount_entry.get()
    category = category_var.get()
    date = datetime.now().strftime("%Y-%m-%d")

    if amount == "":
        output_label.config(text="Enter amount!")
        return

    try:
        amount = float(amount)
    except:
        output_label.config(text="Amount must be number!")
        return

    with open("expenses.csv", "a", newline="") as file:
        csv.writer(file).writerow([amount, category, date])

    output_label.config(text="Added!")
    amount_entry.delete(0, tk.END)
    load_expenses()


def delete_expense():
    selected = tree.selection()
    if not selected:
        output_label.config(text="Select item!")
        return

    index = tree.index(selected[0])

    with open("expenses.csv", "r") as file:
        rows = list(csv.reader(file))

    rows.pop(index)

    with open("expenses.csv", "w", newline="") as file:
        csv.writer(file).writerows(rows)

    output_label.config(text="Deleted!")
    load_expenses()


def update_expense():
    selected = tree.selection()
    if not selected:
        output_label.config(text="Select item!")
        return

    index = tree.index(selected[0])
    amount = amount_entry.get()
    category = category_var.get()
    date = datetime.now().strftime("%Y-%m-%d")

    try:
        amount = float(amount)
    except:
        output_label.config(text="Amount must be number!")
        return

    with open("expenses.csv", "r") as file:
        rows = list(csv.reader(file))

    rows[index] = [amount, category, date]

    with open("expenses.csv", "w", newline="") as file:
        csv.writer(file).writerows(rows)

    output_label.config(text="Updated!")
    amount_entry.delete(0, tk.END)
    category_var.set("Food")
    load_expenses()


def total_expense():
    total = 0
    try:
        with open("expenses.csv", "r") as file:
            for row in csv.reader(file):
                total += float(row[0])

        if total == 0:
            output_label.config(text="No expenses yet!")
        else:
            output_label.config(text=f"Total: ₹{total}")

    except:
        output_label.config(text="No data!")


def monthly_report():
    summary = {}
    try:
        with open("expenses.csv", "r") as file:
            for row in csv.reader(file):
                month = row[2][:7]
                summary[month] = summary.get(month, 0) + float(row[0])

        result = "\n".join([f"{m}: ₹{amt}" for m, amt in summary.items()])
        output_label.config(text=result if result else "No data!")

    except:
        output_label.config(text="No data!")


def search_expense():
    keyword = search_entry.get().lower()

    for row in tree.get_children():
        tree.delete(row)

    try:
        with open("expenses.csv", "r") as file:
            for row in csv.reader(file):
                if keyword in row[1].lower() or keyword in row[0]:
                    tree.insert("", tk.END, values=row)
    except:
        pass


def reset_view():
    search_entry.delete(0, tk.END)
    load_expenses()


def select_item(event):
    selected = tree.selection()
    if selected:
        values = tree.item(selected[0], "values")
        amount_entry.delete(0, tk.END)
        amount_entry.insert(0, values[0])
        category_var.set(values[1])


# ---------- UI ----------

root = tk.Tk()
root.title("Expense Tracker")
root.geometry("420x600")
root.configure(bg="#eef2f7")

tk.Label(root, text="Expense Tracker",
         font=("Arial", 18, "bold"),
         bg="#eef2f7", fg="#333").pack(pady=10)

# Input
frame = tk.Frame(root, bg="white", bd=1, relief="solid")
frame.pack(pady=10, padx=10, fill="x")

tk.Label(frame, text="Amount", bg="white").grid(row=0, column=0)
amount_entry = tk.Entry(frame)
amount_entry.grid(row=0, column=1)

tk.Label(frame, text="Category", bg="white").grid(row=1, column=0)

category_var = tk.StringVar()
category_dropdown = ttk.Combobox(frame, textvariable=category_var, state="readonly")
category_dropdown['values'] = ["Food", "Travel", "Study", "Other"]
category_dropdown.grid(row=1, column=1)
category_dropdown.current(0)

# Buttons
btn_frame = tk.Frame(root, bg="white", bd=1, relief="solid")
btn_frame.pack(pady=10, padx=10, fill="x")

def styled_btn(text, cmd):
    btn = tk.Button(btn_frame, text=text, command=cmd, width=16,
                    bg="#f0f0f0", fg="#333", relief="flat")
    btn.bind("<Enter>", lambda e: btn.config(bg="#dcdcdc"))
    btn.bind("<Leave>", lambda e: btn.config(bg="#f0f0f0"))
    return btn

styled_btn("Add", add_expense).grid(row=0, column=0, padx=5, pady=5)
styled_btn("Delete", delete_expense).grid(row=0, column=1, padx=5, pady=5)
styled_btn("Total", total_expense).grid(row=1, column=0, padx=5, pady=5)
styled_btn("Monthly", monthly_report).grid(row=1, column=1, padx=5, pady=5)
styled_btn("Update", update_expense).grid(row=2, column=0, padx=5, pady=5)

# Search
search_frame = tk.Frame(root, bg="white")
search_frame.pack()

tk.Label(search_frame, text="Search:", bg="white").pack(side=tk.LEFT)
search_entry = tk.Entry(search_frame)
search_entry.pack(side=tk.LEFT)

tk.Button(search_frame, text="Go", command=search_expense).pack(side=tk.LEFT)
tk.Button(search_frame, text="Reset", command=reset_view).pack(side=tk.LEFT)

# Table
table_frame = tk.Frame(root, bg="white", bd=1, relief="solid")
table_frame.pack(pady=10, padx=10, fill="both", expand=True)

style = ttk.Style()
style.configure("Treeview", rowheight=28)
style.configure("Treeview.Heading", font=("Arial", 10, "bold"))

columns = ("Amount", "Category", "Date")
tree = ttk.Treeview(table_frame, columns=columns, show="headings")

tree.tag_configure('odd', background="#f9f9f9")
tree.tag_configure('even', background="white")

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=120, anchor="center")

tree.pack(fill="both", expand=True)
tree.bind("<<TreeviewSelect>>", select_item)

# Output
output_label = tk.Label(root, text="Welcome! Add your expenses 👍",
                        bg="#eef2f7", fg="#333", font=("Arial", 10))
output_label.pack(pady=10)

load_expenses()

root.mainloop()