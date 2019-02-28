# MovieWeb
###网站使用flask轻量级框架，数据库使用MySQL，消息队列使用的是Redis，使用sqlalchemy实现ORM,  使用flask_wtf和wtform处理表单，通过flask_migrate和flask_script更新数据库表结构。后台功能有：标签管理、电影管理、预告管理、会员管理、评论管理、收藏管理、权限管理、角色管理、管理员管理；网站前台功能有：用户注册、登陆、登出、会员信息页、修改密码、评论记录、登陆日志、收藏电影、通过标签筛选电影、电影播放、电影评论、电影收藏、电影弹幕。
###使用到的第三方包包括：
flask
flask-script
flask-sqlalchemy
flask-wtf
Jinja2
pymysql
sqlalchemy
werkzeug
wtform
flask_migrate
flask_redis
