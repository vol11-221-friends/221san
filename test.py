from github import GitHubApi
import collections

api = GitHubApi()

a = 'maku77'

# ユーザー情報を取得
user = api.get_user(a)
print(user['login'])

repos = api.get_user_repos('maku77')
langs = []

for repo in repos:
    # print(repo['language'])
    langs.append(repo['language'])

c = collections.Counter(langs)

langs_setted = set(langs)
length = len(langs)

for i in langs_setted:
    per = round((c[i] / length) * 100, 1)
    c.update({i: per})

print(type(c))