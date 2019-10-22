from . import home
from flask import render_template, redirect, url_for, flash, session, request
from app.models import User, UserLog,Tag,Movie,Preview,Comment,Moviecol
from app.home.forms import RegisterForm, LoginForm, UserDetailForm, PwdForm,CommentForm
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
import uuid, os
from datetime import datetime
from app import db, app
from functools import wraps


# 登陆校验装饰器
def decoration(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('home.login', next=request.url))
        return func(*args, **kwargs)

    return inner


# 更改上次文件名称
def change_file_name(filename):
    name = os.path.splitext(filename)
    file_name = datetime.now().strftime('%Y%m%d%H%M%S') + uuid.uuid4().hex + name[-1]
    return file_name


# 微电影首页
@home.route('/<int:page>/',methods=['GET'])
def index(page=None):
    tag = Tag.query.all()
    tag_id = request.args.get('tid',0)
    star = request.args.get('star',0)
    time = request.args.get('time',0)
    play_num = request.args.get('pm',0)
    comment_num = request.args.get('cm',0)
    page_data = Movie.query
    if int(tag_id) !=0:
        page_data = page_data.filter_by(tag_id=int(tag_id))
    if int(star) !=0:
        page_data = page_data.filter_by(star=int(star))
    if int(time) !=0:
        if time == 1:
            page_data = page_data.order_by(Movie.add_time.desc())
        else:
            page_data = page_data.order_by(Movie.add_time.asc())
    if int(play_num) !=0:
        if play_num == 1:
            page_data = page_data.order_by(Movie.playnum.desc())
        else:
            page_data = page_data.order_by(Movie.playnum.asc())
    if int(comment_num) != 0:
        if comment_num == 1:
            page_data = page_data.order_by(Movie.commentnum.desc())
        else:
            page_data = page_data.order_by(Movie.commentnum.asc())
    if page is None:
        page = 1
    page_data = page_data.paginate(page=page, per_page=10)
    p = dict(
        tag_id=tag_id,
        star=star,
        time=time,
        play_num=play_num,
        comment_num=comment_num
    )
    return render_template('home/index.html',tag=tag,p=p,page_data=page_data,page=page)


# 登陆
@home.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
        user = User.query.filter_by(name=data['account'])
        user_count = user.count()
        if user_count == 0:
            flash('当前用户不存在')
            return redirect(url_for('home.login'))
        if not user.first().check_pwd(data['pwd']):
            flash('账户密码不正确')
            return redirect(url_for('home.login'))
        session['user'] = data['account']
        session['user_id'] = user.first().id
        usr_log = UserLog(
            user_id=int(user.first().id),
            ip=request.remote_addr
        )
        db.session.add(usr_log)
        db.session.commit()
        return redirect(request.args.get('next') or url_for('home.index',page=1))
    return render_template('home/login.html', form=form)


# 退出
@home.route('/logout/')
@decoration
def logout():
    session.pop('user', None)
    session.pop('user_id', None)
    return redirect(url_for('home.login'))


# 注册
@home.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        data = form.data
        if data['pwd'] != data['confirm_pwd']:
            flash('两次密码输入不一致')
            return redirect(url_for('home.register'))
        user = User(
            name=data['name'],
            pwd=generate_password_hash(data['pwd']),
            email=data['email'],
            phone=data['phone'],
            uuid=uuid.uuid4().hex
        )
        db.session.add(user)
        db.session.commit()
        flash('注册会员成功')
        return redirect(url_for('home.login'))
    return render_template('home/register.html', form=form)


# 会员中心
@home.route('/user/', methods=['GET', 'POST'])
def user():
    if 'user' not in session:
        return redirect(url_for('home.index',page=1))
    form = UserDetailForm()
    user = User.query.filter_by(name=session['user']).first()
    if form.validate_on_submit():
        data = form.data
        face_name = secure_filename(form.face.data.filename)
        face = change_file_name(face_name)
        form.face.validators = []
        if request.method == 'GET':
            form.info.data = user.info
        if not os.path.exists(app.config['UP_DIR']):
            os.mkdir(app.config['UP_DIR'])
            os.chmod(app.config['UP_DIR'], 'rw')
        form.face.data.save(app.config['UP_DIR'] + face)
        user.name = data['name']
        user.email = data['email']
        user.phone = data['phone']
        user.info = data['info']
        user.face = face
        db.session.add(user)
        db.session.commit()
        flash('修改会员资料成功')
        session['user'] = data['name']
        return redirect(url_for('home.user'))
    return render_template('home/user.html', form=form, user=user)


# 修改密码
@home.route('/pwd/', methods=['GET', 'POST'])
def pwd():
    form = PwdForm()
    if form.validate_on_submit():
        data = form.data
        user = User.query.filter_by(name=session['user']).first_or_404()
        if not user.check_pwd(data['old_pwd']):
            flash('旧密码错误,请重新输入!')
            return redirect(url_for('home.pwd'))
        new_pwd = generate_password_hash(data['new_pwd'])
        user.pwd = new_pwd
        db.session.add(user)
        db.session.commit()
        flash('修改密码成功')
        return redirect(url_for('home.login'))
    return render_template('home/pwd.html', form=form)


# 评论记录
@home.route('/comments/')
def comments():
    return render_template('home/comments.html')


# 登陆日志
@home.route('/loginlog/', methods=['GET'])
def loginlog(page=None):
    if page is None:
        page = 1
    page_data = UserLog.query.filter_by(
        user_id=int(session['user_id'])
    ).paginate(page=page, per_page=10)
    return render_template('home/loginlog.html', page_data=page_data)


# 收藏电影
@home.route('/moviecol/<int:page>/',methods=['GET'])
def moviecol(page=None):
    if page is None:
        page = 1
    page_data = Moviecol.query.join(Movie).join(User).filter(
        Moviecol.movie_id == Movie.id,
        Moviecol.user_id == session['user_id']
    ).paginate(page=page, per_page=10)
    return render_template('home/moviecol.html',page_data=page_data)


# 动画
@home.route('/animation/',methods=['GET'])
def animation():
    preview = Preview.query.all()
    return render_template('home/animation.html',preview=preview)


# 搜索
@home.route('/search/<int:page>',methods=['GET'])
def search(page=None):
    if page is None:
        page = 1
    name = request.args.get('name')
    page_data = Movie.query.filter(
        Movie.title.ilike('%'+name+'%')
    ).paginate(page=page, per_page=10)
    return render_template('home/search.html',page_data=page_data)


# 播放详情页
@home.route('/play/<int:id>/<int:page>/',methods=['GET','POST'])
def play(id,page=None):
    if page is None:
        page = 1
    page_data = Comment.query.join(User).join(Movie).filter(
        Comment.movie_id == id,
        Comment.user_id == User.id
    ).order_by(Comment.add_time.desc()).paginate(page=page, per_page=10)
    movie = Movie.query.join(Tag).filter(
        Movie.tag_id == Tag.id,
        Movie.id == id
    ).first()
    form = CommentForm()
    movie.playnum = movie.playnum + 1
    if 'user' in session and form.validate_on_submit():
        data = form.data
        comment = Comment(
            content=data['content'],
            movie_id=movie.id,
            user_id=session['user_id']
        )
        db.session.add(comment)
        db.session.commit()
        movie.commentnum = movie.commentnum + 1
        db.session.add(movie)
        db.session.commit()
        flash('添加评论内容成功')
        return redirect(url_for('home.play',id=id,page=1))
    db.session.add(movie)
    db.session.commit()
    col_id = request.args.get('col',None)
    if col_id:
        col_count = Moviecol.query.filter(
            Moviecol.user_id == session['user_id'],
            Moviecol.movie_id == int(col_id)
        ).count()
        if col_count != 0:
            flash('该电影已收藏!')
            return redirect(url_for('home.play',id=col_id,page=1))
        moviecol = Moviecol(
            movie_id=col_id,
            user_id=session['user_id']
        )
        db.session.add(moviecol)
        db.session.commit()
        flash('添加电影收藏成功')
        return redirect(url_for('home.play',id=col_id,page=1))
    return render_template('home/play.html',movie=movie,form=form,page_data=page_data)
