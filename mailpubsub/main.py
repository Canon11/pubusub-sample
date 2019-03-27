from flask import Flask, render_template, request, redirect, url_for
from pubsub_utils import push_to_topic, pull_from_subscriber

import json

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/mail/push', methods=['POST'])
def mail_push():
    push_data = {
        'email': request.form['email'],
        'message': request.form['message']
    }
    push_msg = json.dumps(push_data)

    # json形式でメッセージをPub/SubにPush
    push_to_topic(push_msg)

    return redirect(url_for('index'))


@app.route('/mail/pull')
def mail_pull():
    def pub_callback(msg):
        data = json.loads(msg.data)
        print('email: %s' % data['email'])
        print('msg: %s' % data['message'])
        msg.ack()

    # Pub/Subからメッセージを引っ張ってきて、コールバック
    pull_from_subscriber(pub_callback)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
