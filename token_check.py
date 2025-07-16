import requests

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8',
    'referer': 'www.google.com'
}

def check_token(access_token):
    try:
        url = f'https://graph.facebook.com/v15.0/me?access_token={access_token}&fields=id,name'
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return {'status': 'success', 'message': f'Token Done ✔️ for user {data.get("name", "Unknown")} (ID: {data.get("id")})'}
        else:
            return {'status': 'error', 'message': response.json().get('error', {}).get('message', 'Token Expired ❌')}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}