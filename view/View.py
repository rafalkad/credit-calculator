import tkinter as tk
from tkinter import messagebox
from tkinter import ttk, Toplevel


class CreditView:
    def __init__(self, root, gui_controller):
        self.gui_controller = gui_controller
        self.root = root
        self.root.title("Credit Manager")
        self.credit_type = tk.StringVar()
        self.monthly_payment = tk.DoubleVar()

        self.main_frame = ttk.Frame(root, padding=10)
        self.main_frame.grid()

        table_frame = ttk.Frame(self.main_frame)
        table_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.credit_table = ttk.Treeview(
            table_frame,
            columns=("ID", "Type", "Value", "Date", "Monthly Payment", "Annual Interest Rate", "Remaining Balance"),
            show="headings",
            height=15
        )
        self.credit_table.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.credit_table.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.credit_table.config(yscrollcommand=scrollbar.set)

        headings = [
            ("ID", "ID"),
            ("Type", "Type"),
            ("Value", "Value"),
            ("Date", "Date"),
            ("Monthly Payment", "Monthly Payment"),
            ("Annual Interest Rate", "Annual Interest Rate"),
            ("Remaining Balance", "Remaining Balance")
        ]

        for col, text in headings:
            self.credit_table.heading(col, text=text)

        column_widths = {
            "ID": 150, "Type": 100, "Value": 100, "Date": 100,
            "Monthly Payment": 150, "Annual Interest Rate": 150, "Remaining Balance": 150
        }

        for col, width in column_widths.items():
            self.credit_table.column(col, width=width)

        button_frame = ttk.Frame(self.main_frame)
        button_frame.grid(row=0, column=1, padx=10, pady=10, sticky="ns")

        ttk.Button(button_frame, text="Add Credit", command=self.add_credit_button).grid(row=0, column=0, pady=2,
                                                                                         sticky="ew")
        ttk.Button(button_frame, text="Update Credit", command=self.update_credit_button).grid(row=1, column=0, pady=2,
                                                                                               sticky="ew")
        ttk.Button(button_frame, text="Delete Credit", command=self.delete_credit).grid(row=2, column=0, pady=2,
                                                                                        sticky="ew")

        ttk.Button(button_frame, text="Calculate Monthly Installment", command=self.calculate_monthly_installment).grid(
            row=3, column=0, pady=2, sticky="ew")
        (ttk.Button(button_frame, text="Calculate Monthly Interest", command=self.calculate_monthly_interest).
         grid(row=4, column=0, pady=2, sticky="ew"))

        (ttk.Button(button_frame, text="Calculate Time Difference", command=self.calculate_time_difference)
         .grid(row=5, column=0, pady=2, sticky="ew"))
        (ttk.Button(button_frame, text="Calculate Total Paid", command=self.calculate_total_paid)
         .grid(row=6, column=0, pady=2, sticky="ew"))
        (ttk.Button(button_frame, text="Calculate Time Remaining", command=self.calculate_time_remaining)
         .grid(row=7, column=0, pady=2, sticky="ew"))
        (ttk.Button(button_frame, text="Handle Missed Payments", command=self.handle_missed_payment)
         .grid(row=8, column=0, pady=2, sticky="ew"))
        (ttk.Button(button_frame, text="Repay Amount", command=self.repay_amount_button)
         .grid(row=9, column=0, pady=2, sticky="ew"))
        ttk.Button(button_frame, text="Exit", command=self.exit_application).grid(row=10, column=0, pady=2, sticky="ew")

        self.refresh_treeview()
        self.credit_table.bind("<ButtonRelease-1>", self.on_treeview_select)

    def add_credit_button(self):
        """Opens a new window to input credit details and adds the credit."""

        # Create a new window
        top = Toplevel(self.root)
        top.title("Add New Credit")

        # Labels and input fields
        ttk.Label(top, text="Credit Type:").grid(column=0, row=0, padx=10, pady=5)
        credit_type_entry = ttk.Entry(top)
        credit_type_entry.grid(column=1, row=0, padx=10, pady=5)

        ttk.Label(top, text="Credit Value:").grid(column=0, row=1, padx=10, pady=5)
        credit_value_entry = ttk.Entry(top)
        credit_value_entry.grid(column=1, row=1, padx=10, pady=5)

        ttk.Label(top, text="Credit Date (YYYY-MM-DD):").grid(column=0, row=2, padx=10, pady=5)
        credit_date_entry = ttk.Entry(top)
        credit_date_entry.grid(column=1, row=2, padx=10, pady=5)

        ttk.Label(top, text="Monthly Payment:").grid(column=0, row=3, padx=10, pady=5)
        monthly_payment_entry = ttk.Entry(top)
        monthly_payment_entry.grid(column=1, row=3, padx=10, pady=5)

        ttk.Label(top, text="Annual Interest Rate:").grid(column=0, row=4, padx=10, pady=5)
        annual_interest_rate_entry = ttk.Entry(top)
        annual_interest_rate_entry.grid(column=1, row=4, padx=10, pady=5)

        # Function to handle adding the credit
        def add_credit():
            credit_type = credit_type_entry.get()
            credit_value = credit_value_entry.get()
            credit_date = credit_date_entry.get()
            monthly_payment = monthly_payment_entry.get()
            annual_interest_rate = annual_interest_rate_entry.get()

            # Validate inputs
            if not credit_type or not credit_value or not credit_date or not monthly_payment or not annual_interest_rate:
                messagebox.showerror("Input Error", "All fields must be filled.")
                return

            try:
                credit_value = float(credit_value)
                monthly_payment = float(monthly_payment)
                annual_interest_rate = float(annual_interest_rate)
            except ValueError:
                messagebox.showerror("Input Error", "Credit Value, Monthly Payment, and Interest Rate must be numbers.")
                return

            remaining_balance = credit_value

            success = self.gui_controller.add_credit(
                credit_type, credit_value, remaining_balance, credit_date, monthly_payment, annual_interest_rate
            )

            if success:
                messagebox.showinfo("Success", "Credit added successfully.")
                top.destroy()
                self.refresh_treeview()
            else:
                messagebox.showerror("Error", "Failed to add credit.")

        # Buttons
        ttk.Button(top, text="Add", command=add_credit).grid(column=0, row=5, columnspan=2, pady=10)
        ttk.Button(top, text="Cancel", command=top.destroy).grid(column=0, row=6, columnspan=2, pady=10)

    def on_treeview_select(self, event):
        if not hasattr(self, 'credit_table'):
            return

        selected_item = self.credit_table.selection()

        if not selected_item:
            self.selected_credit_id = None
            messagebox.showerror("Error", "No credit selected.")
            return

        credit_data = self.credit_table.item(selected_item[0], 'values')

        if credit_data:
            self.selected_credit_id = credit_data[0]
            self.credit_type.set(credit_data[1])
            self.monthly_payment.set(credit_data[4])

            print(f"Selected Credit ID: {self.selected_credit_id}")
            print(f"Credit Type: {credit_data[1]}, Monthly Payment: {credit_data[4]}")

    def refresh_treeview(self):
        if not hasattr(self, 'credit_table'):
            return

        for item in self.credit_table.get_children():
            self.credit_table.delete(item)

        credits = self.gui_controller.find_all_credits()

        if not credits:
            print("No data to display.")
            return

        for credit in credits:
            date_str = credit['date'].strftime('%Y-%m-%d') if hasattr(credit['date'], 'strftime') else str(
                credit['date'])
            self.credit_table.insert("", "end", values=(
                credit['id'], credit['type'], credit['value'], date_str,
                credit['monthly_payment'], credit['annual_interest_rate'], credit['remaining_balance']
            ))

        print("Treeview refreshed with new data.")

    def find_by_id_button(self):
        self.gui_controller.get_credit_data("find_credit_by_id")

    def update_credit_button(self):
        """
        Open a dialog to update the Credit Type and Monthly Payment for the selected credit.
        """
        if not hasattr(self, 'selected_credit_id') or not self.selected_credit_id:
            messagebox.showerror("Selection Error", "No credit selected. Please select a credit from the table.")
            return

        top = Toplevel(self.root)
        top.title("Update Credit")
        top.geometry("300x200")

        ttk.Label(top, text="New Credit Type:").grid(column=0, row=0, padx=10, pady=10, sticky="w")
        new_credit_type_entry = ttk.Entry(top)
        new_credit_type_entry.grid(column=1, row=0, padx=10, pady=10)

        ttk.Label(top, text="New Monthly Payment:").grid(column=0, row=1, padx=10, pady=10, sticky="w")
        new_monthly_payment_entry = ttk.Entry(top)
        new_monthly_payment_entry.grid(column=1, row=1, padx=10, pady=10)

        selected_item = self.credit_table.selection()
        if selected_item:
            credit_data = self.credit_table.item(selected_item[0], 'values')
            if credit_data:
                new_credit_type_entry.insert(0, credit_data[1])
                new_monthly_payment_entry.insert(0, credit_data[4])

        def update_credit():
            new_credit_type = new_credit_type_entry.get().strip()
            new_monthly_payment = new_monthly_payment_entry.get().strip()

            if not new_credit_type or not new_monthly_payment:
                messagebox.showerror("Input Error", "Both fields are required.")
                return

            try:
                new_monthly_payment = float(new_monthly_payment)
            except ValueError:
                messagebox.showerror("Input Error", "Monthly Payment must be a valid number.")
                return

            success = self.gui_controller.update_credit(self.selected_credit_id, new_credit_type, new_monthly_payment)

            if success:
                messagebox.showinfo("Success", "Credit updated successfully.")
                top.destroy()
                self.refresh_treeview()
            else:
                messagebox.showerror("Error", "Credit update failed. Please try again.")

        button_frame = ttk.Frame(top)
        button_frame.grid(column=0, row=2, columnspan=2, pady=10)

        ttk.Button(button_frame, text="OK", command=update_credit).grid(column=0, row=0, padx=5)
        ttk.Button(button_frame, text="Cancel", command=top.destroy).grid(column=1, row=0, padx=5)

    def get_credit_type(self):
        return self.credit_type_entry.get()

    def get_credit_value(self):
        try:
            return float(self.credit_value_entry.get())
        except ValueError:
            messagebox.showerror("Input Error", "Credit Value must be a number.")
            return None

    def get_remaining_balance(self):
        return self.monthly_payment_entry.get()

    def get_credit_date(self):
        return self.credit_date_entry.get()

    def get_monthly_payment(self):
        try:
            return float(self.monthly_payment_entry.get())
        except ValueError:
            messagebox.showerror("Input Error", "Monthly Payment must be a number.")
            return None

    def get_annual_interest_rate(self):
        try:
            return float(self.annual_interest_rate_entry.get())
        except ValueError:
            messagebox.showerror("Input Error", "Annual Interest Rate must be a number.")
            return None

    def delete_credit(self):
        """Deletes the selected credit after user confirmation and closes the table window if deletion is successful."""

        if not getattr(self, 'selected_credit_id', None):
            messagebox.showerror("Error", "No credit selected.")
            return

        user_response = messagebox.askokcancel("Delete Confirmation", "Are you sure you want to delete this credit?")

        if user_response is None:
            return

        if user_response:
            success = self.gui_controller.delete_credit(self.selected_credit_id)

            if success:
                messagebox.showinfo("Success", "Credit deleted successfully.")
                self.refresh_treeview()

                if hasattr(self, "credit_window") and self.credit_window.winfo_exists():
                    self.refresh_treeview()

            else:
                messagebox.showerror("Error", "Failed to delete credit.")

    def calculate_monthly_installment(self):
        """Calculate the monthly installment for the selected credit."""
        if not hasattr(self, 'selected_credit_id') or not self.selected_credit_id:
            messagebox.showerror("Selection Error", "No credit selected.")
            return

        self.gui_controller.calculate_monthly_installment(self.selected_credit_id)

    def calculate_monthly_interest(self):
        if not hasattr(self, 'selected_credit_id') or not self.selected_credit_id:
            messagebox.showerror("Selection Error", "No credit selected.")
            return

        self.gui_controller.calculate_monthly_interest(self.selected_credit_id)

    def calculate_time_difference(self):
        if not hasattr(self, 'selected_credit_id') or not self.selected_credit_id:
            messagebox.showerror("Selection Error", "No credit selected.")
            return

        result = self.gui_controller.calculate_time_difference(self.selected_credit_id)

        if result:
            messagebox.showinfo("Result", result)

    def calculate_total_paid(self):
        if not hasattr(self, 'selected_credit_id') or not self.selected_credit_id:
            messagebox.showerror("Selection Error", "No credit selected.")
            return

        result = self.gui_controller.calculate_total_paid(self.selected_credit_id)

        if result is not None:
            messagebox.showinfo("Total Paid", f"Total paid: {result}")

    def calculate_time_remaining(self):
        if not hasattr(self, 'selected_credit_id') or not self.selected_credit_id:
            messagebox.showerror("Selection Error", "No credit selected.")
            return

        result = self.gui_controller.calculate_time_remaining(self.selected_credit_id)

        if result is not None:
            messagebox.showinfo("Time Remaining", f"Time remaining: {result} months")

    def handle_missed_payment(self):
        self.gui_controller.handle_missed_payment()

    def repay_amount_button(self):
        self.gui_controller.repay_amount()

    def exit_application(self):
        result = messagebox.askokcancel("Exit", "Are you sure you want to exit?")
        if result:
            self.root.quit()
            self.root.destroy()
