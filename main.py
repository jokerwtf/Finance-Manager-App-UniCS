import tkinter as tk
import tkinter.ttk as ttk
import sqlite3
from tkinter import messagebox
import xlsxwriter
import matplotlib.pyplot as plt

root = tk.Tk()
root.geometry("800x600")
root.title("Finance Application")


def income_page():
    def submit_income_data():
        category_id = None
        amount = income_amount_entry.get()
        category = income_selected_option.get()
        if category == "Salary":
            category_id = 1
        elif category == "Gifts":
            category_id = 2
        elif category == "Stocks":
            category_id = 3
        elif category == "Passive":
            category_id = 4
        global transaction_id
        date = income_date_entry.get()
        description = income_description_entry.get()
        is_periodic = income_check_box_value.get()
        frequency = income_frequency_entry.get()
        start_date = income_start_date_entry.get()
        end_date = income_end_date_entry.get()
        # create db if not exists
        conn = sqlite3.connect("personal_finance.db")
        table_category_create_query = """CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        type TEXT NOT NULL)"""
        conn.execute(table_category_create_query)
        conn.close()
        conn = sqlite3.connect("personal_finance.db")
        table_transactions_create_query = """CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY,
        category_id INTEGER NOT NULL,
        amount REAL NOT NULL,
        description TEXT,
        date DATE NOT NULL,
        is_periodic INTEGER NOT NULL,
        frequency INTEGER,
        start_date DATE,
        end_date DATE,
        FOREIGN KEY (category_id) REFERENCES categories(id))"""
        conn.execute(table_transactions_create_query)
        conn.close()
        conn = sqlite3.connect("personal_finance.db")
        cursor = conn.cursor()
        insert_categories_query = "INSERT INTO categories (id,name,type) VALUES (?,?,?)"
        values = [
            (1, "Salary", "Income"),
            (2, "Gifts", "Income"),
            (3, "Stocks", "Income"),
            (4, "Passive", "Income")
        ]
        try:
            cursor.executemany(insert_categories_query, values)
        except sqlite3.IntegrityError:
            pass
        conn.commit()
        cursor.close()
        conn.close()

        if (not category_id) or (not description) or (not amount) or (not date):
            messagebox.showinfo("Failure", "insert all data")
            return

        # get a unique id
        transaction_id = 1
        conn = sqlite3.connect("personal_finance.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM transactions")
        column_values = cursor.fetchall()
        cursor.close()
        conn.close()
        id_list = []
        for elements in column_values:
            id_list.append(elements[0])
        while True:
            if transaction_id not in id_list:
                break
            else:
                transaction_id = transaction_id + 1

        conn = sqlite3.connect("personal_finance.db")
        cursor = conn.cursor()
        insert_transaction_query = """INSERT INTO transactions 
        (id,category_id,amount,description,date,is_periodic,frequency,start_date,end_date) 
        VALUES (?,?,?,?,?,?,?,?,?)"""

        values = (transaction_id, category_id, amount, description, date, is_periodic, frequency, start_date, end_date)
        cursor.execute(insert_transaction_query, values)
        conn.commit()
        cursor.close()
        conn.close()

        income_amount_entry.delete(0, tk.END)
        income_selected_option.delete(0, tk.END)
        income_date_entry.delete(0, tk.END)
        income_description_entry.delete(0, tk.END)
        income_isperiodic_box.deselect()
        income_frequency_entry.delete(0, tk.END)
        income_start_date_entry.delete(0, tk.END)
        income_end_date_entry.delete(0, tk.END)

        messagebox.showinfo("Success", "Transaction Saved")

    income_frame = tk.Frame(main_frame)
    lb = tk.Label(income_frame, text="Income Page", font=("Bold,15"))
    lb.pack()
    add_a_transaction_lb = tk.Label(main_frame, text="Add a new transaction", font=("Bold,10")).place(x=0, y=30)
    income_amount_lb = tk.Label(main_frame, text="Income Amount:", font=("Bold,10")).place(x=20, y=60)
    income_amount_entry = tk.Entry(main_frame)
    income_amount_entry.place(x=280, y=60)
    income_category_lb = tk.Label(main_frame, text="Income Category:", font=("Bold,10")).place(x=20, y=100)
    income_options = ["Salary", "Gifts", "Stocks", "Passive"]
    income_selected_option = ttk.Combobox(main_frame, values=income_options)
    income_selected_option.place(x=280, y=100)
    income_date_lb = tk.Label(main_frame, text="Transaction Date:", font=("Bold,10")).place(x=20, y=140)
    income_date_entry = tk.Entry(main_frame)
    income_date_entry.insert(0, "DD/MM/YYYY")
    income_date_entry.place(x=280, y=140)

    def on_entry_click(event):
        if income_date_entry.get() == "DD/MM/YYYY":
            income_date_entry.delete(0, "end")
            income_date_entry.insert(0, '')
    income_date_entry.bind("<FocusIn>", on_entry_click)
    income_submit_btn = tk.Button(main_frame, text="Submit", command=submit_income_data)
    income_submit_btn.place(x=580, y=260)
    income_description_label = tk.Label(main_frame, text="Description", font=("Bold,10")).place(x=20, y=180)
    income_description_entry = tk.Entry(main_frame)
    income_description_entry.place(x=280, y=180)
    income_check_box_value = tk.IntVar()
    income_check_box_value.set(0)

    def checkboxclicked():
        if income_check_box_value.get() == 1:
            income_frequency_entry.configure(state="normal")
            income_start_date_entry.configure(state="normal")
            income_end_date_entry.configure(state="normal")
        else:
            income_frequency_entry.configure(state="disabled")
            income_start_date_entry.configure(state="disabled")
            income_end_date_entry.configure(state="disabled")

    income_isperiodic_box = tk.Checkbutton(main_frame, text="Periodic Transaction", font=("Bold,10"),
                                      variable=income_check_box_value,command=checkboxclicked)
    income_isperiodic_box.place(x=20, y=220)
    income_frequency_label=tk.Label(main_frame,text="Frequency",font=("Bold,10"))

    income_frequency_label.place(x=20,y=260)
    income_frequency_entry=tk.Entry(main_frame,width=5,state="disabled")
    income_frequency_entry.place(x=130,y=265)
    income_start_date_label=tk.Label(main_frame,text="Start date",font=("Bold,10"))
    income_start_date_label.place(x=190,y=260)
    income_start_date_entry=tk.Entry(main_frame,width=10,state="disabled")
    income_start_date_entry.place(x=290,y=265)
    income_end_date_label = tk.Label(main_frame, text="End date", font=("Bold,10"))
    income_end_date_label.place(x=370, y=260)
    income_end_date_entry = tk.Entry(main_frame, width=10, state="disabled")
    income_end_date_entry.place(x=480, y=265)
    income_more_options_label = tk.Label(main_frame, text="More Options", font=("Bold", 15)).place(x=0, y=350)



    def viewall():
        viewall_window = tk.Tk()
        viewall_window.geometry("800x400+300+300")
        viewall_window.title("View All Transactions")

        tree_frame = ttk.Frame(viewall_window)
        tree_frame.pack(fill='both', expand=True)

        tree = ttk.Treeview(tree_frame)
        tree['columns'] = ('Category', 'Amount', 'Date')
        tree.heading('#0', text='ID')
        tree.heading('Category', text='Category')
        tree.heading('Amount', text='Amount')
        tree.heading('Date', text='Date')

        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
        scrollbar.pack(side='right', fill='y')

        tree.configure(yscrollcommand=scrollbar.set)
        tree.pack(side='left', fill='both', expand=True)

        sql = """SELECT transactions.id as ID, categories.name as Category, transactions.amount, transactions.date 
                FROM transactions INNER JOIN categories ON transactions.category_id = categories.id"""

        try:
            with sqlite3.connect('personal_finance.db') as conn:
                cursor = conn.cursor()
                cursor.execute(sql)

                for row in cursor:
                    tree.insert('', 'end', text=row[0], values=(row[1], row[2], row[3]))

        except:
            messagebox.showinfo("Failure", "No transactions")

        viewall_window.mainloop()

    # Rest of the code...

    income_view_all_btn = tk.Button(main_frame, text="View All", width=20, command=viewall)
    income_view_all_btn.place(x=20, y=390)

    def delete_entry():
        delete_window=tk.Tk()
        delete_window.geometry("400x400+1100+300")
        delete_window.title("Delete Transactions")
        delete_label = tk.Label(delete_window, text="Delete Transaction", font=("Bold,15"))
        delete_label.place(x=30, y=0)
        delete_category_label = tk.Label(delete_window,text="Delete a transactions category",font=("Bold,15"))
        delete_category_label.place(x=30,y=140)
        choose_category_label = tk.Label(delete_window,text="Choose category")
        choose_category_label.place(x=20,y=170)
        category_options = ["Salary", "Gifts", "Stocks", "Passive","Entertainment", "Rent", "Groceries", "Transportation"]
        category_selected_option = ttk.Combobox(delete_window, values=category_options)
        category_selected_option.place(x=20, y=190)
        def delete_category():
            category_to_delete = category_selected_option.get()
            id_category=None
            if category_to_delete=="Salary":
                id_category=1
            elif category_to_delete=="Gifts":
                id_category=2
            elif category_to_delete == "Stocks":
                id_category=3
            elif category_to_delete=="Passive":
                id_category=4
            elif category_to_delete=="Entertainment":
                id_category=5
            elif category_to_delete=="Rent":
                id_category=6
            elif category_to_delete=="Groceries":
                id_category=7
            elif category_to_delete=="Transportation":
                id_category=8
            conn = sqlite3.connect("personal_finance.db")
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM transactions WHERE category_id={id_category}")
            data = cursor.fetchall()
            if data:
                cursor.execute(f"DELETE FROM transactions WHERE category_id={id_category}")
                conn.commit()
                messagebox.showinfo("Success", "Category Deleted")
                delete_entry_entry.delete(0, tk.END)
            else:
                messagebox.showinfo("Failure", "Insert Valid category")
                delete_entry_entry.delete(0, tk.END)
            delete_window.destroy()
            viewall_window.destroy()

        category_delete_btn = tk.Button(delete_window, text="Delete", width=20, command=delete_category)
        category_delete_btn.place(x=20, y=220)

        #viewall part
        viewall_window = tk.Tk()
        viewall_window.geometry("800x400+300+300")
        viewall_window.title("View All Transactions")

        tree_frame = ttk.Frame(viewall_window)
        tree_frame.pack(fill='both', expand=True)

        tree = ttk.Treeview(tree_frame)
        tree['columns'] = ('Category', 'Amount', 'Date')
        tree.heading('#0', text='ID')
        tree.heading('Category', text='Category')
        tree.heading('Amount', text='Amount')
        tree.heading('Date', text='Date')

        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
        scrollbar.pack(side='right', fill='y')

        tree.configure(yscrollcommand=scrollbar.set)
        tree.pack(side='left', fill='both', expand=True)

        sql = """SELECT transactions.id as ID, categories.name as Category, transactions.amount, transactions.date 
                        FROM transactions INNER JOIN categories ON transactions.category_id = categories.id"""

        try:
            with sqlite3.connect('personal_finance.db') as conn:
                cursor = conn.cursor()
                cursor.execute(sql)

                for row in cursor:
                    tree.insert('', 'end', text=row[0], values=(row[1], row[2], row[3]))

        except:
            messagebox.showinfo("Failure", "No transactions")
        #viewallpart end
        delete_label=tk.Label(delete_window,text="Insert ID to delete:")
        delete_label.place(x=20,y=30)
        delete_entry_entry=tk.Entry(delete_window,width=3)
        delete_entry_entry.place(x=150,y=30)

        def delete_from_db():
            id_to_delete=delete_entry_entry.get()
            conn = sqlite3.connect("personal_finance.db")
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM transactions WHERE id={id_to_delete}")
            data=cursor.fetchall()
            if data:
                cursor.execute(f"DELETE FROM transactions WHERE id={id_to_delete}")
                conn.commit()
                messagebox.showinfo("Success", "Transaction Deleted")
                delete_entry_entry.delete(0, tk.END)
            else:
                messagebox.showinfo("Failure", "Insert Valid id")
                delete_entry_entry.delete(0, tk.END)
            delete_window.destroy()
            viewall_window.destroy()

        delete_btn=tk.Button(delete_window, text="Delete", width=15,command=delete_from_db)
        delete_btn.place(x=70,y=60)

    income_delete_btn = tk.Button(main_frame, text="Delete", width=20,command=delete_entry)
    income_delete_btn.place(x=240, y=390)
    def modify_entry():
        modify_window = tk.Tk()
        modify_window.geometry("400x400+1100+300")
        modify_window.title("Delete Transactions")
        modify_label = tk.Label(modify_window, text="Modify Transaction", font=("Bold,15"))
        modify_label.place(x=30, y=0)
        # viewall part
        viewall_window = tk.Tk()
        viewall_window.geometry("800x400+300+300")
        viewall_window.title("View All Transactions")

        tree_frame = ttk.Frame(viewall_window)
        tree_frame.pack(fill='both', expand=True)

        tree = ttk.Treeview(tree_frame)
        tree['columns'] = ('Category', 'Amount', 'Date')
        tree.heading('#0', text='ID')
        tree.heading('Category', text='Category')
        tree.heading('Amount', text='Amount')
        tree.heading('Date', text='Date')

        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
        scrollbar.pack(side='right', fill='y')

        tree.configure(yscrollcommand=scrollbar.set)
        tree.pack(side='left', fill='both', expand=True)

        sql = """SELECT transactions.id as ID, categories.name as Category, transactions.amount, transactions.date 
                                FROM transactions INNER JOIN categories ON transactions.category_id = categories.id"""

        try:
            with sqlite3.connect('personal_finance.db') as conn:
                cursor = conn.cursor()
                cursor.execute(sql)

                for row in cursor:
                    tree.insert('', 'end', text=row[0], values=(row[1], row[2], row[3]))

        except:
            messagebox.showinfo("Failure", "No transactions")
        # viewallpart end

        def modify_from_db():
            id_to_modify = modify_entry_entry.get()
            category_id = None
            amount = modify_amount_entry.get()
            date=modify_date_entry.get()
            category = modify_selected_option.get()
            if category == "Salary":
                category_id = 1
            elif category == "Gifts":
                category_id = 2
            elif category == "Stocks":
                category_id = 3
            elif category == "Passive":
                category_id = 4
            elif category == "Entertainment":
                category_id = 5
            elif category == "Rent":
                category_id = 6
            elif category == "Groceries":
                category_id = 7
            elif category == "Transportation":
                category_id = 8

            new_data={
                "id":f"{id_to_modify}",
                "category_id":f"{category_id}",
                "amount":f"{amount}",
                "date":f"{date}"
            }
            conn = sqlite3.connect("personal_finance.db")
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM transactions WHERE id={id_to_modify}")
            data = cursor.fetchall()
            if data:
                cursor.execute(f"UPDATE transactions SET id = ?, category_id = ?, amount = ?,date = ? WHERE id = {id_to_modify}",
               (new_data['id'], new_data['category_id'], new_data['amount'],new_data['date']))
                conn.commit()
                messagebox.showinfo("Success", "Transaction Modified")
                modify_entry_entry.delete(0, tk.END)
            else:
                messagebox.showinfo("Failure", "Insert Valid id")
                modify_entry_entry.delete(0, tk.END)
            modify_window.destroy()
            viewall_window.destroy()

        modify_label = tk.Label(modify_window, text="Insert ID to modify:")
        modify_label.place(x=20, y=40)
        modify_entry_entry = tk.Entry(modify_window, width=3)
        modify_entry_entry.place(x=150, y=40)
        modify_btn = tk.Button(modify_window, text="Modify", width=15, command=modify_from_db)
        modify_btn.place(x=170, y=300)
        modify_category_label=tk.Label(modify_window,text="Category").place(x=20,y=70)
        modify_options = ["Salary", "Gifts", "Stocks", "Passive", "Entertainment", "Rent", "Groceries", "Transportation"]
        modify_selected_option = ttk.Combobox(modify_window, values=modify_options)
        modify_selected_option.place(x=100, y=70)
        modify_amount_label=tk.Label(modify_window,text="Amount")
        modify_amount_label.place(x=20,y=100)
        modify_amount_entry=tk.Entry(modify_window)
        modify_amount_entry.place(x=100,y=100)
        modify_date_label=tk.Label(modify_window,text="Date").place(x=20,y=130)
        modify_date_entry=tk.Entry(modify_window)
        modify_date_entry.place(x=100,y=130)

    income_modify_btn = tk.Button(main_frame, text="Modify", width=20,command=modify_entry)
    income_modify_btn.place(x=470, y=390)
    income_frame.pack(pady=20)


def expenses_page():

    def submit_expenses_data():
        category_id = None
        amount = expenses_amount_entry.get()
        category = expenses_selected_option.get()
        if category == "Entertainment":
            category_id = 5
        elif category == "Rent":
            category_id = 6
        elif category == "Groceries":
            category_id = 7
        elif category == "Transportation":
            category_id = 8
        global transaction_id
        date = expenses_date_entry.get()
        description = expenses_description_entry.get()
        is_periodic = expenses_check_box_value.get()
        frequency = expenses_frequency_entry.get()
        start_date = expenses_start_date_entry.get()
        end_date = expenses_end_date_entry.get()
        # create db if not exists
        conn = sqlite3.connect("personal_finance.db")
        table_category_create_query = """CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        type TEXT NOT NULL)"""
        conn.execute(table_category_create_query)
        conn.close()
        conn = sqlite3.connect("personal_finance.db")
        table_transactions_create_query = """CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY,
        category_id INTEGER NOT NULL,
        amount REAL NOT NULL,
        description TEXT,
        date DATE NOT NULL,
        is_periodic INTEGER NOT NULL,
        frequency INTEGER,
        start_date DATE,
        end_date DATE,
        FOREIGN KEY (category_id) REFERENCES categories(id))"""
        conn.execute(table_transactions_create_query)
        conn.close()
        conn = sqlite3.connect("personal_finance.db")
        cursor = conn.cursor()
        insert_categories_query = "INSERT INTO categories (id,name,type) VALUES (?,?,?)"
        values = [
            (5, "Entertainment", "Expenses"),
            (6, "Rent", "Expenses"),
            (7, "Groceries", "Expenses"),
            (8, "Transportation", "Expenses")
        ]
        try:
            cursor.executemany(insert_categories_query, values)
        except sqlite3.IntegrityError:
            pass
        conn.commit()
        cursor.close()
        conn.close()

        if (not category_id) or (not description) or (not amount) or (not date):
            messagebox.showinfo("Failure", "insert all data")
            return

        # get a unique id
        transaction_id = 1
        conn = sqlite3.connect("personal_finance.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM transactions")
        column_values = cursor.fetchall()
        cursor.close()
        conn.close()
        id_list = []
        for elements in column_values:
            id_list.append(elements[0])
        while True:
            if transaction_id not in id_list:
                break
            else:
                transaction_id = transaction_id + 1

        conn = sqlite3.connect("personal_finance.db")
        cursor = conn.cursor()
        insert_transaction_query = """INSERT INTO transactions 
        (id,category_id,amount,description,date,is_periodic,frequency,start_date,end_date) 
        VALUES (?,?,?,?,?,?,?,?,?)"""

        values = (transaction_id, category_id, amount, description, date, is_periodic, frequency, start_date, end_date)
        cursor.execute(insert_transaction_query, values)
        conn.commit()
        cursor.close()
        conn.close()

        expenses_amount_entry.delete(0, tk.END)
        expenses_selected_option.delete(0, tk.END)
        expenses_date_entry.delete(0, tk.END)
        expenses_description_entry.delete(0, tk.END)
        expenses_isperiodic_box.deselect()
        expenses_frequency_entry.delete(0, tk.END)
        expenses_start_date_entry.delete(0, tk.END)
        expenses_end_date_entry.delete(0, tk.END)

        messagebox.showinfo("Success", "Transaction Saved")

    expenses_frame = tk.Frame(main_frame)
    lb = tk.Label(expenses_frame, text="Expenses Page", font=("Bold,15"))
    lb.pack()
    add_a_transaction_lb = tk.Label(main_frame, text="Add a new transaction", font=("Bold,10")).place(x=0, y=30)
    expenses_amount_lb = tk.Label(main_frame, text="Expenses Amount:", font=("Bold,10")).place(x=20, y=60)
    expenses_amount_entry = tk.Entry(main_frame)
    expenses_amount_entry.place(x=280, y=60)
    expenses_category_lb = tk.Label(main_frame, text="Expenses Category:", font=("Bold,10")).place(x=20, y=100)
    expenses_options = ["Entertainment", "Rent", "Groceries", "Transportation"]
    expenses_selected_option = ttk.Combobox(main_frame, values=expenses_options)
    expenses_selected_option.place(x=280, y=100)
    expenses_date_lb = tk.Label(main_frame, text="Transaction Date:", font=("Bold,10")).place(x=20, y=140)
    expenses_date_entry = tk.Entry(main_frame)
    expenses_date_entry.insert(0, "DD/MM/YYYY")
    expenses_date_entry.place(x=280, y=140)

    def on_entry_click(event):
        if expenses_date_entry.get() == "DD/MM/YYYY":
            expenses_date_entry.delete(0, "end")
            expenses_date_entry.insert(0, '')

    expenses_date_entry.bind("<FocusIn>", on_entry_click)
    expenses_submit_btn = tk.Button(main_frame, text="Submit", command=submit_expenses_data)
    expenses_submit_btn.place(x=580, y=260)
    expenses_description_label = tk.Label(main_frame, text="Description", font=("Bold,10")).place(x=20, y=180)
    expenses_description_entry = tk.Entry(main_frame)
    expenses_description_entry.place(x=280, y=180)
    expenses_check_box_value = tk.IntVar()
    expenses_check_box_value.set(0)

    def checkboxclicked():
        if expenses_check_box_value.get() == 1:
            expenses_frequency_entry.configure(state="normal")
            expenses_start_date_entry.configure(state="normal")
            expenses_end_date_entry.configure(state="normal")
        else:
            expenses_frequency_entry.configure(state="disabled")
            expenses_start_date_entry.configure(state="disabled")
            expenses_end_date_entry.configure(state="disabled")

    expenses_isperiodic_box = tk.Checkbutton(main_frame, text="Periodic Transaction", font=("Bold,10"),
                                           variable=expenses_check_box_value, command=checkboxclicked)
    expenses_isperiodic_box.place(x=20, y=220)
    expenses_frequency_label = tk.Label(main_frame, text="Frequency", font=("Bold,10"))

    expenses_frequency_label.place(x=20, y=260)
    expenses_frequency_entry = tk.Entry(main_frame, width=5, state="disabled")
    expenses_frequency_entry.place(x=130, y=265)
    expenses_start_date_label = tk.Label(main_frame, text="Start date", font=("Bold,10"))
    expenses_start_date_label.place(x=190, y=260)
    expenses_start_date_entry = tk.Entry(main_frame, width=10, state="disabled")
    expenses_start_date_entry.place(x=290, y=265)
    expenses_end_date_label = tk.Label(main_frame, text="End date", font=("Bold,10"))
    expenses_end_date_label.place(x=370, y=260)
    expenses_end_date_entry = tk.Entry(main_frame, width=10, state="disabled")
    expenses_end_date_entry.place(x=480, y=265)
    expenses_more_options_label = tk.Label(main_frame, text="More Options", font=("Bold", 15)).place(x=0, y=350)

    def viewall():
        viewall_window = tk.Tk()
        viewall_window.geometry("800x400+300+300")
        viewall_window.title("View All Transactions")

        tree_frame = ttk.Frame(viewall_window)
        tree_frame.pack(fill='both', expand=True)

        tree = ttk.Treeview(tree_frame)
        tree['columns'] = ('Category', 'Amount', 'Date')
        tree.heading('#0', text='ID')
        tree.heading('Category', text='Category')
        tree.heading('Amount', text='Amount')
        tree.heading('Date', text='Date')

        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
        scrollbar.pack(side='right', fill='y')

        tree.configure(yscrollcommand=scrollbar.set)
        tree.pack(side='left', fill='both', expand=True)

        sql = """SELECT transactions.id as ID, categories.name as Category, transactions.amount, transactions.date 
                FROM transactions INNER JOIN categories ON transactions.category_id = categories.id"""

        try:
            with sqlite3.connect('personal_finance.db') as conn:
                cursor = conn.cursor()
                cursor.execute(sql)

                for row in cursor:
                    tree.insert('', 'end', text=row[0], values=(row[1], row[2], row[3]))

        except:
            messagebox.showinfo("Failure", "No transactions")

        viewall_window.mainloop()

    # Rest of the code...

    income_view_all_btn = tk.Button(main_frame, text="View All", width=20, command=viewall)
    income_view_all_btn.place(x=20, y=390)

    def delete_entry():
        delete_window = tk.Tk()
        delete_window.geometry("400x400+1100+300")
        delete_window.title("Delete Transactions")
        delete_label = tk.Label(delete_window, text="Delete Transaction", font=("Bold,15"))
        delete_label.place(x=30, y=0)
        delete_category_label = tk.Label(delete_window, text="Delete a transactions category", font=("Bold,15"))
        delete_category_label.place(x=30, y=140)
        choose_category_label = tk.Label(delete_window, text="Choose category")
        choose_category_label.place(x=20, y=170)
        category_options = ["Salary", "Gifts", "Stocks", "Passive", "Entertainment", "Rent", "Groceries",
                            "Transportation"]
        category_selected_option = ttk.Combobox(delete_window, values=category_options)
        category_selected_option.place(x=20, y=190)

        def delete_category():
            category_to_delete = category_selected_option.get()
            id_category = None
            if category_to_delete == "Salary":
                id_category = 1
            elif category_to_delete == "Gifts":
                id_category = 2
            elif category_to_delete == "Stocks":
                id_category = 3
            elif category_to_delete == "Passive":
                id_category = 4
            elif category_to_delete == "Entertainment":
                id_category = 5
            elif category_to_delete == "Rent":
                id_category = 6
            elif category_to_delete == "Groceries":
                id_category = 7
            elif category_to_delete == "Transportation":
                id_category = 8
            conn = sqlite3.connect("personal_finance.db")
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM transactions WHERE category_id={id_category}")
            data = cursor.fetchall()
            if data:
                cursor.execute(f"DELETE FROM transactions WHERE category_id={id_category}")
                conn.commit()
                messagebox.showinfo("Success", "Category Deleted")
                delete_entry_entry.delete(0, tk.END)
            else:
                messagebox.showinfo("Failure", "Insert Valid category")
                delete_entry_entry.delete(0, tk.END)
            delete_window.destroy()
            viewall_window.destroy()

        category_delete_btn = tk.Button(delete_window, text="Delete", width=20, command=delete_category)
        category_delete_btn.place(x=20, y=220)
        # viewall part
        viewall_window = tk.Tk()
        viewall_window.geometry("800x400+300+300")
        viewall_window.title("View All Transactions")

        tree_frame = ttk.Frame(viewall_window)
        tree_frame.pack(fill='both', expand=True)

        tree = ttk.Treeview(tree_frame)
        tree['columns'] = ('Category', 'Amount', 'Date')
        tree.heading('#0', text='ID')
        tree.heading('Category', text='Category')
        tree.heading('Amount', text='Amount')
        tree.heading('Date', text='Date')

        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
        scrollbar.pack(side='right', fill='y')

        tree.configure(yscrollcommand=scrollbar.set)
        tree.pack(side='left', fill='both', expand=True)

        sql = """SELECT transactions.id as ID, categories.name as Category, transactions.amount, transactions.date 
                        FROM transactions INNER JOIN categories ON transactions.category_id = categories.id"""

        try:
            with sqlite3.connect('personal_finance.db') as conn:
                cursor = conn.cursor()
                cursor.execute(sql)

                for row in cursor:
                    tree.insert('', 'end', text=row[0], values=(row[1], row[2], row[3]))

        except:
            messagebox.showinfo("Failure", "No transactions")
        # viewallpart end
        delete_label = tk.Label(delete_window, text="Insert ID to delete:")
        delete_label.place(x=20, y=30)
        delete_entry_entry = tk.Entry(delete_window, width=3)
        delete_entry_entry.place(x=150, y=30)

        def delete_from_db():
            id_to_delete = delete_entry_entry.get()
            conn = sqlite3.connect("personal_finance.db")
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM transactions WHERE id={id_to_delete}")
            data = cursor.fetchall()
            if data:
                cursor.execute(f"DELETE FROM transactions WHERE id={id_to_delete}")
                conn.commit()
                messagebox.showinfo("Success", "Transaction Deleted")
                delete_entry_entry.delete(0, tk.END)
            else:
                messagebox.showinfo("Failure", "Insert Valid id")
                delete_entry_entry.delete(0, tk.END)
            delete_window.destroy()
            viewall_window.destroy()

        delete_btn = tk.Button(delete_window, text="Delete", width=15, command=delete_from_db)
        delete_btn.place(x=70, y=60)

    expenses_delete_btn = tk.Button(main_frame, text="Delete", width=20, command=delete_entry)
    expenses_delete_btn.place(x=240, y=390)
    #################
    def modify_entry():
        modify_window = tk.Tk()
        modify_window.geometry("400x400+1100+300")
        modify_window.title("Delete Transactions")
        modify_label = tk.Label(modify_window, text="Modify Transaction", font=("Bold,15"))
        modify_label.place(x=30, y=0)
        # viewall part
        viewall_window = tk.Tk()
        viewall_window.geometry("800x400+300+300")
        viewall_window.title("View All Transactions")

        tree_frame = ttk.Frame(viewall_window)
        tree_frame.pack(fill='both', expand=True)

        tree = ttk.Treeview(tree_frame)
        tree['columns'] = ('Category', 'Amount', 'Date')
        tree.heading('#0', text='ID')
        tree.heading('Category', text='Category')
        tree.heading('Amount', text='Amount')
        tree.heading('Date', text='Date')

        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
        scrollbar.pack(side='right', fill='y')

        tree.configure(yscrollcommand=scrollbar.set)
        tree.pack(side='left', fill='both', expand=True)

        sql = """SELECT transactions.id as ID, categories.name as Category, transactions.amount, transactions.date 
                                FROM transactions INNER JOIN categories ON transactions.category_id = categories.id"""

        try:
            with sqlite3.connect('personal_finance.db') as conn:
                cursor = conn.cursor()
                cursor.execute(sql)

                for row in cursor:
                    tree.insert('', 'end', text=row[0], values=(row[1], row[2], row[3]))

        except:
            messagebox.showinfo("Failure", "No transactions")
        # viewallpart end

        def modify_from_db():
            id_to_modify = modify_entry_entry.get()
            category_id = None
            amount = modify_amount_entry.get()
            date=modify_date_entry.get()
            category = modify_selected_option.get()
            if category == "Salary":
                category_id = 1
            elif category == "Gifts":
                category_id = 2
            elif category == "Stocks":
                category_id = 3
            elif category == "Passive":
                category_id = 4
            elif category == "Entertainment":
                category_id = 5
            elif category == "Rent":
                category_id = 6
            elif category == "Groceries":
                category_id = 7
            elif category == "Transportation":
                category_id = 8

            new_data={
                "id":f"{id_to_modify}",
                "category_id":f"{category_id}",
                "amount":f"{amount}",
                "date":f"{date}"
            }
            conn = sqlite3.connect("personal_finance.db")
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM transactions WHERE id={id_to_modify}")
            data = cursor.fetchall()
            if data:
                cursor.execute(f"UPDATE transactions SET id = ?, category_id = ?, amount = ?,date = ? WHERE id = {id_to_modify}",
               (new_data['id'], new_data['category_id'], new_data['amount'],new_data['date']))
                conn.commit()
                messagebox.showinfo("Success", "Transaction Modified")
                modify_entry_entry.delete(0, tk.END)
            else:
                messagebox.showinfo("Failure", "Insert Valid id")
                modify_entry_entry.delete(0, tk.END)
            modify_window.destroy()
            viewall_window.destroy()

        modify_label = tk.Label(modify_window, text="Insert ID to modify:")
        modify_label.place(x=20, y=40)
        modify_entry_entry = tk.Entry(modify_window, width=3)
        modify_entry_entry.place(x=150, y=40)
        modify_btn = tk.Button(modify_window, text="Modify", width=15, command=modify_from_db)
        modify_btn.place(x=170, y=300)
        modify_category_label=tk.Label(modify_window,text="Category").place(x=20,y=70)
        modify_options = ["Salary", "Gifts", "Stocks", "Passive", "Entertainment", "Rent", "Groceries", "Transportation"]
        modify_selected_option = ttk.Combobox(modify_window, values=modify_options)
        modify_selected_option.place(x=100, y=70)
        modify_amount_label=tk.Label(modify_window,text="Amount")
        modify_amount_label.place(x=20,y=100)
        modify_amount_entry=tk.Entry(modify_window)
        modify_amount_entry.place(x=100,y=100)
        modify_date_label=tk.Label(modify_window,text="Date").place(x=20,y=130)
        modify_date_entry=tk.Entry(modify_window)
        modify_date_entry.place(x=100,y=130)
    #################
    expenses_modify_btn = tk.Button(main_frame, text="Modify", width=20,command=modify_entry)
    expenses_modify_btn.place(x=470, y=390)
    expenses_frame.pack(pady=20)


def monthly_income_graph(cursor):
    cursor.execute("""SELECT sum(amount), name FROM transactions, categories WHERE transactions.category_id = categories.id and categories.type = "Income" GROUP by name;""")
    data = cursor.fetchall()
    amounts = [row[0] for row in data]
    types = [row[1] for row in data]

    total = sum(amounts)
    def my_fmt(x):
        return f"{x:.2f}%\n {total * x / 100:.0f}"

    plt.pie(amounts, labels = types, autopct=my_fmt)
    plt.show()


def monthly_expense_graph(cursor):
    cursor.execute("""SELECT sum(amount), name FROM transactions, categories WHERE transactions.category_id = categories.id and categories.type = "Expenses" GROUP by name;""")
    data = cursor.fetchall()
    amounts = [row[0] for row in data]
    types = [row[1] for row in data]

    total = sum(amounts)
    def my_fmt(x):
        return f"{x:.2f}%\n {total * x / 100:.0f}"

    plt.pie(amounts, labels = types, autopct=my_fmt)
    plt.show()


def annually_expenses_graph(cursor):
    cursor.execute("""
        SELECT
            SUM(CASE WHEN category_id BETWEEN 1 AND 4 THEN amount ELSE 0 END) AS total_income,
            SUM(CASE WHEN category_id BETWEEN 5 AND 8 THEN amount ELSE 0 END) AS total_expenses
        FROM
            transactions;
    """)
    frame3 = tk.Frame(main_frame)
    lb = tk.Label(frame3, text="", font=("Bold,15"))
    lb.pack()
    data = cursor.fetchall()
    total_income = data[0][0]
    total_expenses = data[0][1]
    amounts = [total_income, total_expenses]
    types = ["Total Income", "Total Expenses"]
    total = sum(amounts)
    def my_fmt(x):
        return f"{x:.2f}%\n {total * x / 100:.0f}"

    plt.pie(amounts, labels = types, autopct=my_fmt)
    plt.show()

def visualise_page():
    conn = sqlite3.connect("personal_finance.db")
    cursor = conn.cursor()

    visualise_frame = tk.Frame(main_frame)
    lb = tk.Label(visualise_frame, text="Graphs Page", font=("Bold,15"))
    lb.pack()
    visualise_frame.pack(pady=20)
    monthly_exp_btn = tk.Button(visualise_frame, text="Total Expenses", font=("bold", 10),
                                command=lambda: monthly_expense_graph(cursor))
    monthly_exp_btn.pack(side=tk.LEFT, padx=10, pady=10)
    annually_exp_btn = tk.Button(visualise_frame, text="Total Expenses & Income Ratio", font=("bold", 10),
                                 command=lambda: annually_expenses_graph(cursor))
    annually_exp_btn.pack(side=tk.LEFT, padx=10, pady=10)
    monthly_inc_btn = tk.Button(visualise_frame, text="Total Income", font=("bold", 10),
                                command=lambda: monthly_income_graph(cursor))
    monthly_inc_btn.pack(side=tk.LEFT, padx=10, pady=10)


def extract_page():
    def export_to_excel(selected_month):
        # Query the transactions for the selected month
        conn = sqlite3.connect("personal_finance.db")
        cursor = conn.cursor()
        # Extract the month from the date using string manipulation
        cursor.execute(
            "SELECT t.id, c.name, t.amount, t.description, t.date, t.is_periodic, t.frequency, t.start_date, t.end_date FROM transactions t JOIN categories c ON t.category_id = c.id WHERE SUBSTR(t.date, 4, 2) = ?",
            (selected_month,))
        transactions = cursor.fetchall()
        conn.close()

        # Create an Excel file and add a worksheet
        workbook = xlsxwriter.Workbook("extracted_data.xlsx")
        worksheet = workbook.add_worksheet("Transactions")

        # Write column headers
        headers = ["ID", "Category", "Amount", "Description", "Date", "Is Periodic", "Frequency", "Start Date",
                   "End Date"]
        for col, header in enumerate(headers):
            worksheet.write(0, col, header)

        # Format amount as text
        text_format = workbook.add_format({'num_format': '@'})
        worksheet.set_column(2, 2, None, text_format)

        # Write transaction data
        for row, transaction in enumerate(transactions):
            for col, value in enumerate(transaction):
                if col == 5:  # Map is_periodic to "No" or "Yes"
                    worksheet.write(row + 1, col, "No" if value == 0 else "Yes")
                elif col == 2:  # Format amount as text
                    worksheet.write(row + 1, col, str(value), text_format)
                else:
                    worksheet.write(row + 1, col, value)

        # Close the workbook
        workbook.close()
        messagebox.showinfo("Success", "Data exported to extracted_data.xlsx")

    extract_frame = tk.Frame(main_frame)
    lb = tk.Label(extract_frame, text="Extract Page", font=("Bold", 15))
    lb.pack(pady=10)

    # Label for month selection
    month_label = tk.Label(extract_frame, text="Select Month:", font=("Bold", 10))
    month_label.pack()

    # Month selection
    month_combo = ttk.Combobox(extract_frame,
                               values=["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"])
    month_combo.pack()

    # Export button
    export_btn = tk.Button(extract_frame, text="Export to Excel", command=lambda: export_to_excel(month_combo.get()))
    export_btn.pack(pady=10)

    extract_frame.pack(pady=20)




# function pou allazei xrwma indicators otan clicked
def hide_indicators():
    income_indicate.config(bg="#c3c3c3")
    expenses_indicate.config(bg="#c3c3c3")
    visualise_indicate.config(bg="#c3c3c3")
    extract_indicate.config(bg="#c3c3c3")


def delete_pages():
    for frame in main_frame.winfo_children():
        frame.destroy()


def indicate(label_object, page):
    hide_indicators()
    label_object.config(bg="black")
    delete_pages()
    page()


# frames

transaction_id=1
options_frame = tk.Frame(root, bg="#c3c3c3")
options_frame.pack(side=tk.LEFT)
options_frame.pack_propagate(False)
options_frame.configure(height=600, width=100)
main_frame = tk.Frame(root, highlightbackground="black", highlightthickness=2)
main_frame.pack(side=tk.LEFT)
main_frame.pack_propagate(False)
# In Tkinter, the pack_propagate method is used to control whether a widget should
# be allowed to change the size of its parent widget when packed using the pack geometry manager.
# You can use the pack_propagate method to prevent a widget from resizing its parent.
main_frame.configure(height=600, width=700)

# buttons
income_btn = tk.Button(options_frame, text="Income", font=("Bold", 10),
                       command=lambda: indicate(income_indicate, income_page))
income_btn.place(x=10, y=10)
expenses_btn = tk.Button(options_frame, text="Expenses", font=("bold", 10),
                         command=lambda: indicate(expenses_indicate, expenses_page))
expenses_btn.place(x=10, y=60)
visualise_btn = tk.Button(options_frame, text="Visualise", font=("bold", 10),
                          command=lambda: indicate(visualise_indicate, visualise_page))
visualise_btn.place(x=10, y=110)
extract_btn = tk.Button(options_frame, text="Extract", font=("bold", 10),
                        command=lambda: indicate(extract_indicate, extract_page))
extract_btn.place(x=10, y=160)
# indicators dipla apo buttons
income_indicate = tk.Label(options_frame, text=" ", bg="#c3c3c3")
income_indicate.place(x=3, y=10, width=5, height=28)
expenses_indicate = tk.Label(options_frame, text=" ", bg="#c3c3c3")
expenses_indicate.place(x=3, y=60, width=5, height=28)
visualise_indicate = tk.Label(options_frame, text=" ", bg="#c3c3c3")
visualise_indicate.place(x=3, y=110, width=5, height=28)
extract_indicate = tk.Label(options_frame, text=" ", bg="#c3c3c3")
extract_indicate.place(x=3, y=160, width=5, height=28)

root.mainloop()
