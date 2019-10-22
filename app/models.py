from datetime import datetime
from app import db



# 会员
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 会员名
    pwd = db.Column(db.String(100))  # 密码
    email = db.Column(db.String(100), unique=True)  # 邮箱
    phone = db.Column(db.String(11), unique=True)  # 电话
    info = db.Column(db.Text)  # 会员介绍
    face = db.Column(db.String(255), unique=True)  # 头像
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 注册时间
    uuid = db.Column(db.String(255), unique=True)  # 唯一标识符
    userlog = db.relationship('UserLog', backref='user')  # 日志外键关联
    comment = db.relationship('Comment', backref='user')  # 评论外键关联
    moviecol = db.relationship('Moviecol', backref='user')  # 收藏外键关联

    def __str__(self):
        return '<User %r>' % self.name

    def check_pwd(self,pwd):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.pwd,pwd)


# 会员登陆日志
class UserLog(db.Model):
    __tablename__ = 'userlog'
    id = db.Column(db.Integer, primary_key=True)  # 编号
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 关联会员
    ip = db.Column(db.String(100))  # 登陆IP
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 登陆时间

    def __str__(self):
        return '<UserLog %r>' % self.id


# 标签
class Tag(db.Model):
    __tablename__ = 'tag'
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 标题
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间
    movie = db.relationship('Movie', backref='tag')  # 电影外键关联

    def __str__(self):
        return "<Tag %r>" % self.name


# 电影
class Movie(db.Model):
    __tablename = 'movie'
    id = db.Column(db.Integer, primary_key=True)  # 编号
    title = db.Column(db.String(255), unique=True)  # 标题
    url = db.Column(db.String(255), unique=True)  # 地址
    info = db.Column(db.Text)  # 简介
    logo = db.Column(db.String(255), unique=True)  # 封面
    star = db.Column(db.SmallInteger)  # 星级
    playnum = db.Column(db.BigInteger)  # 播放量
    commentnum = db.Column(db.BigInteger)  # 评论量
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'))  # 所属标签
    area = db.Column(db.String(255))  # 上映地区
    release_time = db.Column(db.Date)  # 上映时间
    length = db.Column(db.String(100))  # 播放时间
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间
    comment = db.relationship('Comment', backref='movie')  # 评论外键关联
    moviecol = db.relationship('Moviecol', backref='movie')  # 收藏外键关联

    def __str__(self):
        return '<Movie %r>' % self.title


# 上映预告
class Preview(db.Model):
    __tablename__ = 'preview'
    id = db.Column(db.Integer, primary_key=True)  # 编号
    title = db.Column(db.String(255), unique=True)  # 标题
    logo = db.Column(db.String(255), unique=True)  # 封面
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间

    def __str__(self):
        return '<Preview> %r' % self.title


# 评论
class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)  # 编号
    content = db.Column(db.Text)  # 内容
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))  # 所属电影
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属用户
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间

    def __str__(self):
        return 'Comment %r' % self.id


# 电影收藏
class Moviecol(db.Model):
    __tablename__ = 'moviecol'
    id = db.Column(db.Integer, primary_key=True)  # 编号
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))  # 所属电影
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属用户
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间

    def __str__(self):
        return 'Comment %r' % self.id


# 权限
class Auth(db.Model):
    __tablename__ = 'auth'
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 名称
    url = db.Column(db.String(255), unique=True)  # 地址
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间

    def __str__(self):
        return '<Auth %r>' % self.name


# 角色
class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 名称
    auths = db.Column(db.String(600))
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间
    admin = db.relationship('Admin', backref='role')  # 管理员外键关系

    def __str__(self):
        return '<Role %r>' % self.name


# 管理员
class Admin(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 管理员账号
    pwd = db.Column(db.String(100))  # 密码
    is_super = db.Column(db.SmallInteger)  # 是否蔚超级管理员，0为超级管理员
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))  # 所属角色
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间
    adminlog = db.relationship('AdminLog', backref='admin')  # 登陆日志外键关联
    oplog = db.relationship('OpLog', backref='admin')  # 操作日志外键关联

    def check_pwd(self,pwd):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.pwd,pwd)

    def __str__(self):
        return '<Admin %r>' % self.id


# 管理员登陆日志
class AdminLog(db.Model):
    __tablename__ = 'adminlog'
    id = db.Column(db.Integer, primary_key=True)  # 编号
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))  # 所属管理员
    ip = db.Column(db.String(100))  # 登陆IP
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 登陆时间

    def __str__(self):
        return '<AdminLog %r>' % self.id


# 操作日志
class OpLog(db.Model):
    __tablename__ = 'oplog'
    id = db.Column(db.Integer, primary_key=True)  # 编号
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))  # 所属管理员
    ip = db.Column(db.String(100))  # 登陆IP
    reason = db.Column(db.String(600))  # 操作原因
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 登陆时间

    def __str__(self):
        return '<AdminLog %r>' % self.id

# if __name__ == '__main__':
#     #db.create_all()
#     # role = Role(
#     #     name='超级管理员',
#     #     auths=''
#     # )
#     # db.session.add(role)
#     # db.session.commit()
#     from werkzeug.security import generate_password_hash
#     admin = Admin(
#         name='admin',
#         pwd = generate_password_hash('admin'),
#         is_super = 0,
#         role_id = 1
#     )
#     db.session.add(admin)
#     db.session.commit()