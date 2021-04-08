from flask import Flask, render_template
from config.config_param import RDS_Chengdu_url as DBConfigURL
from flask_sqlalchemy import SQLAlchemy
import pymysql

pymysql.install_as_MySQLdb()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DBConfigURL()
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)


class Report(db.Model):
    __tablename__ = "report"
    ID = db.Column(db.Integer, primary_key=True)
    id_source = db.Column(db.String(11))
    id_school = db.Column(db.String(5))
    id_univ = db.Column(db.String(6))
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

    def __init__(self, ID, id_source, id_school, id_univ, date, year, topic, reporter_name, reporter_title,
                 reporter_school, host_name, host_title, host_school, inviter_name, inviter_title, inviter_school):
        self.ID = ID
        self.id_source = id_source
        self.id_school = id_school
        self.id_univ = id_univ
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


class University(db.Model):
    __tablename__ = "university"
    id = db.Column(db.Integer)
    univ_name = db.Column(db.String(255))
    description = db.Column(db.String(255))
    introduction = db.Column(db.String(255))
    location = db.Column(db.String(255))
    logo = db.Column(db.String(255))
    orig_name = db.Column(db.String(255), primary_key=True)

    def __init__(self, id, univ_name, description, introduction, location, logo, orig_name):
        self.id = id
        self.univ_name = univ_name
        self.description = description
        self.introduction = introduction
        self.location = location
        self.logo = logo
        self.orig_name = orig_name

    def __repr__(self):
        return '<University %r>' % self.id


@app.route('/')
def indexpage():
    return render_template('index.html')


@app.route('/list/')
@app.route('/list/<int:page>')
def listpage(page=1, PER_PAGE=10):
    # 默认渲染
    reports = Report.query.paginate(page, per_page=PER_PAGE)
    maxPage = len(Report.query.all()) // PER_PAGE
    start = max(1, page - 1)
    end = min(maxPage + 1, page + 2)
    return render_template('list.html', reports=reports, pageNum=page, maxPage=maxPage, start=start, end=end)

    # 条件渲染


@app.route('/info/<id>')
def infopage(id):
    # items = getinfo(id)
    items = []
    report = Report.query.filter_by(id_source=id).first_or_404()
    items.append(report)
    return render_template('info.html', items=items)

@app.route('/cluster/school/<id>')
@app.route('/cluster/school/<id>/<int:page>')
def schoolpage(id, page=1, PER_PAGE=10):
    university = University.query.filter_by(id=id).first_or_404()
    reports = Report.query.filter_by(id_univ=id).paginate(page, per_page=PER_PAGE)
    maxPage = len(Report.query.filter_by(id_univ=id).all()) // PER_PAGE
    start = max(1, page - 1)
    end = min(maxPage + 1, page + 2)
    return render_template('list_by_school.html', reports=reports, university=university,pageNum=int(page), maxPage=maxPage, start=start, end=end)


if __name__ == '__main__':
    app.run()
