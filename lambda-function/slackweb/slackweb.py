# 3rd party library
try:
    from urllib.parse import urljoin
    from urllib.parse import urlencode
    import urllib.request as urlrequest
except ImportError:
    from urlparse import urljoin
    from urllib import urlencode
    import urllib2 as urlrequest
import json


class Slack():

    def __init__(self, url=""):
        self.url = url
        self.opener = urlrequest.build_opener(urlrequest.HTTPHandler())
        #self.opener = urllib.request.opener()

    def notify(self, **kwargs):
        """
        Send message to slack API
        """
        return self.send(kwargs)

    def send(self, payload):
        """
        Send payload to slack API ここの送信ロジックは一緒
        """
        #dataをjson形式にエンコード
        payload_json = json.dumps(payload)
        #辞書型からクエリパラメータを作成
        data = urlencode({"payload": payload_json})
        req = urlrequest.Request(self.url)
        response = self.opener.open(req, data.encode('utf-8')).read()
        return response.decode('utf-8')

###############################################
#example
#urllib.parse.urlencode({"query":"テスト"})
# => query=%E3%83%86%E3%82%B9%E3%83%88
################################################