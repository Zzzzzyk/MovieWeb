# coding:utf8
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,FileField,TextAreaField
from wtforms.validators import DataRequired, Email, Regexp, Length, ValidationError,EqualTo

from app.models import User,Comment
from flask import session

# 会员注册表单
class UserForm(FlaskForm):
    name = StringField(
        label='昵称',
        validators=[DataRequired('请输入用户名')],
        render_kw={
            'class': "form-control input-lg",
            'placeholder': "昵称"
        }
    )
    email = StringField(
        label='邮箱',
        validators=[
            DataRequired('请输入邮箱'),
            Email('邮箱格式不正确')
        ],
        render_kw={
            'class': "form-control input-lg",
            'placeholder': "邮箱"
        }
    )
    phone = StringField(
        label='手机',
        validators=[
            DataRequired('请输入手机号码'),
            Regexp('1[345678]\d{9}', message='手机号码格式不正确')
        ],
        render_kw={
            'class': "form-control input-lg",
            'placeholder': "手机号码"
        }
    )
    pwd = PasswordField(
        label='密码',
        validators=[
            DataRequired('请输入密码'),
            Length(8)
        ],
        render_kw={
            'class': "form-control input-lg",
            'placeholder': "密码(不少于8位)"
        }
    )
    repwd = PasswordField(
        label='确认密码',
        validators=[
            DataRequired('请再次输入密码'),
            Length(8),
            EqualTo('pwd',message='两次密码输入不一致')
        ],
        render_kw={
            'class': "form-control input-lg",
            'placeholder': "确认密码(不少于8位)"
        }
    )
    submit = SubmitField(
        '提交',
        render_kw={
            'class': 'btn btn-lg btn-success btn-block'
        }
    )


    def validate_name(self, field):
        name_co = User.query.filter_by(name=field.data).count()
        if name_co == 1:
            raise ValidationError('用户名已存在')

    def validate_email(self, field):
        email_co = User.query.filter_by(email=field.data).count()
        if email_co == 1:
            raise ValidationError('邮箱已被注册')

    def validate_phone(self, field):
        phone_co = User.query.filter_by(phone=field.data).count()
        if phone_co == 1:
            raise ValidationError('手机已被注册')

#会员登陆表单
class LoginForm(FlaskForm):
    name = StringField(
        label='账户',
        validators=[DataRequired('请输入用户名')],
        render_kw={
            'class': "form-control input-lg",
            'placeholder': "昵称/邮箱/手机号码"
        }
    )
    pwd = PasswordField(
        label='密码',
        validators=[
            DataRequired('请输入密码'),
            Length(8)
        ],
        render_kw={
            'class': "form-control input-lg",
            'placeholder': "密码(不少于8位)"
        }
    )
    submit = SubmitField(
        '提交',
        render_kw={
            'class': 'btn btn-lg btn-success btn-block'
        }
    )



#会员个人资料表单
class UserInfoForm(FlaskForm):
    name = StringField(
        label='昵称',
        validators=[DataRequired('请输入用户名')],
        render_kw={
            'class': "form-control input-lg",
            'placeholder': "昵称"
        }
    )
    email = StringField(
        label='邮箱',
        validators=[
            DataRequired('请输入邮箱'),
            Email('邮箱格式不正确')
        ],
        render_kw={
            'class': "form-control input-lg",
            'placeholder': "邮箱"
        }
    )
    phone = StringField(
        label='手机',
        validators=[
            DataRequired('请输入手机号码'),
            Regexp('1[345678]\d{9}', message='手机号码格式不正确')
        ],
        render_kw={
            'class': "form-control input-lg",
            'placeholder': "手机号码"
        }
    )
    face = FileField(
        label='用户头像',
        description=['用户头像'],
    )
    info = TextAreaField(
        label='用户简介',
        description='用户简介',
        render_kw={
            'class': "form-control",
            'rows': "10"
        }
    )
    submit = SubmitField(
        '保存修改',
        render_kw={
            'class': 'btn btn-success '
        }
    )

    def validate_name(self, field):
        name_co = User.query.filter_by(name=field.data).count()
        user = User.query.filter_by(id=session['user_id']).first()
        if name_co == 1 and user.name!=field.data:
            raise ValidationError('用户名已存在')

    def validate_email(self, field):
        email_co = User.query.filter_by(email=field.data).count()
        user = User.query.filter_by(id=session['user_id']).first()
        if email_co == 1 and user.email!=field.data:
            raise ValidationError('邮箱已被注册')

    def validate_phone(self, field):
        phone_co = User.query.filter_by(phone=field.data).count()
        user = User.query.filter_by(id=session['user_id']).first()
        if phone_co == 1 and user.phone!=field.data:
            raise ValidationError('手机已被注册')



#会员修改密码表单
class UserPwdForm(FlaskForm):
    old_pwd = PasswordField(
        label='旧密码',
        validators=[
            DataRequired('请输入旧密码'),
            Length(8)
        ],
        render_kw={
            'class': "form-control input-lg",
            'placeholder': "旧密码(不少于8位)"
        }
    )
    new_pwd = PasswordField(
        label='新密码',
        validators=[
            DataRequired('请输入新密码'),
            Length(8)
        ],
        render_kw={
            'class': "form-control input-lg",
            'placeholder': "新密码(不少于8位)"
        }
    )
    renew_pwd = PasswordField(
        label='确认新密码',
        validators=[
            DataRequired('请再次输入新密码'),
            Length(8),
            EqualTo('new_pwd',message='两次密码输入不一致')
        ],
        render_kw={
            'class': "form-control input-lg",
            'placeholder': "请再次输入新密码(不少于8位)"
        }
    )
    submit = SubmitField(
        '修改密码',
        render_kw={
            'class': ' btn btn-success '
        }
    )
#电影评论表单
class CommentForm(FlaskForm):
    content = TextAreaField(
        label='内容',
        validators=[DataRequired("请输入评论")],
        description='内容',
        render_kw={
            'id':'input_content',
        }
    )
    submit = SubmitField(
        '提交评论',
        render_kw={
            'class': ' btn btn-success '
        }
    )