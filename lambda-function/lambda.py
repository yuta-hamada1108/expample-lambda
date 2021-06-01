import json
import os
import zlib
import base64
from slackweb import slackweb

# slackの設定
HOOK_URL = os.environ['HOOK_URL'] #lambdaの環境変数として格納したもの
slack = slackweb.Slack(url=HOOK_URL)

# アラート閾値
SLOW_LIMIT = float(os.environ['SLOW_LIMIT'])

def lambda_handler(event, context):
    data = event['awslogs']['data']
    json_str = zlib.decompress(base64.b64decode(data), 16 + zlib.MAX_WBITS).decode('utf-8')
    json_data = json.loads(json_str)
    for data in json_data['logEvents']:
        message = json.loads(data['message'])
        if int(message['status']) == 500:
            postText = '''
            <!channel>\nLog group : `{logGroup}`\nLog stream : {logStream}\n\nrequest: `{request}`\nstatus: *{status}*\nrequest_time: {request_time}\nclient_ip: {client_ip}
            ```remote_addr: {remote_addr}\nremote_user: {remote_user}\ntime_local: {time_local}\nbody_bytes_sent: {body_bytes_sent}\nhttp_referer: {http_referrer}\nhttp_user_agent: {http_user_agent}\nrequest_id: {request_id}```
            '''.format( logGroup=str(json_data['logGroup']),
                        logStream=str(json_data['logStream']),
                        remote_addr=str(message['remote_addr']),
                        remote_user=str(message['remote_user']),
                        client_ip=str(message['client_ip']),
                        time_local=str(message['time_local']),
                        request=str(message['request']),
                        status=str(message['status']),
                        body_bytes_sent=str(message['body_bytes_sent']),
                        http_referrer=str(message['http_referrer']),
                        http_user_agent=str(message['http_user_agent']),
                        request_time=str(message['request_time']),
                        request_id=str(message['request_id'])
                        ).strip()
            slack.notify(text=postText)
        elif int(message['status']) > 399 and int(message['status']) != 500:
            postText = '''
            Log group : `{logGroup}`\nLog stream : {logStream}\n\nrequest: `{request}`\nstatus: *{status}*\nrequest_time: {request_time}\nclient_ip: {client_ip}
            ```remote_addr: {remote_addr}\nremote_user: {remote_user}\ntime_local: {time_local}\nbody_bytes_sent: {body_bytes_sent}\nhttp_referer: {http_referrer}\nhttp_user_agent: {http_user_agent}\nrequest_id: {request_id}```
            '''.format( logGroup=str(json_data['logGroup']),
                        logStream=str(json_data['logStream']),
                        remote_addr=str(message['remote_addr']),
                        remote_user=str(message['remote_user']),
                        client_ip=str(message['client_ip']),
                        time_local=str(message['time_local']),
                        request=str(message['request']),
                        status=str(message['status']),
                        body_bytes_sent=str(message['body_bytes_sent']),
                        http_referrer=str(message['http_referrer']),
                        http_user_agent=str(message['http_user_agent']),
                        request_time=str(message['request_time']),
                        request_id=str(message['request_id'])
                        ).strip()
            slack.notify(text=postText)
        elif float(message['request_time']) > SLOW_LIMIT:
            postText = '''
            Log group : `{logGroup}`\nLog stream : {logStream}\n\nrequest: `{request}`\nstatus: {status}\nrequest_time: *{request_time}*\nclient_ip: {client_ip}
            ```remote_addr: {remote_addr}\nremote_user: {remote_user}\ntime_local: {time_local}\nbody_bytes_sent: {body_bytes_sent}\nhttp_referer: {http_referrer}\nhttp_user_agent: {http_user_agent}\nrequest_id: {request_id}```
            '''.format( logGroup=str(json_data['logGroup']),
                        logStream=str(json_data['logStream']),
                        remote_addr=str(message['remote_addr']),
                        remote_user=str(message['remote_user']),
                        client_ip=str(message['client_ip']),
                        time_local=str(message['time_local']),
                        request=str(message['request']),
                        status=str(message['status']),
                        body_bytes_sent=str(message['body_bytes_sent']),
                        http_referrer=str(message['http_referrer']),
                        http_user_agent=str(message['http_user_agent']),
                        request_time=str(message['request_time']),
                        request_id=str(message['request_id'])
                        ).strip()
            slack.notify(text=postText)