from flask import Flask,render_template

app = Flask(__name__)


@app.route('/')
def indexpage():
    return render_template('index.html')

@app.route('/list/')
def listpage():
    return render_template('list.html')

@app.route('/info/')
def infopage():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
