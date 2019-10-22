from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, TextAreaField, SelectField,SelectMultipleField
from wtforms.validators import DataRequired, ValidationError
from app.models import Admin, Tag,Auth

tags = Tag.query.all()

auths = Auth.query.all()

class LoginForm(FlaskForm):
    '''
    管理员登陆表单
    '''
    account = StringField(
        label='账号',
        validators=[
            DataRequired('请输入账号!')
        ],
        description='账号',
        render_kw={
            'class': "form-control",
            "placeholder": "请输入账号！",
            'required': 'required'
        }
    )
    pwd = PasswordField(
        label='密码',
        validators=[
            DataRequired('请输入密码!')
        ],
        description='密码',
        render_kw={
            'class': "form-control",
            "placeholder": "请输入密码！",
            'required': 'required'
        }
    )
    submit = SubmitField(
        '登陆',
        render_kw={
            'class': "btn btn-primary btn-block btn-flat"
        }
    )

    def validate_account(self, field):
        account = field.data
        count = Admin.query.filter_by(name=account).count()
        if count == 0:
            raise ValidationError('账号不存在')


class TagForm(FlaskForm):
    name = StringField(
        label='名称',
        validators=[
            DataRequired('请输入标签')
        ],
        description='标签',
        render_kw={
            'class': "form-control",
            'id': "input_name",
            "placeholder": "请输入标签名称！"
        }
    )
    submit = SubmitField(
        '添加',
        render_kw={
            'class': "btn btn-primary"
        }
    )


# 电影表单
class MovieForm(FlaskForm):
    title = StringField(
        label='标题',
        validators=[
            DataRequired('请输入电影名称!')
        ],
        description='片名',
        render_kw={
            'class': "form-control",
            'placeholder': "请输入片名！"
        }
    )
    url = FileField(
        label='文件',
        validators=[
            DataRequired('请上传文件')
        ],
        description='文件'
    )
    info = TextAreaField(
        label='电影简介',
        validators=[
            DataRequired('简介不能为空')
        ],
        description='简介',
        render_kw={
            'class': "form-control",
            'rows': "10",
        }
    )
    logo = FileField(
        label='封面',
        validators=[
            DataRequired('请上传封面')
        ],
        description='文件'
    )
    star = SelectField(
        label='星级',
        validators=[
            DataRequired('请选择星级')
        ],
        description='星级',
        render_kw={
            'class': "form-control",
        },
        coerce=int,
        choices=[(1, '1星'), (2, '2星'), (3, '3星'), (4, '4星'), (5, '5星')]
    )
    tag_id = SelectField(
        label='所属标签',
        validators=[
            DataRequired('请选择标签')
        ],
        description='标签',
        render_kw={
            'class': "form-control",
        },
        coerce=int,
        choices=[(v.id, v.name) for v in tags]
    )
    area = StringField(
        label='地区',
        validators=[
            DataRequired('请输入地区!')
        ],
        description='地区',
        render_kw={
            'class': "form-control",
            'placeholder': "请输入地区！"
        }
    )
    length = StringField(
        label='片长',
        validators=[
            DataRequired('请输入片长!')
        ],
        description='片长',
        render_kw={
            'class': "form-control",
            'placeholder': "请输入片长！"
        }
    )
    release_time = StringField(
        label='上映时间',
        validators=[
            DataRequired('请输入上映时间!')
        ],
        description='上映时间',
        render_kw={
            'class': "form-control",
            'placeholder': "请输入上映时间！",
            'id': "input_release_time"
        }
    )
    submit = SubmitField(
        '添加',
        render_kw={
            'class': "btn btn-primary"
        }
    )


# 预告管理
class PreviewForm(FlaskForm):
    title = StringField(
        label='标题',
        validators=[
            DataRequired('请输入电影名称!')
        ],
        description='标题',
        render_kw={
            'class': "form-control",
            'placeholder': "请输入预告标题！"
        }
    )
    logo = FileField(
        label='封面',
        validators=[
            DataRequired('请上传封面')
        ],
        description='文件'
    )
    submit = SubmitField(
        '添加',
        render_kw={
            'class': "btn btn-primary"
        }
    )


# 密码表单
class PwdForm(FlaskForm):
    old_pwd = StringField(
        label='旧密码',
        validators=[
            DataRequired('请输入旧密码!')
        ],
        description='旧密码',
        render_kw={
            'class': "form-control",
            'id': "input_pwd",
            'placeholder': "请输入旧密码！",
            'type' : "password"
        }
    )
    new_pwd = StringField(
        label='新密码',
        validators=[
            DataRequired('请输入新密码!')
        ],
        description='新密码',
        render_kw={
            'class': "form-control",
            'id': "input_pwd",
            'placeholder': "请输入新密码！",
            'type': "password"
        }
    )
    submit = SubmitField(
        '修改',
        render_kw={
            'class': "btn btn-primary"
        }
    )

#权限表单
class AuthForm(FlaskForm):
    name = StringField(
        label='权限名称',
        validators=[
            DataRequired('请输入权限名称!')
        ],
        description='权限名称',
        render_kw={
            'class': "form-control",
            'placeholder': "请输入权限名称！",
        }
    )
    url = StringField(
        label='权限地址',
        validators=[
            DataRequired('请输入权限地址!')
        ],
        description='权限地址',
        render_kw={
            'class': "form-control",
            'placeholder': "请输入权限地址！",
        }
    )
    submit = SubmitField(
        '添加',
        render_kw={
            'class': "btn btn-primary"
        }
    )

#角色表单
class RoleForm(FlaskForm):
    name = StringField(
        label='角色名称',
        validators=[
            DataRequired('请输入角色名称!')
        ],
        description='角色名称',
        render_kw={
            'class': "form-control",
            'placeholder': "请输入角色名称！",
        }
    )
    auths = SelectMultipleField(
        label='权限列表',
        validators=[
            DataRequired('请选择权限')
        ],
        description='权限列表',
        coerce=int,
        choices=[(v.id,v.name) for v in auths]
    )
    submit = SubmitField(
        '添加',
        render_kw={
            'class': "btn btn-primary"
        }
    )
