from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy
import pymysql
import os
app = Flask(__name__)
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:sy123456@192.168.101.20:3306/movie'
app.config['SQLALCHEMY_TRACH_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'cxc2^^%%sasas'
app.config['UP_DIR'] = os.path.join(os.path.abspath(os.path.dirname(__file__)),'static/upload/')
db = SQLAlchemy(app)

from app.admin import admin  as admin_blueprint
from app.home import home as home_blueprint
app.register_blueprint(admin_blueprint, url_prefix='/admin')
app.register_blueprint(home_blueprint)

#自定义错误页面
@app.errorhandler(404)
def page_not_found(e):
    return render_template('home/404.html'),404