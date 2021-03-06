import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import Flask, request, jsonify
from validate_email import validate_email

app = Flask(__name__)

config = {
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'useTls': True,
    'sendReceipt': True,
    'recipient': 'philip@pfoster.me',
    'password': os.environ.get('email_password'),
    'receipt-subject': 'Thanks for reaching out!',
    'receipt-body': 'Your message has been sent to Philip. He will respond shortly. \n\n\nYour message:\n %s'
}


#
# @app.route("/")
# def test():
#     return 'hello world'

class InvalidUsage(Exception):

    def __init__(self, message, status_code):
        Exception.__init__(self)
        self.message = message
        self.status_code = status_code

    def to_dict(self):
        rv = dict()
        rv['message'] = self.message
        rv['status_code'] = self.status_code
        return rv


@app.route("/sendmail", methods=['POST'])
def send_mail():
    name = request.form.get('name')
    from_addr = request.form.get('email')
    title = "Contact Me message from %s" % name
    #
    # if not verifyEmail(from_addr):
    #     raise InvalidUsage(message="Not a real email address", status_code=400)

    # Connect to SMTP server
    server = smtplib.SMTP(config['smtp_server'], config['smtp_port'])
    server.ehlo()

    # Setup STARTTLS if requested
    if config['useTls']:
        server.starttls()
        server.ehlo()

    # Authenticate with the server
    server.login(config['recipient'], config['password'])

    # Send the mail and a send receipt if desired.
    sendToMe(from_addr, config['recipient'], title, server)
    if config['sendReceipt']:
        sendReceipt(from_addr, request.form.get('message'), server)

    # Exit the session
    server.quit()

    return 'ok'


def sendToMe(from_addr, to_addr, subject, server_client):
    message = MIMEMultipart()
    message['From'] = from_addr
    message['To'] = to_addr
    message['Subject'] = subject
    message.add_header('reply-to', from_addr)
    body = MIMEText(request.form.get('message'), 'plain')
    message.attach(body)
    server_client.sendmail(from_addr, config['recipient'], message.as_string())


def sendReceipt(sender, msg, server_client):
    message = MIMEMultipart()
    message['From'] = config['recipient']
    message['To'] = sender
    message['Subject'] = config['receipt-subject']

    msg_text = config['receipt-body'] % msg

    body = MIMEText(msg_text, 'plain')
    message.attach(body)

    server_client.sendmail(config['recipient'], sender, message.as_string())
    pass


def verifyEmail(email):
    print(email)
    return validate_email(email, check_mx=True)


@app.errorhandler(InvalidUsage)
def handle_errors(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


if __name__ == '__main__':
    app.run(debug=False, port=5000, host='0.0.0.0')


