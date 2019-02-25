# coding=utf8
import datetime
import os
import uuid
from functools import wraps

from flask import render_template, redirect, url_for, session, flash, request, Response
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename

from app import db, app, redis_store
from app.home import home
from app.home.forms import UserForm, LoginForm, UserInfoForm, UserPwdForm, CommentForm
from app.models import User, Userlog, Preview, Tag, Movie, Comment, Moviecol


# 用户登陆状态检查--装饰器
def user_login_require(f):
    @wraps(f)
    def inner_func(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('home.login', next=request.url))
        return f(*args, **kwargs)

    return inner_func


# 404处理
@app.errorhandler(404)
def page_not_found(error):
    return render_template('home/404.html', error=error)


# 默认网站主页
@home.route('/', methods=['GET', 'POST'])
def index():
    page = 1
    tags = Tag.query.all()
    page_data = Movie.query
    tagid = int(request.args.get('tagid', 0))
    if tagid != 0:
        page_data = page_data.filter_by(tag_id=tagid)
    star = int(request.args.get('star', 0))
    if star != 0:
        page_data = page_data.filter_by(star=star)
    time = int(request.args.get('time', 0))
    if time != 0:
        if int(time) == 1:
            page_data = page_data.order_by(Movie.addtime.desc())
        if int(time) == 2:
            page_data = page_data.order_by(Movie.addtime.asc())
        cn = request.args.get('cn', 0)
    pn = int(request.args.get('pn', 0))
    if pn != 0:
        if int(pn) == 1:
            page_data = page_data.order_by(Movie.playnum.desc())
        if int(pn) == 2:
            page_data = page_data.order_by(Movie.playnum.asc())
    cn = int(request.args.get('cn', 0))
    if cn != 0:
        if int(cn) == 1:
            page_data = page_data.order_by(Movie.commentnum.desc())
        if int(cn) == 2:
            page_data = page_data.order_by(Movie.commentnum.asc())
    pagedata = page_data.paginate(page=page, per_page=20)
    p = dict(
        tagid=tagid,
        star=star,
        time=time,
        pn=pn,
        cn=cn
    )
    return render_template('home/index.html', tags=tags, p=p, pagedata=pagedata)


# 适配标签筛选的网站主页
@home.route('/<int:page>/', methods=['GET', 'POST'])
def reindex(page=1):
    tags = Tag.query.all()
    page_data = Movie.query
    tagid = int(request.args.get('tagid', 0))
    if tagid != 0:
        page_data = page_data.filter_by(tag_id=tagid)
    star = int(request.args.get('star', 0))
    if star != 0:
        page_data = page_data.filter_by(star=star)
    time = int(request.args.get('time', 0))
    if time != 0:
        if int(time) == 1:
            page_data = page_data.order_by(Movie.addtime.desc())
        if int(time) == 2:
            page_data = page_data.order_by(Movie.addtime.asc())
        cn = request.args.get('cn', 0)
    pn = int(request.args.get('pn', 0))
    if pn != 0:
        if int(pn) == 1:
            page_data = page_data.order_by(Movie.playnum.desc())
        if int(pn) == 2:
            page_data = page_data.order_by(Movie.playnum.asc())
    cn = int(request.args.get('cn', 0))
    if cn != 0:
        if int(cn) == 1:
            page_data = page_data.order_by(Movie.commentnum.desc())
        if int(cn) == 2:
            page_data = page_data.order_by(Movie.commentnum.asc())
    pagedata = page_data.paginate(page=page, per_page=20)
    p = dict(
        tagid=tagid,
        star=star,
        time=time,
        pn=pn,
        cn=cn
    )
    return render_template('home/index.html', tags=tags, p=p, pagedata=pagedata)


# 会员登陆
@home.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
        user_co = 0
        if User.query.filter_by(name=data['name']).count():
            user = User.query.filter_by(name=data['name']).first()
            user_co = 1
        elif User.query.filter_by(email=data['name']).count():
            user = User.query.filter_by(email=data['name']).first()
            user_co = 1
        elif User.query.filter_by(phone=data['name']).count():
            user = User.query.filter_by(phone=data['name'])
            user_co = 1
        if not user_co or not user.check_pwd(data['pwd']):
            flash('登录失败', 'err')
            return redirect(url_for('home.login'))
        session['user'] = user.name
        session['user_id'] = user.id
        # flash('用户登陆成功', 'ok')
        userlog = Userlog(
            user_id=user.id,
            ip=request.remote_addr
        )
        db.session.add(userlog)
        db.session.commit()
        return redirect(url_for('home.index'))
    return render_template('home/login.html', form=form)


# 会员退出登陆
@home.route('/logout', methods=['GET'])
def logout():
    session.pop('user', None)
    session.pop('user_id', None)
    return redirect(url_for('home.login'))


# 会员注册
@home.route('/register', methods=['GET', 'POST'])
def register():
    form = UserForm()
    if form.validate_on_submit():
        data = form.data
        user = User(
            name=data['name'],
            email=data['email'],
            phone=data['phone'],
            pwd=generate_password_hash(data['pwd'])
        )
        db.session.add(user)
        db.session.commit()
        flash('用户注册成功', 'ok')
        session['user'] = user.name
        return redirect(url_for('home.index'))
    return render_template('home/register.html', form=form)


# 会员中心
@home.route('/user', methods=['GET', 'POST'])
@user_login_require
def user():
    form = UserInfoForm()
    user = User.query.filter_by(id=session['user_id']).first()
    if request.method == 'GET':
        form.info.data = user.info
    if request.method == 'POST':
        if form.validate_on_submit():
            data = form.data
            if not os.path.exists(app.config['UP_DIR'] + 'userface/'):
                os.makedirs(app.config['UP_DIR' + 'userface/'], mode=0o777)
            print(form.face)
            print(form.face.data)
            print(type(form.face.data))
            if form.face.data:
                print(form.face.data)
                print(type(form.face.data))
                face_url = secure_filename(form.face.data.filename)
                print(face_url)
                print(type(face_url))
                user.face = face_url
                form.face.data.save(app.config['UP_DIR'] + 'userface/' + face_url)
            user.name = data['name']
            user.email = data['email']
            user.phone = data['phone']
            user.info = data['info']
            db.session.add(user)
            db.session.commit()
            flash('个人资料更新成功！', 'ok')
            return redirect(url_for('home.user'))
        else:
            flash('个人资料修改失败！', 'err')
    return render_template('home/user.html', form=form, user=user)


# 会员修改密码
@home.route('/pwd', methods=['GET', 'POST'])
@user_login_require
def pwd():
    form = UserPwdForm()
    if form.validate_on_submit():
        data = form.data
        user = User.query.filter_by(id=session['user_id']).first()
        if not user.check_pwd(data['old_pwd']):
            flash('密码修改失败', 'err')
            return redirect(url_for('home.pwd'))
        user.pwd = generate_password_hash(data['new_pwd'])
        db.session.add(user)
        db.session.commit()
        flash('密码修改成功，请重新登陆', 'ok')
        session.pop('user')
        session.pop('user_id')
        return redirect(url_for('home.relogin'))
    return render_template('home/pwd.html', form=form)


# 修改密码后跳转界面
@home.route('/relogin', methods=['GET'])
def relogin():
    return render_template('home/relogin.html')


# 会员评论记录
@home.route('/comments/<int:page>')
@user_login_require
def comments(page):
    pagedata = Comment.query.filter_by(user_id=session['user_id']).order_by(Comment.addtime.desc()).join(User).filter(
        Comment.user_id == User.id
    ).paginate(page=page, per_page=10)
    return render_template('home/comments.html', pagedata=pagedata)


# 会员登陆记录
@home.route('/loginlog/<int:page>', methods=['GET'])
@user_login_require
def loginlog(page=1):
    pagedata = Userlog.query.order_by(Userlog.addtime.desc()).paginate(page=page, per_page=10)
    return render_template('home/loginlog.html', pagedata=pagedata)


# 会员收藏记录
@home.route('/moviecol/<int:page>', methods=['GET'])
@user_login_require
def moviecol(page):
    pagedata = Moviecol.query.filter_by(user_id=session['user_id']).join(Movie).filter(
        Moviecol.movie_id == Movie.id
    ).order_by(Moviecol.addtime.desc()).paginate(page=page, per_page=10)
    return render_template('home/moviecol.html', pagedata=pagedata)


# 会员增加电影收藏
@home.route('/moviecol_add', methods=['GET'])
@user_login_require
def moviecol_add():
    movie_id = int(request.args.get('mid'))
    user_id = int(request.args.get('uid'))
    moviecol_co = Moviecol.query.filter_by(
        movie_id=movie_id,
        user_id=user_id
    ).count()
    import json
    if moviecol_co == 0:
        moviecollection = Moviecol(
            movie_id=movie_id,
            user_id=user_id
        )
        db.session.add(moviecollection)
        db.session.commit()
        return json.dumps(dict(ok=1))
    else:
        return json.dumps(dict(ok=0))


@home.route('/animation')
def animation():
    data = Preview.query.all()
    return render_template('home/animation.html', data=data)


# 搜索功能
@home.route('/search/<int:page>')
def search(page=1):
    search_key = request.args.get('key', '')
    pagedata = Movie.query.filter(
        Movie.title.ilike("%" + search_key + "%")
    ).order_by(Movie.addtime.desc()).paginate(page=page, per_page=10)
    search_co = Movie.query.filter(
        Movie.title.ilike("%" + search_key + "%")
    ).count()
    return render_template('home/search.html', pagedata=pagedata, search_key=search_key, search_co=search_co)


# 电影播放和评论收藏功能
@home.route('/play/<int:id>/<int:page>', methods=['GET', 'POST'])
@user_login_require
def play(id, page=1):
    form = CommentForm()
    movie = Movie.query.filter_by(id=id).join(Tag).filter(
        Movie.tag_id == Tag.id
    ).first_or_404()
    movie.playnum += 1
    db.session.add(movie)
    db.session.commit()
    comment_co = Comment.query.filter_by(movie_id=id).count()
    comment_list = Comment.query.filter_by(movie_id=id).join(User).filter(
        Comment.user_id == User.id
    ).order_by(Comment.addtime.desc()).paginate(page=page, per_page=8)
    if form.validate_on_submit():
        data = form.content.data
        comment = Comment(
            content=data,
            movie_id=id,
            user_id=session['user_id']
        )
        movie.commentnum += 1
        db.session.add(comment)
        db.session.add(movie)
        db.session.commit()
        flash('评论成功', 'ok')
        return redirect(url_for('home.play', id=movie.id, page=1))
    return render_template('home/danmaku.html', comment_co=comment_co, movie=movie, form=form,
                           comment_list=comment_list)


@home.route('/danmaku/v3/', methods=['GET', 'POST'])
def danmaku():
    import json
    if request.method == 'GET':
        id = request.args.get('id')
        key = 'movie' + str(id)
        if redis_store.llen(key):
            msgs = redis_store.lrange(key, 0, 999)
            print(msgs)
            res = {
                'code': 1,
                "danmaku": [json.loads(v) for v in msgs]
            }
        else:
            res = {
                'code': 1,
                "danmaku": []
            }
        resp = json.dumps(res)
    if request.method == 'POST':
        data = json.loads(request.get_data())
        print(data)
        msg = {
            "id": data['id'],
            "author": data['author'],
            "time": data['time'],
            "text": data['text'],
            "color": data['color'],
            "type": data['type'],
            "ip": request.remote_addr,
            "mid": datetime.datetime.now().strftime('%Y%m%d%H%M%S') + uuid.uuid4().hex,
            # 'player': [
            #     data['player'],
            # ]
        }
        # data.append("'ip':request.remote_addr","'_id':datetime.datetime.now().strftime('%Y%m%d%H%M%S') + uuid.uuid4().hex")
        res = {
            'code': 1,
            'data': msg
        }
        resp = json.dumps(res)
        redis_store.lpush('movie' + str(msg['mid']), json.dumps(msg))
    return Response(resp, mimetype='application/json')
