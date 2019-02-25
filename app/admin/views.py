# coding;utf8

import datetime
import os
import uuid
from functools import wraps

from flask import render_template, redirect, url_for, flash, session, request,abort
from werkzeug.utils import secure_filename

from app import db, app
from app.admin import admin
from app.admin.forms import LoginForm, TagForm, MovieForm, PreviewForm, PwdForm, AuthForm,RoleForm,AdminForm
from app.models import Admin, Tag, Movie, Preview, User, Comment, Moviecol, Auth,Role


# 用户登陆状态检查--装饰器
def admin_login_require(f):
    @wraps(f)
    def inner_func(*args, **kwargs):
        if 'account' not in session:
            return redirect(url_for('admin.login', next=request.url))
        return f(*args, **kwargs)

    return inner_func



#权限限制--装饰器
def admin_auth(f):
    @wraps(f)
    def inner_func(*args,**kwargs):
        admin = Admin.query.join(Role).filter(Admin.name==session['account']).filter(Role.id==Admin.role_id,).first()
        authlist = Auth.query.all()
        auths = admin.role.auths
        auth = []
        if auths:
            auth = map(lambda i:int(i),auths.split(','))
        urls = ['/admin'+j.url for i in auth for j in authlist if i==j.id]
        print(urls)
        url = request.url_rule
        print(url)
        if admin.is_super and str(url) not in urls:
            abort(404,'No Permission!')
        return f(*args,**kwargs)
    return inner_func






# 更改文件文件名称
def change_filename(filename):
    filename_old = os.path.splitext(filename)
    filename = datetime.datetime.now().strftime('%Y%m%d%H%M%S') + str(uuid.uuid4().hex) + filename_old[-1]
    return filename


# 用户登录界面
@admin.route('/login', methods=['POST', 'GET'])
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


@admin.route('/logout')
def logout():
    session.pop('account', None)
    return redirect(url_for('admin.login'))


@admin.route('/')
@admin_login_require
def index():
    return render_template('admin/index.html')


# 标签列表
@admin.route('/tag/list/<int:page>/', methods=['GET'])
@admin_login_require
@admin_auth
def tag_list(page=1):
    page_data = Tag.query.order_by(Tag.id.asc()).paginate(page=page, per_page=10)
    return render_template('admin/tag_list.html', page_data=page_data)


# 添加标签
@admin.route('/tag/add', methods=['GET', 'POST'])
@admin_login_require
@admin_auth
def tag_add():
    form = TagForm()
    if form.validate_on_submit():
        data = form.data
        tag = Tag.query.filter_by(name=data['name']).count()
        if tag == 1:
            flash('操作失败', 'err')
            return redirect(url_for('admin.tag_add'))
        tag = Tag(name=data['name'])
        db.session.add(tag)
        db.session.commit()
        flash('操作成功', 'ok')
        return redirect(url_for('admin.tag_add'))
    return render_template('admin/tag_add.html', form=form)


# 修改标签
@admin.route('/tag/edit/<int:id>', methods=['GET', 'POST'])
@admin_login_require
@admin_auth
def tag_edit(id):
    form = TagForm()
    tag = Tag.query.get_or_404(id)
    if form.validate_on_submit():
        data = form.data
        tag_co = Tag.query.filter_by(name=data['name']).count()
        if tag.name != data['name'] and tag_co == 1:
            flash('标签已存在', 'err')
            return redirect(url_for('admin.tag_edit', id=id))
        tag.name = data['name']
        db.session.add(tag)
        db.session.commit()
        flash('操作成功', 'ok')
        return redirect(url_for('admin.tag_list', page=1))
    return render_template('admin/tag_edit.html', form=form, tag=tag)


# 删除标签
@admin.route('/tag/del/<int:id>', methods=['GET'])
@admin_login_require
@admin_auth
def tag_del(id):
    tag = Tag.query.filter_by(id=id).first_or_404()
    db.session.delete(tag)
    db.session.commit()
    flash('标签删除成功', 'ok')
    return redirect(url_for('admin.tag_list', page=1))


# 电影列表
@admin.route('/movie/list/<int:page>/', methods=['GET'])
@admin_login_require
@admin_auth
def movie_list(page=1):
    page_data = Movie.query.join(Tag).filter(Movie.tag_id == Tag.id).order_by(Movie.id.desc()).paginate(page=page,
                                                                                                             per_page=10)
    return render_template('admin/movie_list.html', page_data=page_data)


# 删除电影
@admin.route('/movie/del/<int:id>', methods=['GET'])
@admin_login_require
@admin_auth
def movie_del(id):
    tag = Movie.query.filter_by(id=id).first_or_404()
    db.session.delete(tag)
    db.session.commit()
    flash('电影删除成功', 'ok')
    return redirect(url_for('admin.movie_list', page=1))


# 添加电影
@admin.route('/movie/add/', methods=['GET', 'POST'])
@admin_login_require
@admin_auth
def movie_add():
    form = MovieForm()
    if request.method == 'POST':
        data = form.data
        if not os.path.exists(app.config['UP_DIR']):
            os.makedirs(app.config['UP_DIR'], mode=0o777)
        file_url = secure_filename(form.moviefile.data.filename)
        file_logo = secure_filename(form.logo.data.filename)
        movieurl = change_filename(file_url)
        movielogo = change_filename(file_logo)
        form.moviefile.data.save(app.config['UP_DIR'] + movieurl)
        form.logo.data.save(app.config['UP_DIR'] + movielogo)
        movie = Movie(
            title=data['title'],
            url=movieurl,
            info=data['info'],
            logo=movielogo,
            star=data['star'],
            tag_id=data['tag'],
            area=data['area'],
            release_time=data['release_time'],
            length=data['length'],
            playnum=0,
            commentnum=0,
        )
        db.session.add(movie)
        db.session.commit()
        flash('电影添加成功', 'ok')
        return redirect(url_for('admin.movie_add'))
    return render_template('admin/movie_add.html', form=form)


# 修改电影
@admin.route('/movie/edit/<int:id>/', methods=['GET', 'POST'])
@admin_login_require
@admin_auth
def movie_edit(id):
    form = MovieForm()
    form.moviefile.validators = False
    form.logo.validators = False
    movie = Movie.query.get_or_404(id)
    if request.method == 'GET':
        form.info.data = movie.info

    if request.method == 'POST':
        data = form.data
        if not os.path.exists(app.config['UP_DIR']):
            os.makedirs(app.config['UP_DIR'], mode=0o777)
        if form.moviefile.data:
            file_url = secure_filename(form.moviefile.data.filename)
            movieurl = change_filename(file_url)
            form.moviefile.data.save(app.config['UP_DIR'] + movieurl)
            movie.url = movieurl
        if form.logo.data:
            file_logo = secure_filename(form.logo.data.filename)
            movielogo = change_filename(file_logo)
            form.logo.data.save(app.config['UP_DIR'] + movielogo)
            movie.logo = movielogo
        movie.title = data['title']
        movie.info = data['info']
        movie.star = data['star']
        movie.tag_id = data['tag']
        movie.area = data['area']
        movie.release_time = data['release_time']
        movie.length = data['length']
        db.session.add(movie)
        db.session.commit()
        flash('电影修改成功', 'ok')
        return redirect(url_for('admin.movie_list', page=1))
    return render_template('admin/movie_edit.html', form=form, movie=movie)


# 预告列表
@admin.route('/preview/list/<int:page>/', methods=['GET'])
@admin_login_require
@admin_auth
def preview_list(page=1):
    pagedata = Preview.query.order_by(Preview.addtime.desc()).paginate(page=page, per_page=10)
    return render_template('admin/preview_list.html', pagedata=pagedata)


# 添加预告
@admin.route('/preview/add', methods=['GET', 'POST'])
@admin_login_require
@admin_auth
def preview_add():
    form = PreviewForm()
    if request.method == 'POST':
        data = form.data
        if not os.path.exists(app.config['UP_DIR']):
            os.makedirs(app.config['UP_DIR'], mode=0o777)
        file_logo = secure_filename(form.logo.data.filename)
        previewlogo = change_filename(file_logo)
        form.logo.data.save(app.config['UP_DIR'] + previewlogo)
        preview = Preview(
            title=data['title'],
            logo=previewlogo,
        )
        db.session.add(preview)
        db.session.commit()
        flash('预告添加成功！', 'ok')
        return redirect(url_for('admin.preview_add'))
    return render_template('admin/preview_add.html', form=form)


# 修改预告
@admin.route('/preview/edit/<int:id>/', methods=['GET', 'POST'])
@admin_login_require
@admin_auth
def preview_edit(id):
    form = PreviewForm()
    form.title.validators = []
    form.logo.validators = []
    preview = Preview.query.get_or_404(id)
    if request.method == 'POST':
        data = form.data
        if not os.path.exists(app.config['UP_DIR']):
            os.makedirs(app.config['UP_DIR'], mode=0o777)
        if form.logo.data:
            file_logo = secure_filename(form.logo.data.filename)
            previewlogo = change_filename(file_logo)
            form.logo.data.save(app.config['UP_DIR'] + previewlogo)
            preview.logo = previewlogo
        preview.title = data['title']
        db.session.add(preview)
        db.session.commit()
        flash('预告修改成功！', 'ok')
        return redirect(url_for('admin.preview_edit', id=id))
    return render_template('admin/preview_edit.html', form=form, preview=preview)


# 删除预告
@admin.route('/preview/del/<int:id>/', methods=['GET'])
@admin_login_require
@admin_auth
def preview_del(id):
    preview = Preview.query.get_or_404(id)
    db.session.delete(preview)
    db.session.commit()
    flash('预告删除成功！', 'ok')
    return redirect(url_for('admin.preview_list', page=1))


# 用户列表
@admin.route('/user/list/<int:page>/', methods=['GET'])
@admin_login_require
@admin_auth
def user_list(page=1):
    pagedata = User.query.order_by(User.addtime.desc()).paginate(page=page, per_page=10)
    return render_template('admin/user_list.html', pagedata=pagedata)


# 用户信息页
@admin_login_require
@admin.route('/user/view/<int:id>', methods=['GET'])
@admin_auth
def user_view(id):
    user = User.query.get_or_404(id)
    return render_template('admin/user_view.html', user=user)


# 删除用户
@admin_login_require
@admin.route('/user/del/<int:id>')
@admin_auth
def user_del(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    flash('用户删除成功', 'ok')
    return redirect(url_for('admin.user_list', page=1))


# 评论管理
@admin.route('/comment/list/<int:page>/', methods=['GET'])
@admin_login_require
@admin_auth
def comment_list(page=1):
    pagedata = Comment.query.join(Movie).join(User).filter(
        Comment.movie_id == Movie.id,
        Comment.user_id == User.id
    ).order_by(Comment.addtime.desc()).paginate(page=page, per_page=10)
    return render_template('admin/comment_list.html', pagedata=pagedata)


# 删除评论
@admin_login_require
@admin.route('/comment/del/<int:id>')
@admin_auth
def comment_del(id):
    comment = Comment.query.get_or_404(id)
    db.session.delete(comment)
    db.session.commit()
    flash('评论删除成功', 'ok')
    return redirect(url_for('admin.comment_list', page=1))


# 收藏管理
@admin.route('/moviecol/list/<int:page>/', methods=['GET'])
@admin_login_require
@admin_auth
def moviecol_list(page=1):
    pagedata = Moviecol.query.join(Movie).join(User).filter(
        Moviecol.movie_id == Movie.id,
        Moviecol.user_id == User.id
    ).order_by(Moviecol.addtime.desc()).paginate(page=page, per_page=10)
    return render_template('admin/moviecol_list.html', pagedata=pagedata)


# 删除收藏
@admin.route('/moviecol/del/<int:id>')
@admin_login_require
@admin_auth
def moviecol_del(id):
    moviecol = Moviecol.query.get_or_404(id)
    db.session.delete(moviecol)
    db.session.commit()
    flash('收藏删除成功', 'ok')
    return redirect(url_for('admin.moviecol_list', page=1))


# 修改密码
@admin.route('/pwd', methods=['GET', 'POST'])
@admin_login_require
@admin_auth
def pwd():
    form = PwdForm()
    if request.method == 'POST':
        data = form.data
        admin = Admin.query.filter_by(name=session['account']).first()
        if not admin.check_pwd(data['old_pwd']):
            flash('原密码错误！', 'ok')
            return redirect(url_for('admin.pwd'))
        from werkzeug.security import generate_password_hash
        admin.pwd = generate_password_hash(data['new_pwd'])
        db.session.add(admin)
        db.session.commit()
        flash('修改密码成功', 'ok')
        return redirect(url_for('admin.logout'))
    return render_template('admin/pwd.html', form=form)


@admin.route('/admin/oplog_list')
@admin_login_require
@admin_auth
def oplog_list():
    return render_template('admin/oplog_list.html')


@admin.route('/admin/adminloginlog_list')
@admin_login_require
@admin_auth
def adminloginlog_list():
    return render_template('admin/adminloginlog_list.html')


@admin.route('/admin/userloginlog_list')
@admin_login_require
@admin_auth
def userloginlog_list():
    return render_template('admin/userloginlog_list.html')


# 添加权限
@admin.route('/auth/add', methods=['GET', 'POST'])
@admin_login_require
@admin_auth
def auth_add():
    form = AuthForm()
    if form.validate_on_submit():
        data = form.data
        auth = Auth(
            name=data['name'],
            url=data['url']
        )
        db.session.add(auth)
        db.session.commit()
        flash('权限添加成功!', 'ok')
        return redirect(url_for('admin.auth_add'))
    return render_template('admin/auth_add.html', form=form)


# 修改权限
@admin.route('/auth/edit/<int:id>', methods=['GET', 'POST'])
@admin_login_require
@admin_auth
def auth_edit(id):
    form = AuthForm()
    form.name.validators = []
    form.url.validators = []
    auth = Auth.query.get_or_404(id)
    if form.validate_on_submit():
        data = form.data
        auth_co = Auth.query.filter_by(name=data['name']).count()
        if auth.name != data['name'] and auth_co == 1:
            flash('权限名称已存在', 'err')
            return redirect(url_for('admin.auth_edit',id=id))
        auth.name = data['name']
        auth.url = data['url']
        db.session.add(auth)
        db.session.commit()
        flash('权限修改成功!', 'ok')
        return redirect(url_for('admin.auth_edit',id=id))
    return render_template('admin/auth_edit.html', form=form, auth=auth)


# 权限列表
@admin.route('/auth/list/<int:page>', methods=['GET'])
@admin_login_require
@admin_auth
def auth_list(page=1):
    pagedata = Auth.query.order_by(Auth.addtime.desc()).paginate(page=page, per_page=10)
    return render_template('admin/auth_list.html', pagedata=pagedata)


# 删除权限
@admin.route('/auth/del/<int:id>', methods=['GET'])
@admin_login_require
@admin_auth
def auth_del(id):
    auth = Auth.query.get_or_404(id)
    db.session.delete(auth)
    db.session.commit()
    flash('权限删除成功', 'ok')
    return redirect(url_for('admin.auth_list', page=1))

#添加角色
@admin.route('/role/add',methods=['GET','POST'])
@admin_login_require
@admin_auth
def role_add():
    form = RoleForm()
    if form.validate_on_submit():
        data = form.data
        role_co = Role.query.filter_by(name=data['name']).count()
        if role_co == 1:
            flash('角色已存在','err')
            return redirect(url_for('admin.role_add'))
        role = Role(
            name = data['name'],
            auths = ','.join(map(lambda v :str(v),data['auths'])),
        )
        db.session.add(role)
        db.session.commit()
        flash('角色添加成功！','ok')
        return redirect(url_for('admin.role_add'))
    return render_template('admin/role_add.html',form=form)

#角色列表
@admin.route('/role/list/<int:page>',methods=['GET'])
@admin_login_require
@admin_auth
def role_list(page=1):
    pagedata = Role.query.order_by(Role.addtime.desc()).paginate(page=page,per_page=10)
    return render_template('admin/role_list.html',pagedata=pagedata)


#删除角色
@admin.route('/role/del/<int:id>',methods=['GET'])
@admin_login_require
@admin_auth
def role_del(id):
    role = Role.query.get_or_404(id)
    db.session.delete(role)
    db.session.commit()
    flash('角色删除成功','ok')
    return redirect(url_for('admin.role_list',page=1))



#修改角色
@admin.route('/role/edit/<int:id>',methods=['GET','POST'])
@admin_login_require
@admin_auth
def role_edit(id):
    form = RoleForm()
    role = Role.query.get_or_404(id)
    if role.auths:
        form.auths.data = map(lambda v:int(v),(role.auths.split(',')))
    if form.validate_on_submit():
        data = form.data
        role_co = Role.query.filter_by(name=data['name']).count()
        if role_co == 1 and role.name!=data['name']:
            flash('角色已存在','err')
            return redirect(url_for('admin.role_edit',id=id))
        role.name = data['name']
        role.auths = ','.join(map(lambda v :str(v),data['auths']))
        db.session.add(role)
        db.session.commit()
        flash('角色修改成功！','ok')
        return redirect(url_for('admin.role_edit',id=id))
    return render_template('admin/role_edit.html',form=form,role=role)




@admin.route('/admin/add',methods=['GET','POST'])
@admin_login_require
@admin_auth
def admin_add():
    form = AdminForm()
    if form.validate_on_submit():
        from werkzeug.security import generate_password_hash
        data = form.data
        admin = Admin(
            name = data['name'],
            pwd = generate_password_hash(data['pwd']),
            role_id = data['role_id'],
            is_super = 1
        )
        db.session.add(admin)
        db.session.commit()
        flash('管理员添加成功','ok')
        return redirect(url_for('admin.admin_add'))
    return render_template('admin/admin_add.html',form=form)


@admin.route('/admin/list/<int:page>',methods=['GET'])
@admin_login_require
@admin_auth
def admin_list(page=1):
    pagedata = Admin.query.order_by(Admin.addtime.desc()).paginate(page=page,per_page=10)
    return render_template('admin/admin_list.html',pagedata=pagedata)
