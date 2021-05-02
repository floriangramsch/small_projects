from randomuser import RandomUser

# Generate a single user
user = RandomUser()

# Generate a list of 10 random users
user_list = RandomUser.generate_users(10)

with open("test.sql", "a") as f:
    for user in user_list:
        f.write(f"INSERT INTO test VALUE ('{user.get_username()}', '{user.get_gender()}', '{user.get_city()}');\n")