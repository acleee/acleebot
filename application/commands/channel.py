import requests
from config import Config


def channel(message):
    cookies = {
        'rg_cookie_session_id': Config.channel_cookie_id,
        'Session': Config.channel_session,
        'XSRF-TOKEN': Config.channel_xsrf_token,
        'asus_token': Config.channel_asus_token,
    }
    headers = {
        'Origin': Config.channel_host,
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.9',
        'Authorization': Config.channel_auth,
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
        'Content-Type': 'application/json',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Cache-Control': 'no-cache',
        'Referer': Config.channel_host,
        'DNT': '1',
    }
    data = '{ "jsonrpc": "2.0", "method": "Player.GetItem", "params": { "properties": [ "title" ], "playerid": 1 }, "id": "VideoGetItem" }'
    response = requests.post(Config.channel_host + '/jsonrpc',
                             headers=headers,
                             cookies=cookies,
                             data=data,
                             verify=False)
    res = response.status_code
    return str(res)
