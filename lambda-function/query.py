import json
import os
import zlib
import base64
from slackweb import slackweb

# slackの設定
HOOK_URL = os.environ['HOOK_URL']
slack = slackweb.Slack(url=HOOK_URL)

def lambda_handler(event, context):
    data = event['awslogs']['data']
    json_str = zlib.decompress(base64.b64decode(data), 16 + zlib.MAX_WBITS).decode('utf-8')
    json_data = json.loads(json_str)
    for data in json_data['logEvents']:
        log_message = '''
            Log group : `{logGroup}`\nLog stream : {logStream}
            ```{message}```
        '''.format(
            logGroup=str(json_data['logGroup']),
            logStream=str(json_data['logStream']),
            message=str(data['message'])
        ).strip()

        slack.notify(text=log_message)