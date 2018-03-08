from app import app, db
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

import models

## ------------------------ Migrations ------------------------ ##
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    # $ python migrate.py db init
    # $ python migrate.py db migrate
    # $ python migrate.py db upgrade
    manager.run()