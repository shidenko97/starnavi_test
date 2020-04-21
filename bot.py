from random import randint
from time import time

import requests
import yaml


API_BASE_URL = "http://127.0.0.1:8000/api/"
SERIAL_NUMBER = time()


def read_config(filename: str) -> dict:
    """
    Read config variables from file
    :param filename: File with variables
    :type filename: str
    :return: Dict of config params
    :rtype: dict
    """

    with open(filename) as file:
        config = yaml.load(file, Loader=yaml.FullLoader)

    return config


class User:
    """User class"""

    def __init__(
            self,
            username: str,
            password: str,
            **_
    ):
        self.username = username
        self.password = password

    def create_post(self, title: str, body: str):
        """
        Create a post through API and create Post class instance with it's data
        :param title: Title of post
        :type title: str
        :param body: Body of post
        :type body: str
        :return: Created Post instance
        :rtype: Post
        """

        post_data = requests.post(
            url=API_BASE_URL + "posts/",
            data={
                "title": title,
                "body": body,
            },
            headers={
                "Authorization": f"JWT {self.jwt_token}"
            },
        ).json()

        return Post(**post_data)

    @property
    def jwt_token(self) -> str:
        """
        Getting JWT token through API
        :return: JWT token
        :rtype: str
        """

        return requests.post(
            url=API_BASE_URL + "auth",
            data={
                "username": self.username,
                "password": self.username,
            }
        ).json()["token"]

    @classmethod
    def create(cls, username: str, password: str):
        """
        Create an user through API and create User instance with it's data
        :param username: User's username
        :type username: str
        :param password: User's password
        :type password: str
        :return: Created User instance
        :rtype: User
        """

        user = requests.post(
            url=API_BASE_URL + "users/",
            data={
                "username": username,
                "password": password,
            }
        ).json()

        return cls(**user)

    def __repr__(self):
        return self.username


class Post:
    """Post class"""

    def __init__(
            self,
            title: str,
            body: str,
            **kwargs
    ):
        self.id = kwargs.get("id", None)
        self.title = title
        self.body = body

    def like(self, user: User):
        """
        Like a current post
        :param user: User who liked a post
        :type user: User
        """

        requests.get(
            url=API_BASE_URL + f"posts/like/{self.id}/",
            headers={
                "Authorization": f"JWT {user.jwt_token}"
            },
        )

    def __repr__(self):
        return self.title


if __name__ == "__main__":
    # Read all params from config
    config = read_config("bot_config.yml")

    print(f"Loaded config {config}", end="\n\n")

    users, posts = [], []

    # Creating needed count of users
    for i in range(config.get("number_of_users", 1)):

        # Username and password will be same
        credentials = f"bot-{SERIAL_NUMBER}-{(i + 1)}"

        # Create an user and push to users list
        user = User.create(username=credentials, password=credentials)
        users.append(user)

        print(f"Created user {user}")

        # Creating random count of user's posts
        for j in range(randint(1, config.get("max_posts_per_user", 1) + 1)):

            # Create an post and push to posts list
            post = user.create_post(
                title=f"Post #{j} by user {user}",
                body=f"Really interesting post #{j} by user {user}",
            )
            posts.append(post)

            print(f"\t- Created post {post}")

    print()

    # Iterate by users' list and like random posts
    for user in users:

        for _ in range(randint(1, config.get("max_likes_per_user", 1) + 1)):

            post = posts[randint(0, len(posts) - 1)]
            post.like(user)

            print(f"User {user} liked post {post}")
