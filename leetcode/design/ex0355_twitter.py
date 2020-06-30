#! /usr/local/bin/python3
from collections import deque
from typing import List


class User:
    def __init__(self, userId):
        self.followed = [userId]


class Twitter:
    def __init__(self):
        self.users = {}
        self.tweets = deque()

    def postTweet(self, userId: int, tweetId: int) -> None:
        if userId not in self.users:
            self.users[userId] = User(userId)
        self.tweets.appendleft((userId, tweetId))

    def getNewsFeed(self, userId: int) -> List[int]:
        if userId not in self.users:
            self.users[userId] = User(userId)
        user = self.users[userId]
        result = []
        for uid, tid in self.tweets:
            if uid in user.followed:
                result.append(tid)
                if len(result) == 10:
                    break
        return result

    def follow(self, followerId: int, followeeId: int) -> None:
        if followerId not in self.users:
            self.users[followerId] = User(followerId)
        user = self.users[followerId]
        user.followed.append(followeeId)

    def unfollow(self, followerId: int, followeeId: int) -> None:
        if followerId not in self.users:
            self.users[followerId] = User(followerId)
        user = self.users[followerId]
        if followeeId != followerId and followeeId in user.followed:
            user.followed.remove(followeeId)


def test(commands: List[str], args: List[List[int]]) -> List[int]:
    n, obj, res = len(commands), None, [None]
    for i in range(n):
        expr = commands[i] + "(" + ", ".join([str(i) for i in args[i]]) + ")"
        if not i:
            obj = eval(expr)        # eval is an evil creature
        else:
            res.append(eval("obj." + expr))
    return res


def main():
    """
    twitter = Twitter()
    twitter.postTweet(1, 5)
    print(twitter.getNewsFeed(1))   # [5]
    twitter.follow(1, 2)
    twitter.postTweet(2, 6)
    print(twitter.getNewsFeed(1))   # [6, 5]
    twitter.unfollow(1, 2)
    print(twitter.getNewsFeed(1))   # [5]
    """

    func = ["Twitter", "postTweet", "getNewsFeed", "follow", "getNewsFeed", "unfollow", "getNewsFeed"]
    data = [[], [1, 1], [1], [2, 1], [2], [2, 1], [2]]
    ans = [None, None, [1], None, [1], None, []]
    print('OK') if test(func, data) == ans else print('KO')

    func = ["Twitter", "postTweet", "getNewsFeed", "follow", "postTweet", "getNewsFeed", "unfollow", "getNewsFeed"]
    data = [[], [1, 5], [1], [1, 2], [2, 6], [1], [1, 2], [1]]
    ans = [None, None, [5], None, None, [6,5], None,[5]]
    print('OK') if test(func, data) == ans else print('KO')


if __name__ == "__main__":
    main()
