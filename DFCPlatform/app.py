from flask import Flask,render_template
from listpage import item, get_list
from infopage import item, getinfo
app = Flask(__name__)


@app.route('/')
def indexpage():
    return render_template('index.html')

@app.route('/list/')
def listpage():
    # 默认渲染
    items = get_list()
    return render_template('list.html',items = items)

    # 条件渲染

@app.route('/info/<id>')
def infopage(id):
    items = getinfo(id)
    return render_template('info.html',items=items)


if __name__ == '__main__':
    app.run()
