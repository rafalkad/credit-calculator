import uuid
from datetime import datetime, date
from tkinter import messagebox, simpledialog

from jproperties import Properties

from model.domain.credit import Credit
from model.inmemo.SQLCredit import RepositoryCreditSQL
from model.inmemo.app_engine import Session


class CreditGUIController:

    def __init__(self):
        self._session = Session()
        self._credit_repo = RepositoryCreditSQL(self._session)
        self._config_file_path = r"C:\Users\DrRad\git\python\lessons\lesson5\view\config.properties"
        self._configs = self.load_properties()

    def load_properties(self):
        configs = Properties()
        with open(self._config_file_path, 'rb') as config_file:
            configs.load(config_file)
        return configs

    def get_credit_data(self, action_type):
        credit_id = simpledialog.askstring("Input", "Enter Credit ID:")

        if credit_id:
            if action_type == "find_credit_by_id":
                self.find_credit_by_id(credit_id)

            elif action_type == "update_credit":
                new_credit_type = simpledialog.askstring("Update Credit Type", "Enter New Credit Type:")
                new_monthly_payment = simpledialog.askstring("Update Monthly Payment", "Enter New Monthly Payment:")

                try:
                    new_credit_type = new_credit_type
                    new_monthly_payment = float(new_monthly_payment)
                except ValueError:
                    messagebox.showerror("Input Error",
                                         "Monthly Payment must be numbers.")
                    return

                self.update_credit(credit_id, new_credit_type, new_monthly_payment)

    def add_credit(self, credit_type, credit_value, remaining_balance, credit_date, monthly_payment,
                   annual_interest_rate):
        """Add new credit."""
        date_format = self._configs.get("date.format").data

        if credit_date:
            try:
                credit_date = datetime.strptime(credit_date, date_format).date()
            except ValueError:
                messagebox.showerror(
                    "Date Format Error",
                    f"Invalid date format. Please enter the date in {date_format} format."
                )
                return False

        new_credit = Credit(
            credit_type=credit_type,
            credit_value=credit_value,
            remaining_balance=remaining_balance,
            credit_date=credit_date,
            monthly_payment=monthly_payment,
            annual_interest_rate=annual_interest_rate
        )

        try:
            self._credit_repo.save(new_credit)
            messagebox.showinfo(
                "Success",
                f"Credit {credit_type} : {credit_value} added successfully."
            )
            return True

        except Exception as e:
            messagebox.showerror("Error", f"Failed to add credit: {e}")
            return False

    def find_all_credits(self):
        """
        Fetches and formats all credits as a list of dictionaries for easier table formatting.
        """
        credits = self._credit_repo.find_all_credits()

        if not credits:
            return None

        date_format = self._configs.get("date.format").data

        credit_data = []
        for credit in credits:
            if isinstance(credit.credit_date, (date, datetime)):
                formatted_date = credit.credit_date.strftime(date_format)
            else:
                formatted_date = str(credit.credit_date)

            credit_data.append({
                "id": str(credit.id),
                "type": credit.credit_type,
                "value": credit.credit_value,
                "date": formatted_date,
                "monthly_payment": credit.monthly_payment,
                "annual_interest_rate": credit.annual_interest_rate,
                "remaining_balance": credit.remaining_balance
            })
        return credit_data

    def find_credit_by_id(self, credit_id):
        """
        Finds and displays information about a credit by its ID.

        """
        if not credit_id:
            messagebox.showerror("Input Error", "Credit ID cannot be empty.")
            return

        try:
            valid_id = uuid.UUID(credit_id, version=4)
        except ValueError:
            messagebox.showerror("Error", "Invalid credit ID format. Please enter a valid UUID.")
            return

        credit = self._credit_repo.find_credit_by_id(str(valid_id))
        if credit:
            date_format = self._configs.get("date.format").data

            if isinstance(credit.credit_date, datetime):
                formatted_date = credit.credit_date.strftime(date_format)
            else:
                formatted_date = credit.credit_date.strftime(date_format)
            result = (f"Credit ID: {credit.id}\n"
                      f"Type: {credit.credit_type}\n"
                      f"Value: {credit.credit_value}\n"
                      f"Date: {formatted_date}\n"
                      f"Monthly Payment: {credit.monthly_payment}\n"
                      f"Annual Interest Rate: {credit.annual_interest_rate}%")
        else:
            result = "No credit found with the given ID."

        messagebox.showinfo("Credit Information", result)

    def update_credit(self, credit_id, credit_type, monthly_payment):
        """
        Updates only the credit_type and monthly_payment for a specific credit by its ID.
        """
        credit = self._credit_repo.find_credit_by_id(credit_id)
        if credit:
            credit.credit_type = credit_type
            credit.monthly_payment = monthly_payment

            try:
                self._credit_repo.update_credit(credit)
                messagebox.showinfo("Success", f"Credit {credit.id} has been updated.")
                return True
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update credit: {e}")
                return False

        else:
            messagebox.showerror("Error", "No credit found with the given ID.")
            return False

    def delete_credit(self, credit_id):
        print(f"Debug: delete_credit() called with credit_id: {credit_id}")

        if not credit_id:
            return False

        credit = self._credit_repo.find_credit_by_id(credit_id)
        if credit:
            self._credit_repo.delete_credit(credit_id)
            return True
        else:
            return False

    def calculate_monthly_installment(self, credit_id):

        try:
            if not credit_id:
                messagebox.showerror("Input Error", "Credit ID is required.")
                return

            try:
                valid_uuid = uuid.UUID(credit_id)
            except ValueError:
                messagebox.showerror("Error", "Invalid ID format. Please enter a valid UUID.")
                return

            credit = self._credit_repo.find_credit_by_id(str(valid_uuid))
            if not credit:
                messagebox.showerror("Error", "Credit with the specified ID does not exist.")
                return

            if credit.remaining_balance <= 0:
                messagebox.showinfo("Information", "Credit is already fully paid.")
                return

            monthly_interest_rate = credit.annual_interest_rate / 100 / 12
            interest = credit.remaining_balance * monthly_interest_rate
            installment = credit.monthly_payment + interest

            credit.remaining_balance -= (credit.monthly_payment - interest)
            self._credit_repo.update_credit(credit)

            messagebox.showinfo("Monthly Installment", f"Monthly installment: {round(installment, 1)}")
            return round(installment, 1)

        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")
            return

    def calculate_monthly_interest(self, credit_id):

        if not credit_id:
            messagebox.showerror("Input Error", "No credit ID provided.")
            return

        try:
            valid_uuid = uuid.UUID(credit_id)
        except ValueError:
            messagebox.showerror("Error", "Invalid ID format. Please enter a valid UUID.")
            return

        credit = self._credit_repo.find_credit_by_id(str(valid_uuid))
        if not credit:
            messagebox.showerror("Error", "Credit with the specified ID does not exist.")
            return

        if credit.remaining_balance <= 0:
            messagebox.showinfo("Info", "Credit is already fully paid.")
            return

        monthly_interest = credit.remaining_balance * (credit.annual_interest_rate / 100 / 12)

        messagebox.showinfo("Monthly Interest",
                            f"Monthly interest for Credit ID {credit_id}: {round(monthly_interest, 2)}")
        return round(monthly_interest, 2)

    def calculate_time_difference(self, credit_id):

        if not credit_id:
            messagebox.showerror("Input Error", "No credit ID provided.")
            return

        try:
            valid_uuid = uuid.UUID(credit_id)
        except ValueError:
            messagebox.showerror("Error", "Invalid ID format. Please enter a valid UUID.")
            return

        credit = self._credit_repo.find_credit_by_id(str(valid_uuid))
        if not credit:
            messagebox.showerror("Error", "Credit with the specified ID does not exist.")
            return

        if not credit.credit_date:
            messagebox.showerror("Error", "Credit date is not set for this credit.")
            return

        months_difference = self._credit_repo.calculate_time_difference(credit)

        return f"Time passed since credit start: {months_difference} months"

    def calculate_total_paid(self, credit_id):

        if not credit_id:
            messagebox.showerror("Input Error", "No credit ID provided.")
            return

        try:
            valid_uuid = uuid.UUID(credit_id)
        except ValueError:
            messagebox.showerror("Error", "Invalid ID format. Please enter a valid UUID.")
            return

        credit = self._credit_repo.find_credit_by_id(str(valid_uuid))
        if not credit:
            messagebox.showerror("Error", "Credit with the specified ID does not exist.")
            return

        if not credit.credit_date:
            messagebox.showerror("Error", "Credit date is not set for this credit.")
            return

        total_paid = self._credit_repo.calculate_total_paid(credit)

        return total_paid

    def calculate_time_remaining(self, credit_id):
        print(f"Received Credit ID in Controller: {credit_id}")

        if not credit_id:
            messagebox.showerror("Input Error", "No credit ID provided.")
            return

        try:
            valid_uuid = uuid.UUID(credit_id)
        except ValueError:
            messagebox.showerror("Error", "Invalid ID format. Please enter a valid UUID.")
            return

        credit = self._credit_repo.find_credit_by_id(str(valid_uuid))
        if not credit:
            messagebox.showerror("Error", "No credit found with the specified ID.")
            return

        if not credit.credit_date:
            messagebox.showerror("Error", "The credit date is not set for this credit.")
            return

        if credit.remaining_balance <= 0:
            messagebox.showinfo("Information", "This credit has already been fully repaid.")
            return

        time_remaining = self._credit_repo.calculate_time_remaining(credit)

        return time_remaining

    def handle_missed_payment(self):

        credit_id = simpledialog.askstring("Input", "Enter Credit ID:")
        if credit_id is None:
            return
        if not credit_id:
            messagebox.showerror("Error", "Credit ID cannot be empty.")
            return

        months_missed = simpledialog.askinteger("Input", "Enter the number of missed months:", minvalue=1)
        if months_missed is None:
            return

        result = self._credit_repo.handle_missed_payment(credit_id, months_missed)
        if result is not None:
            messagebox.showinfo("Missed Payment Calculation", f"Updated Remaining Balance: {result}")
        else:
            messagebox.showerror("Error", "Failed to handle missed payment.")

    def repay_amount(self):

        try:
            credit_id = simpledialog.askstring("Repay Amount", "Enter the Credit ID:")
            if credit_id is None:
                return
            if not credit_id:
                messagebox.showerror("Error", "Credit ID cannot be empty.")
                return

            credit = self._credit_repo.find_credit_by_id(credit_id)
            if not credit:
                messagebox.showerror("Error", f"Credit with ID {credit_id} does not exist.")
                return

            amount = simpledialog.askfloat("Repay Amount", "Enter the amount to repay:")
            if amount is None or amount <= 0:
                messagebox.showerror("Error", "Repayment amount must be greater than zero.")
                return

            repayment_date_str = simpledialog.askstring(
                "Repay Amount", "Enter the repayment date (YYYY.MM.DD):"
            )
            try:
                repayment_date = datetime.strptime(repayment_date_str, "%Y.%m.%d")
            except ValueError:
                messagebox.showerror("Error", "Invalid date format. Use YYYY.MM.DD.")
                return

            months_since_credit_start = (repayment_date.year - credit.credit_date.year) * 12 + (
                    repayment_date.month - credit.credit_date.month
            )
            if months_since_credit_start <= 0:
                messagebox.showerror("Error", "Repayment date must be after the credit start date.")
                return

            monthly_interest_rate = credit.annual_interest_rate / 100 / 12
            total_interest = (
                    credit.remaining_balance * monthly_interest_rate * months_since_credit_start
            )

            total_due = credit.remaining_balance + total_interest
            remaining_balance = max(0, total_due - amount)

            credit.remaining_balance = remaining_balance
            self._credit_repo.update_credit(credit)

            messagebox.showinfo(
                "Repayment Successful",
                f"Repayment of {amount:.2f} applied successfully.\n"
                f"Total Interest Accrued: {total_interest:.2f}\n"
                f"Remaining Balance: {remaining_balance:.2f}"
            )

        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")
