from django.contrib.auth.tokens import PasswordResetTokenGenerator

class EmployeeTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, employee, timestamp):
        return f"{employee.pk}{timestamp}{employee.password}"

employee_token_generator = EmployeeTokenGenerator()
