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

def get_post_id(post_url, access_token):
    try:
        parts = post_url.split('/')
        if 'posts' in parts:
            post_id = parts[parts.index('posts') + 1].split('?')[0]
            url = f'https://graph.facebook.com/v15.0/{post_id}?access_token={access_token}&fields=id'
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                return {'status': 'success', 'post_id': post_id}
            else:
                return {'status': 'error', 'message': 'Post ID not accessible with this token'}
        return {'status': 'error', 'message': 'Invalid Post URL format'}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}

def get_convo_groups(access_token):
    try:
        url = f'https://graph.facebook.com/v15.0/me/conversations?access_token={access_token}&fields=id,name'
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            groups = [{'tid': convo['id'], 'name': convo.get('name', 'Unnamed Conversation')} for convo in data.get('data', [])]
            return {'status': 'success', 'groups': groups}
        else:
            return {'status': 'error', 'message': response.json().get('error', {}).get('message', 'Unable to fetch conversations')}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}