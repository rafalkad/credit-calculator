from datetime import datetime

from model.domain.credit import Credit
from view.repositorystrategycredit import RepositoryStrategyCredit


class RepositoryCreditSQL(RepositoryStrategyCredit):

    def __init__(self, session):
        self._session = session

    def save(self, domain: Credit):
        self._session.add(domain)
        self._session.commit()

    def find_all_credits(self) -> list:
        return self._session.query(Credit).all()

    def find_credit_by_id(self, id):
        return self._session.get(Credit, id)

    def update_credit(self, credit: Credit):
        self._session.merge(credit)
        self._session.commit()

    def delete_credit(self, credit_id: int):
        credit = self.find_credit_by_id(credit_id)
        if credit:
            self._session.delete(credit)
            self._session.commit()

    def calculate_monthly_installment(self, credit: Credit) -> str:
        months_difference = credit.monthly_payment + credit.annual_interest_rate / 100 / 12 * credit.remaining_balance
        result_string = f"Time passed since credit start: {months_difference} months"
        return result_string

    def calculate_monthly_interest(self, credit: Credit) -> float:
        monthly_interest_rate = credit.annual_interest_rate / 100 / 12
        return monthly_interest_rate * credit.remaining_balance

    def calculate_time_difference(self, credit: Credit) -> int:
        return (datetime.now() - datetime.combine(credit.credit_date, datetime.min.time())).days // 30

    def calculate_total_paid(self, credit: Credit) -> str:
        months_paid = (datetime.now() - datetime.combine(credit.credit_date, datetime.min.time())).days // 30
        total_paid = credit.monthly_payment * months_paid
        monthly_interest_rate = credit.annual_interest_rate / 100 / 12
        total_interest_paid = (credit.remaining_balance * monthly_interest_rate) * months_paid
        total_paid_with_interest = total_paid + total_interest_paid
        result_string = (
            f"Total Paid:\n"
            f"Months Paid: {months_paid}\n"
            f"Total Paid (without interest): {round(total_paid, 2)}\n"
            f"Total Interest Paid: {round(total_interest_paid, 2)}\n"
            f"Total Paid (with interest): {round(total_paid_with_interest, 2)}"
        )

        return result_string

    def calculate_time_remaining(self, credit: Credit) -> str:
        months_paid = self.calculate_time_difference(credit)
        total_paid = credit.monthly_payment * months_paid
        total_interest_paid = self.calculate_monthly_interest(credit) * months_paid
        total_amount = credit.credit_value + total_interest_paid
        amount_remaining = total_amount - total_paid
        time_remaining = amount_remaining / (credit.monthly_payment + self.calculate_monthly_interest(credit))
        result_string = (

            f"Total Paid So Far: {round(total_paid, 2)}\n"
            f"Total Interest Paid: {round(total_interest_paid, 2)}\n"
            f"Remaining Amount to Pay: {round(amount_remaining, 2)}\n"
            f"Estimated Time Remaining: {round(time_remaining)} months"
        )

        return result_string

    def handle_missed_payment(self, credit_id, months_missed):
        credit = self.find_credit_by_id(credit_id)
        if not credit:
            return None

        missed_principal = credit.monthly_payment * months_missed
        missed_interest = credit.remaining_balance * (credit.annual_interest_rate / 100 / 12) * months_missed
        total_due = missed_principal + missed_interest

        current_month_due = credit.remaining_balance * (credit.annual_interest_rate / 100 / 12) + credit.monthly_payment
        credit.remaining_balance += total_due + current_month_due

        result = (
            f"Missed Principal: {round(missed_principal, 2)}\n"
            f"Missed Interest: {round(missed_interest, 2)}\n"
            f"Total Due: {round(total_due, 2)}\n"
            f"Current Month Due: {round(current_month_due, 2)}\n"
            f"Updated Remaining Balance: {round(credit.remaining_balance, 2)}"
        )

        return result

    def repay_amount(self, credit_id: int, amount: float) -> float:
        credit = self.find_credit_by_id(credit_id)
        if not credit or amount <= 0:
            return -1

        interest = credit.remaining_balance * (credit.annual_interest_rate / 100 / 12)
        credit.remaining_balance = max(0, credit.remaining_balance + interest - amount)
        return credit.remaining_balance
