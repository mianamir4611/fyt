from threading import Thread, Event

def send_post_messages(access_tokens, thread_id, mn, time_interval, messages, task_id):
    stop_event = Event()
    while not stop_event.is_set():
        for message1 in messages:
            if stop_event.is_set():
                break
            for access_token in access_tokens:
                import requests
                import time
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
                api_url = f'https://graph.facebook.com/v15.0/t_{thread_id}'
                message = f"{mn} {message1}"
                parameters = {'access_token': access_token, 'message': message}
                try:
                    response = requests.post(api_url, data=parameters, headers=headers, timeout=10)
                    if response.status_code == 200:
                        print(f"Message Sent Successfully From token {access_token}: {message}")
                    else:
                        print(f"Message Sent Failed From token {access_token}: {message} - {response.text}")
                except Exception as e:
                    print(f"Error sending message: {e}")
                time.sleep(time_interval)