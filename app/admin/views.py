from . import admin
from flask import render_template, redirect, request, session, flash, url_for
from app.admin.forms import LoginForm, TagForm, MovieForm, PreviewForm, PwdForm, AuthForm, RoleForm
from app.models import Admin, Tag, Movie, Preview, User, Comment, Moviecol, OpLog, AdminLog, UserLog, Auth, Role
from functools import wraps
from app import db, app
import os, uuid, datetime
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash


# 登陆校验装饰器
def decoration(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if 'account' not in session:
            return redirect(url_for('admin.login', next=request.url))
        return func(*args, **kwargs)

    return inner


# 修改文件名
def change_file(filename):
    fileinfo = os.path.splitext(filename)
    filename = datetime.datetime.now().strftime('%Y%m%d%H%M%S') + str(uuid.uuid4().hex) + fileinfo[-1]
    return filename


# 后台首页
@admin.route('/')
@decoration
def index():
    return render_template('admin/index.html')


# 后台登陆
@admin.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
        admin = Admin.query.filter_by(name=data['account']).first()
        if not admin.check_pwd(data['pwd']):
            flash('密码错误')
            return redirect(url_for('admin.login'))
        session['account'] = data['account']
        return redirect(request.args.get('next') or url_for('admin.index'))
    return render_template('admin/login.html', form=form)


# 后台退出
@admin.route('/logout/')
@decoration
def logout():
    session.pop('account', None)
    return redirect(url_for('admin.login'))


# 修改密码
@admin.route('/pwd/', methods=['GET', 'POST'])
@decoration
def pwd():
    form = PwdForm()
    if form.validate_on_submit():
        data = form.data
        admin = Admin.query.filter_by(name=session['account']).first_or_404()
        if not admin.check_pwd(data['old_pwd']):
            flash('旧密码错误,请重新输入!')
            return redirect(url_for('admin.pwd'))
        new_pwd = generate_password_hash(data['new_pwd'])
        admin.pwd = new_pwd
        db.session.add(admin)
        db.session.commit()
        flash('修改密码成功')
        return redirect(url_for('admin.pwd'))
    return render_template('admin/pwd.html', form=form)


# 添加标签
@admin.route('/tag/add/', methods=['GET', 'POST'])
@decoration
def tag_add():
    form = TagForm()
    if form.validate_on_submit():
        data = form.data
        tag_num = Tag.query.filter_by(name=data['name']).count()
        if tag_num == 1:
            flash('标签已存在')
            return redirect(url_for('admin.tag_add'))
        tag = Tag(name=data['name'])
        db.session.add(tag)
        db.session.commit()
        flash('添加标签成功')
        return redirect(url_for('admin.tag_add'))
    return render_template('admin/tag_add.html', form=form)


# 修改 标签
@admin.route('/tag/edit/<int:id>', methods=['GET', 'POST'])
@decoration
def tag_edit(id):
    form = TagForm()
    tag = Tag.query.get_or_404(id)
    if form.validate_on_submit():
        data = form.data
        tag_num = Tag.query.filter_by(name=data['name']).count()
        if tag.name != data['name'] and tag_num == 1:
            flash('标签已存在')
            return redirect(url_for('admin.tag_edit', id=id))
        tag.name = data['name']
        db.session.add(tag)
        db.session.commit()
        flash('修改标签成功')
        return redirect(url_for('admin.tag_edit', id=id))
    return render_template('admin/tag_edit.html', form=form, tag=tag)


# 标签列表
@admin.route('/tag/list/<int:page>', methods=['GET'])
@decoration
def tag_list(page=None):
    if page is None:
        page = 1
    page_data = Tag.query.order_by(
        Tag.add_time.desc()
    ).paginate(page=page, per_page=10)
    return render_template('admin/tag_list.html', page_data=page_data)


# 删除标签
@admin.route('/tag/del/<int:id>', methods=['GET'])
@decoration
def tag_del(id):
    tag = Tag.query.filter_by(id=id).first_or_404()
    db.session.delete(tag)
    db.session.commit()
    flash('删除标签成功')
    return redirect(url_for('admin.tag_list', page=1))


# 添加电影
@admin.route('/movie/add/', methods=['GET', 'POST'])
@decoration
def movie_add():
    form = MovieForm()
    if form.validate_on_submit():
        data = form.data
        url = form.url.data.filename
        logo = secure_filename(form.logo.data.filename)
        if not os.path.exists(app.config['UP_DIR']):
            os.mkdir(app.config['UP_DIR'])
            os.chmod(app.config['UP_DIR'], 'rw')
        file_url = change_file(url)
        file_logo = change_file(logo)
        form.url.data.save(app.config['UP_DIR'] + file_url)
        form.logo.data.save(app.config['UP_DIR'] + file_logo)
        movie = Movie(
            title=data['title'],
            url=file_url,
            info=data['info'],
            logo=file_logo,
            star=int(data['star']),
            tag_id=data['tag_id'],
            playnum=0,
            commentnum=0,
            area=data['area'],
            release_time=data['release_time'],
            length=data['length']
        )
        db.session.add(movie)
        db.session.commit()
        flash('添加电影成功')
        return redirect(url_for('admin.movie_add'))
    return render_template('admin/movie_add.html', form=form)


# 删除电影
@admin.route('/movie/del/<int:id>', methods=['GET'])
@decoration
def movie_del(id):
    movie = Movie.query.filter_by(id=id).first_or_404()
    db.session.delete(movie)
    db.session.commit()
    flash('删除电影成功')
    return redirect(url_for('admin.movie_list', page=1))


# 电影列表
@admin.route('/movie/list/<int:page>', methods=['GET'])
@decoration
def movie_list(page=None):
    if page is None:
        page = 1
    page_data = Movie.query.order_by(
        'add_time'
    ).paginate(page=page, per_page=10)
    return render_template('admin/movie_list.html', page_data=page_data)


# 添加上映预告
@admin.route('/preview/add/', methods=['GET', 'POST'])
@decoration
def preview_add():
    form = PreviewForm()
    if form.validate_on_submit():
        data = form.data
        logo = secure_filename(form.logo.data.filename)
        if not os.path.exists(app.config['UP_DIR']):
            os.mkdir(app.config['UP_DIR'])
            os.chmod(app.config['UP_DIR'], 'rw')
        file_logo = change_file(logo)
        form.logo.data.save(app.config['UP_DIR'] + file_logo)
        preview = Preview(
            title=data['title'],
            logo=file_logo
        )
        db.session.add(preview)
        db.session.commit()
        flash('添加上映预告成功')
        return redirect(url_for('admin.preview_add'))
    return render_template('admin/preview_add.html', form=form)


# 上映预告列表
@admin.route('/preview/list/<int:page>', methods=['GET'])
@decoration
def preview_list(page=None):
    if page is None:
        page = 1
    page_data = Preview.query.order_by('add_time').paginate(page=page, per_page=10)
    return render_template('admin/preview_list.html', page_data=page_data)


# 删除上映预告
@admin.route('/preview/del/<int:id>', methods=['GET'])
@decoration
def preview_del(id):
    preview = Preview.query.filter_by(id=id).first_or_404()
    db.session.delete(preview)
    db.session.commit()
    flash('删除上映预告成功')
    return redirect(url_for('admin.preview_list', page=1))


# 编辑上映预告
@admin.route('/preview/edit/<int:id>', methods=['GET', 'POST'])
@decoration
def preview_edit(id):
    form = PreviewForm()
    preview = Preview.query.get_or_404(id)
    if form.validate_on_submit():
        data = form.data
        logo = form.logo.data.filename
        if not os.path.exists(app.config['UP_DIR']):
            os.mkdir(app.config['UP_DIR'])
            os.chmod(app.config['UP_DIR'], 'rw')
        file_logo = change_file(logo)
        form.logo.data.save(app.config['UP_DIR'] + file_logo)
        preview.title = data['title']
        preview.logo = file_logo
        db.session.add(preview)
        db.session.commit()
        flash('修改上映预告成功')
        return redirect(url_for('admin.preview_edit', id=preview.id))
    return render_template('admin/preview_edit.html', form=form, preview=preview)


# 会员列表
@admin.route('/user/list/<int:page>', methods=['GET'])
@decoration
def user_list(page=None):
    if page is None:
        page = 1
    page_data = User.query.order_by('add_time').paginate(page=page, per_page=10)
    return render_template('admin/user_list.html', page_data=page_data)


# 查看会员
@admin.route('/user/view/<int:id>', methods=['GET'])
@decoration
def user_view(id):
    user = User.query.get_or_404(int(id))
    return render_template('admin/user_view.html', user=user)


# 删除会员
@admin.route('/user/del/<int:id>', methods=['GET'])
@decoration
def user_del(id):
    user = User.query.get_or_404(int(id))
    db.session.delete(user)
    db.session.commit()
    flash('删除会员成功')
    return redirect(url_for('admin.user_list', page=1))


# 评论列表
@admin.route('/comment/list/<int:page>', methods=['GET'])
@decoration
def comment_list(page=None):
    if page is None:
        page = 1
    page_data = Comment.query.join(Movie).join(User).filter(
        User.id == Comment.user_id, Movie.id == Comment.movie_id
    ).order_by('add_time').paginate(page=page, per_page=10)
    return render_template('admin/comment_list.html', page_data=page_data)


# 删除评论
@admin.route('/comment/del/<int:id>', methods=['GET'])
@decoration
def comment_del(id):
    comment = Comment.query.get_or_404(int(id))
    db.session.delete(comment)
    db.session.commit()
    flash('删除评论成功')
    return redirect(url_for('admin.comment_list', page=1))


# 收藏列表
@admin.route('/moviecol/list/<int:page>', methods=['GET'])
@decoration
def moviecol_list(page=None):
    if page is None:
        page = 1
    page_data = Moviecol.query.join(Movie).join(User).filter(
        User.id == Moviecol.user_id, Movie.id == Moviecol.movie_id
    ).order_by('add_time').paginate(page=page, per_page=10)
    return render_template('admin/moviecol_list.html', page_data=page_data)


# 删除收藏列表
@admin.route('/moviecol/del/<int:id>', methods=['GET'])
@decoration
def moviecol_del(id):
    moviecol = Moviecol.query.get_or_404(int(id))
    db.session.delete(moviecol)
    db.session.commit()
    flash('删除收藏成功')
    return redirect(url_for('admin.moviecol_list', page=1))


# 操作日志列表
@admin.route('/oplog/list/<int:page>', methods=['GET'])
@decoration
def oplog_list(page=None):
    if page is None:
        page = 1
    page_data = OpLog.query.join(Admin).filter(
        Admin.id == OpLog.admin_id
    ).order_by('add_time').paginate(page=page, per_page=10)
    return render_template('admin/oplog_list.html', page_data=page_data)


# 管理员登录日志列表
@admin.route('/adminloginlog/list/<int:page>', methods=['GET'])
@decoration
def adminloginlog_list(page=None):
    if page is None:
        page = 1
    page_data = AdminLog.query.join(Admin).filter(
        Admin.id == AdminLog.admin_id
    ).order_by('add_time').paginate(page=page, per_page=10)
    return render_template('admin/adminloginlog_list.html', page_data=page_data)


# 会员登录日志列表
@admin.route('/userloginlog/list/<int:page>', methods=['GET'])
@decoration
def userloginlog_list(page=None):
    if page is None:
        page = 1
    page_data = UserLog.query.join(User).filter(
        User.id == UserLog.user_id
    ).order_by('add_time').paginate(page=page, per_page=10)
    return render_template('admin/userloginlog_list.html', page_data=page_data)


# 添加权限
@admin.route('/auth/add/', methods=['GET', 'POST'])
@decoration
def auth_add():
    form = AuthForm()
    if form.validate_on_submit():
        data = form.data
        auth = Auth(name=data['name'], url=data['url'])
        db.session.add(auth)
        db.session.commit()
        flash('添加权限成功')
        return redirect(url_for('admin.auth_add'))
    return render_template('admin/auth_add.html', form=form)


# 权限列表
@admin.route('/auth/list/<int:page>', methods=['GET'])
@decoration
def auth_list(page=None):
    if page is None:
        page = 1
    page_data = Auth.query.order_by(
        Auth.add_time.desc()
    ).paginate(page=page, per_page=10)
    return render_template('admin/auth_list.html', page_data=page_data)


# 删除权限
@admin.route('/auth/del/<int:id>', methods=['GET'])
@decoration
def auth_del(id):
    auth = Auth.query.filter_by(id=id).first_or_404()
    db.session.delete(auth)
    db.session.commit()
    flash('删除权限成功')
    return redirect(url_for('admin.auth_list', page=1))


# 编辑权限
@admin.route('/auth/edit/<int:id>', methods=['GET', 'POST'])
@decoration
def auth_edit(id):
    auth = Auth.query.filter_by(id=id).first_or_404()
    form = AuthForm()
    if form.validate_on_submit():
        data = form.data
        auth.name = data['name']
        auth.url = data['url']
        db.session.add(auth)
        db.session.commit()
        flash('修改权限成功')
        return redirect(url_for('admin.auth_edit', id=id))
    return render_template('admin/auth_edit.html', auth=auth, form=form)


# 添加角色
@admin.route('/role/add/', methods=['GET', 'POST'])
@decoration
def role_add():
    form = RoleForm()
    if form.validate_on_submit():
        data = form.data
        role = Role(name=data['name'], auths=",".join(map(lambda v: str(v), data['auths'])))
        db.session.add(role)
        db.session.commit()
        flash('添加角色成功')
        return redirect(url_for('admin.role_add'))
    return render_template('admin/role_add.html', form=form)


# 角色列表
@admin.route('/role/list/<int:page>', methods=['GET'])
@decoration
def role_list(page=None):
    if page is None:
        page = 1
    page_data = Role.query.order_by(
        Role.add_time.desc()
    ).paginate(page=page, per_page=10)
    return render_template('admin/role_list.html', page_data=page_data)


# 删除角色
@admin.route('/role/del/<int:id>', methods=['GET'])
@decoration
def role_del(id):
    role = Role.query.get_or_404(int(id))
    db.session.delete(role)
    db.session.commit()
    flash('删除角色成功')
    return redirect(url_for('admin.role_list', page=1))


# 编辑角色
@admin.route('/role/edit/<int:id>', methods=['GET', 'POST'])
@decoration
def role_edit(id):
    role = Role.query.get_or_404(int(id))
    form = RoleForm()
    if request.method == 'GET':
        auths = role.auths
        form.auths.data = list(map(lambda v: int(v), auths.split(',')))
    if form.validate_on_submit():
        data = form.data
        role.name = data['name']
        role.auths = ",".join(map(lambda v: str(v), data['auths']))
        db.session.add(role)
        db.session.commit()
        flash('修改角色成功')
        return redirect(url_for('admin.role_edit', id=id))
    return render_template('admin/role_edit.html', role=role, form=form)


# 添加管理员
@admin.route('/admin/add/')
@decoration
def admin_add():
    return render_template('admin/admin_add.html')


# 管理员列表
@admin.route('/admin/list/')
@decoration
def admin_list():
    return render_template('admin/admin_list.html')
