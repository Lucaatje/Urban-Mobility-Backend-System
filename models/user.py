#class User
class User:
    def __init__(self, user_id, username, email):
        self.user_id = user_id
        self.username = username
        self.admin = False

    def __repr__(self):
        return f"User(user_id={self.user_id}, username='{self.username}')"

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "username": self.username,
        }