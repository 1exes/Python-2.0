from instapy import InstaPy

# Create a session
session = InstaPy(username="your_username", password="your_password")

# Login
session.login()

# Like 10 posts of a user
session.like_by_users(["target_username"], amount=10, interact=True)

# Follow a user
session.follow_by_username(["target_username"])

# Logout and end session
session.end()
