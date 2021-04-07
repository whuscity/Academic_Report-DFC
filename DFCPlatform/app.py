from flask import Flask,render_template
from config.config_param import RDS_Chengdu_url as DBConfigURL
from flask_sqlalchemy import SQLAlchemy
import pymysql
pymysql.install_as_MySQLdb()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DBConfigURL()
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)

class Report(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    id_source = db.Column(db.String(11))
    id_school = db.Column(db.String(5))
    date = db.Column(db.String(30))
    year = db.Column(db.String(5))
    topic = db.Column(db.String(255))
    reporter_name = db.Column(db.String(50))
    reporter_title = db.Column(db.String(50))
    reporter_school = db.Column(db.String(180))
    host_name = db.Column(db.String(50))
    host_title = db.Column(db.String(50))
    host_school = db.Column(db.String(180))
    inviter_name = db.Column(db.String(50))
    inviter_title = db.Column(db.String(50))
    inviter_school = db.Column(db.String(180))

    def __init__(self, ID, id_source, id_school, date, year, topic, reporter_name, reporter_title, reporter_school, host_name, host_title, host_school, inviter_name, inviter_title, inviter_school):
        self.ID = ID
        self.id_source = id_source
        self.id_school = id_school
        self.date = date
        self.year = year
        self.topic = topic
        self.reporter_name = reporter_name
        self.reporter_title = reporter_title
        self.reporter_school = reporter_school
        self.host_name = host_name
        self.host_title = host_title
        self.host_school = host_school
        self.inviter_name = inviter_name
        self.inviter_title = inviter_title
        self.inviter_school = inviter_school

    def __repr__(self):
        return '<Report %r>' % self.ID


@app.route('/')
def indexpage():
    return render_template('index.html')

@app.route('/list/')
def listpage():
    # 默认渲染
    items = Report.query.limit(10).all()
    return render_template('list.html',items = items)

    # 条件渲染

@app.route('/info/<id>')
def infopage(id):
    # items = getinfo(id)
    items = []
    report = Report.query.filter_by(id_source=id).first_or_404()
    items.append(report)
    return render_template('info.html',items=items)


if __name__ == '__main__':
    app.run()
