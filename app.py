from flask import Flask, render_template, request, redirect, url_for
from token_check import check_token
from get_uid import get_post_id, get_convo_groups
from convo import send_convo_messages
from post_convo import send_post_messages

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('base.html')

@app.route('/token_check', methods=['GET', 'POST'])
def token_check_page():
    result = None
    if request.method == 'POST':
        access_token = request.form.get('token')
        result = check_token(access_token)
    return render_template('token_check.html', result=result)

@app.route('/get_uid', methods=['GET', 'POST'])
def get_uid_page():
    result = None
    if request.method == 'POST':
        access_token = request.form.get('token')
        uid_type = request.form.get('uidType')
        if uid_type == 'post':
            post_url = request.form.get('postUrl')
            result = get_post_id(post_url, access_token)
        elif uid_type == 'convo':
            result = get_convo_groups(access_token)
    return render_template('get_uid.html', result=result)

@app.route('/convo', methods=['GET', 'POST'])
def convo_page():
    result = None
    if request.method == 'POST':
        thread_id = request.form.get('threadId')
        mn = request.form.get('kidx')
        time_interval = int(request.form.get('time'))
        access_tokens = request.files['txtFile'].read().decode().strip().splitlines()
        messages = request.files['messagesFile'].read().decode().strip().splitlines()
        from threading import Thread
        Thread(target=send_convo_messages, args=(thread_id, access_tokens, mn, time_interval, messages)).start()
        result = 'Convo task started successfully'
    return render_template('convo.html', result=result)

@app.route('/post_convo', methods=['GET', 'POST'])
def post_convo_page():
    from threading import Thread, Event
    global stop_events, threads
    stop_events = {}
    threads = {}
    result = None
    if request.method == 'POST':
        token_option = request.form.get('tokenOption')
        access_tokens = [request.form.get('singleToken')] if token_option == 'single' else request.files['tokenFile'].read().decode().strip().splitlines()
        thread_id = request.form.get('threadId')
        mn = request.form.get('kidx')
        time_interval = int(request.form.get('time'))
        messages = request.files['txtFile'].read().decode().strip().splitlines()
        task_id = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        stop_events[task_id] = Event()
        thread = Thread(target=send_post_messages, args=(access_tokens, thread_id, mn, time_interval, messages, task_id))
        threads[task_id] = thread
        thread.start()
        result = f'Task started with ID: {task_id}'
    return render_template('post_convo.html', result=result)

@app.route('/stop', methods=['POST'])
def stop_task():
    task_id = request.form.get('taskId')
    if task_id in stop_events:
        stop_events[task_id].set()
        return f'Task with ID {task_id} has been stopped.'
    return f'No task found with ID {task_id}.'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)