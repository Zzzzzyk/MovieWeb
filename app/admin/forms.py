# coding:utf8
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, TextAreaField, SelectField,SelectMultipleField
from wtforms.validators import DataRequired, ValidationError,EqualTo

from app.models import Admin,Tag,Auth,Role

tags = Tag.query.all()
auths = Auth.query.all()
roles = Role.query.all()

# 管理员登录表单
class LoginForm(FlaskForm):
    '''管理员登陆表单'''
    account = StringField(
        label='账号',
        validators=[DataRequired('请输入账号')],
        description='账号',
        render_kw={
            'class': "form-control",
            'placeholder': "请输入账号！",
            'required': 'required',
        }

    )
    pwd = PasswordField(
        label='密码',
        validators=[DataRequired('请输入密码')],
        description='密码',
        render_kw={
            'class': "form-control",
            'placeholder': "请输入密码！",
            'required': 'required',
        }
    )
    submit = SubmitField(
        '登陆',
        render_kw={
            'class': "btn btn-primary btn-block btn-flat",
        }
    )

    def validate_account(self, field):
        account = field.data
        admin = Admin.query.filter_by(name=account).count()
        if admin == 0:
            raise ValidationError('账号不存在')


# 标签表单
class TagForm(FlaskForm):
    name = StringField(
        label='标签名称',
        validators=[DataRequired('请输入标签')],
        description='标签',
        render_kw={
            "class": "form-control",
            'placeholder': "请输入标签名称！",
        }
    )
    submit = SubmitField(
        '提交',
        render_kw={
            'class': "btn btn-primary",
        }
    )


# 电影表单
class MovieForm(FlaskForm):
    title = StringField(
        label='片名',
        validators=[DataRequired('请输入片名')],
        description='片名',
        render_kw={
            'class': "form-control",
            'id': "input_title",
            'placeholder': "请输入片名！"
        }
    )
    moviefile = FileField(
        label='电影文件',
        validators=[DataRequired('请上传电影')],
        description='电影文件',
    )
    info = TextAreaField(
        label='电影简介',
        description='电影简介',
        render_kw={
            'class': "form-control",
            'rows': "10",
            'id': "input_info"
        }
    )
    logo = FileField(
        label='电影封面',
        validators=[DataRequired('请上传电影封面')],
    )
    star = SelectField(
        label='星级',
        validators=[DataRequired('请选择星级')],
        coerce=int,
        choices=((1, '1星'), (2, '2星'), (3, '3星'), (4, '4星'), (5, '5星'),),
        render_kw={
            'class': 'form-control',
        }
    )
    tag = SelectField(
        label='标签',
        validators=[DataRequired('请选择标签')],
        choices=[(v.id, v.name) for v in tags],
        render_kw={
            'class': 'form-control',
        }
    )
    area = StringField(
        label='上映地区',
        render_kw={
            'class': 'form-control',
            'type': "text",
            ' id': "input_area",
            'placeholder': "请输入地区！"
        }
    )
    length = StringField(
        label='片长',
        render_kw={
            'class': 'form-control',
            'type': "text",
            ' id': "input_length",
            'placeholder': "请输入片长！"
        }
    )
    release_time = StringField(
        label='上映时间',
        render_kw={
            'class': 'form-control',
            'type': "text",
            ' id': "input_release_time",
            'placeholder': "请输入上映时间！"
        }
    )
    submit = SubmitField(
        'Submit',
        render_kw={
            'class': "btn btn-primary",
        }
    )


# 电影预告
class PreviewForm(FlaskForm):
    title = StringField(
        label='预告标题',
        validators=[DataRequired('请添加预告标题')],
        render_kw={
            'class': "form-control",
            'id': "input_title",
            'placeholder': "请输入预告标题！"
        }
    )
    logo = FileField(
        label='预告图片',
        validators=[DataRequired('请添加预告图片')],
        description='预告图片',
    )
    submit = SubmitField(
        '提交',
        render_kw={
            'class':"btn btn-primary"
        }
    )


#更改密码
class PwdForm(FlaskForm):
    old_pwd = PasswordField(
        label='原密码',
        validators=[DataRequired('请输入原密码')],
        description='原密码',
        render_kw={
            'class': "form-control",
            'placeholder': "请输入原密码！",
            'required': 'required',
        }
    )
    new_pwd = PasswordField(
        label='新密码',
        validators=[DataRequired('请输入新密码')],
        description='新密码',
        render_kw={
            'class': "form-control",
            'placeholder': "请输入新密码！",
            'required': 'required',
        }
    )
    submit = SubmitField(
        '提交',
        render_kw={
            'class': "btn btn-primary btn-block btn-flat",
        }
    )
    def validate_old_pwd(self,field):
        pwd = field.data
        from flask import session
        name = session['admin']
        admin = Admin.query.filter_by(name=name).first()
        if not admin.check_pwd(pwd):
            return ValidationError('原密码错误！')


#权限管理
class AuthForm(FlaskForm):
    name = StringField(
        label='权限名称',
        validators=[DataRequired('请输入权限')],
        description='权限',
        render_kw={
            "class": "form-control",
            'placeholder': "请输入权限名称！",
        }
    )
    url = StringField(
        label='权限路径',
        validators=[DataRequired('请输入权限路径')],
        description='权限路径',
        render_kw={
            "class": "form-control",
            'placeholder': "请输入权限路径！",
        }
    )
    submit = SubmitField(
        '提交',
        render_kw={
            'class': "btn btn-primary",
        }
    )


#角色管理
class RoleForm(FlaskForm):
    name = StringField(
        label='角色名称',
        validators=[DataRequired('请输入角色名称')],
        description='角色名称',
        render_kw={
            "class": "form-control",
            'placeholder': "请输入角色名称！",
        }
    )
    auths = SelectMultipleField(
        label='权限列表',
        description='权限列表',
        coerce=int,
        choices=[(v.id,v.name) for v in auths],
        render_kw={
            'class':'form-control',
        }
    )
    submit = SubmitField(
        '提交',
        render_kw={
            'class': "btn btn-primary",
        }
    )


#管理员注册表
class AdminForm(FlaskForm):
    name = StringField(
        label='管理员名称',
        validators=[DataRequired('请输入管理员名称')],
        description='管理员名称',
        render_kw={
            "class": "form-control",
            'placeholder': "请输入管理员名称！",
        }
    )
    pwd = PasswordField(
        label='管理员密码',
        validators=[DataRequired('请输入管理员密码')],
        description='管理员密码',
        render_kw={
            'class': "form-control",
            'placeholder': "请输入管理员密码！",
            'required': 'required',
        }
    )
    repwd = PasswordField(
        label='管理员重复密码',
        validators=[DataRequired('请输入管理员重复密码'),
                    EqualTo('pwd',message='两次输入的密码不一致')],
        description='管理员重复密码',
        render_kw={
            'class': "form-control",
            'placeholder': "请再次输入管理员密码！",
            'required': 'required',
        }
    )
    role_id = SelectField(
        label='所属角色',
        validators=[DataRequired('请选择所属角色')],
        coerce=int,
        choices=[(v.id,v.name) for v in roles],
        render_kw={
            'class': "form-control",
        }
    )
    submit = SubmitField(
        '提交',
        render_kw={
            'class': "btn btn-primary",
        }
    )
