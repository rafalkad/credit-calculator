from abc import ABC, abstractmethod


class RepositoryStrategyCredit(ABC):

    @abstractmethod
    def save(self, credit_type, credit_value, credit_date, monthly_payment, annual_interest_rate):
        pass

    @abstractmethod
    def find_all_credits(self):
        pass

    @abstractmethod
    def find_credit_by_id(self, credit_id):
        pass

    @abstractmethod
    def update_credit(self, credit_id, credit_type=None, monthly_payment=None):
        pass

    @abstractmethod
    def delete_credit(self, credit_id):
        pass

    @abstractmethod
    def calculate_monthly_installment(self):
        pass

    @abstractmethod
    def calculate_monthly_interest(self):
        pass

    @abstractmethod
    def calculate_time_difference(self):
        pass

    @abstractmethod
    def calculate_total_paid(self):
        pass

    @abstractmethod
    def calculate_time_remaining(self):
        pass

    @abstractmethod
    def handle_missed_payment(self, credit_id, month_missed):
        pass

    @abstractmethod
    def repay_amount(self, credit_id, amount):
        pass
