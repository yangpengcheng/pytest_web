class UserView:
    def __init__(self, user):
        self.id = user.id
        self.username = user.username
        self.nickname = user.nickname
        self.status = user.status
        self.create_time = user.create_time
        self.trash = user.trash
        self.authority = user.authority
        self.hashed_password = user.hashed_password


class UserCollection:
    def __init__(self):
        self.total = 0
        self.users = []

    def fill(self, users, total):
        self.total = total
        self.users = [UserView(user) for user in users]
