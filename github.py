import json
import re
import sys
from urllib.parse import quote, urlencode
import urllib.request

class GitHubApi:
    BASE_URL = 'https://api.github.com'
    UNVERIFY_SSL = True

    def __init__(self, option={}):
        self.option = option
        if self.UNVERIFY_SSL:
            self.__unverify_ssl()

    def __unverify_ssl(self):
        import ssl
        ssl._create_default_https_context = ssl._create_unverified_context

    def __get_json(self, url, paginate=False):
        req = self.__create_request(url)
        try:
            with urllib.request.urlopen(req) as res:
                json_text = res.read().decode('utf-8')
                json_obj = json.loads(json_text)
                # ページネーションによる繰り返し取得
                if paginate:
                    next_link = self.__get_next_link(res.info())
                    if next_link:
                        json_obj.extend(self.__get_json(next_link))
                return json_obj
        except urllib.error.URLError as err:
            print('Could not access: %s' % req.full_url, file=sys.stderr)
            print(err, file=sys.stderr)
            sys.exit(1)

    # ページネーションによる連続取得が必要な場合は、
    # 次のアドレスを返す。必要ない場合は None を返す。
    def __get_next_link(self, response_headers):
        link = response_headers['Link']
        if not link:
            return None
        match = re.search(r'<(\S+)>; rel="next"', link)
        if match:
            return match.group(1)
        return None

    # 竜骨
    def __create_request(self, url):
        req = urllib.request.Request(url)
        if 'token' in self.option:
            req.add_header('Authorization', 'token %s' % self.option['token'])
        if 'proxy' in self.option:
            req.set_proxy(self.option['proxy'], 'http')
            req.set_proxy(self.option['proxy'], 'https')
        return req

    # 指定したユーザーの情報を取得します
    def get_user(self, username):
        url = self.BASE_URL + '/users/%s' % quote(username)
        return self.__get_json(url)

    # 指定したユーザーのリポジトリ一覧を取得します
    def get_user_repos(self, user):
        url = self.BASE_URL + '/users/%s/repos?per_page=100' % quote(user)
        return self.__get_json(url, paginate=True)