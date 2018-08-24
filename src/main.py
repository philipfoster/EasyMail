from flask import Flask, request

app = Flask(__name__)


@app.route("/")
def test():
    return 'hello world'


@app.route("/sendmail", methods=['POST'])
def send_mail():
    name = request.form.get('name')
    from_addr = request.form.get('from')
    message = request.form.get('message')

    print("name = %s, from = %s, message = %s" % (name, from_addr, message))
    return ''


if __name__ == '__main__':
    app.run(debug=False, port=5000)
