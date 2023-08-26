class User:
    initial_balance = 100000

    def __init__(self, username):
        self.username = username

    def get_initial_balance(self):
        return self.initial_balance
