from app import app,db
from app.models import *
from flask_migrate import Migrate,MigrateCommand
from flask_script import Manager


migrate=Migrate(app,db)
manager = Manager(app)
manager.add_command('db',MigrateCommand)

if __name__ == '__main__':
    db.create_all()
    superuser = Admin(
    name='zzzzzyk',
    pwd='zyk666!!',
    is_super=0,
    role_id='',
    )
    db.session.add(superuser)
    db.session.commit()
    # manager.run()
