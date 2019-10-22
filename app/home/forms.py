from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,FileField,TextAreaField,SubmitField
from wtforms.validators import DataRequired,ValidationError


#会员注册表单
class RegisterForm(FlaskForm):
    name = StringField(
        label='昵称',
        validators=[
            DataRequired('请填写昵称!')
        ],
        description='昵称',
        render_kw={
            'class' :"form-control input-lg",
            'placeholder':"昵称"
        }
    )
    pwd = PasswordField(
        label='密码',
        validators=[
            DataRequired('请填写密码')
        ],
        description='密码',
        render_kw={
            'class': "form-control input-lg",
            'placeholder': "密码"
        }
    )
    email = StringField(
        label='邮箱',
        validators=[
            DataRequired('请填写邮箱')
        ],
        description='邮箱',
        render_kw={
            'class': "form-control input-lg",
            'placeholder': "邮箱"
        }
    )
    phone = StringField(
        label='电话',
        validators=[
            DataRequired('请填写电话')
        ],
        description='电话',
        render_kw={
            'class': "form-control input-lg",
            'placeholder': "电话"
        }
    )
    confirm_pwd = PasswordField(
        label='确认密码',
        validators=[
            DataRequired('请填写确认密码')
        ],
        description='确认密码',
        render_kw={
            'class': "form-control input-lg",
            'placeholder': "确认密码"
        }
    )
    submit = SubmitField(
        '注册',
        render_kw={
            'class' :"btn btn-lg btn-success btn-block"
        }
    )

#会员登陆表单
class LoginForm(FlaskForm):
    account = StringField(
        label='用户名',
        validators=[
            DataRequired('请填写用户名')
        ],
        description='用户名',
        render_kw={
            'class': "form-control input-lg",
            'placeholder': "用户名"
        }
    )
    pwd = PasswordField(
        label='密码',
        validators=[
            DataRequired('请填写密码')
        ],
        description='密码',
        render_kw={
            'class': "form-control input-lg",
            'placeholder': "密码"
        }
    )
    submit = SubmitField(
        '登陆',
        render_kw={
            'class': "btn btn-lg btn-success btn-block"
        }
    )

#会员详情表单
class UserDetailForm(FlaskForm):
    name = StringField(
        label='昵称',
        validators=[
            DataRequired('请填写昵称')
        ],
        description='昵称',
        render_kw={
            'class': "form-control input-lg",
            'placeholder': "昵称"
        }
    )
    email = StringField(
        label='邮箱',
        validators=[
            DataRequired('请填写邮箱')
        ],
        description='邮箱',
        render_kw={
            'class': "form-control input-lg",
            'placeholder': "邮箱"
        }
    )
    phone = StringField(
        label='手机',
        validators=[
            DataRequired('请填写手机')
        ],
        description='手机',
        render_kw={
            'class': "form-control input-lg",
            'placeholder': "手机"
        }
    )
    face = FileField(
        label='头像',
        validators=[
            DataRequired('请上传头像')
        ],
        description='头像'
    )
    info = TextAreaField(
        label='简介',
        description='简介',
        render_kw={
            'class' :"form-control",
            'rows':"10"
        }
    )
    submit = SubmitField(
        '保存修改',
        render_kw={
            'class':"glyphicon glyphicon-saved"
        }
    )

# 密码表单
class PwdForm(FlaskForm):
    old_pwd = PasswordField(
        label='旧密码',
        validators=[
            DataRequired('请输入旧密码!')
        ],
        description='旧密码',
        render_kw={
            'class': "form-control",
            'id': "input_pwd",
            'placeholder': "请输入旧密码！",
        }
    )
    new_pwd = PasswordField(
        label='新密码',
        validators=[
            DataRequired('请输入新密码!')
        ],
        description='新密码',
        render_kw={
            'class': "form-control",
            'id': "input_pwd",
            'placeholder': "请输入新密码！",
        }
    )
    submit = SubmitField(
        '修改密码',
        render_kw={
            'class': "btn btn-primary"
        }
    )

class CommentForm(FlaskForm):
    content = TextAreaField(
        label='评论内容',
        description='评论内容',
        validators=[
            DataRequired('请输入评论内容')
        ],
        render_kw={
            'id':'input_content'
        }
    )
    submit = SubmitField(
        '提交评论',
        render_kw={
            'class':"btn btn-success",
            'id':"btn-sub"
        }
    )


