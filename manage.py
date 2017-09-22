from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
import unittest
import os

from app import app, db

# app.config.from_object(os.environ['APP_SETTINGS'])
app.config.from_object('config.TestConfig')
migrate = Migrate(app, db)
manager = Manager(app)

# python manage.py db init    - creates migrations folder
# python manage.py db migrate - creates migrations script in migrations/versions
# python manage.py db upgrade - runs generated migration script @upgrade
# python manage.py db downgrade -1  - rollsback the latest migration
# python manage.py db histody  - shows list of migrations with ids
# python manage.py db downgrade :revisionId  - rollsback to migration by revisionId
manager.add_command('db', MigrateCommand)

@manager.command
def test():
    """ Runs the test suite """
    tests = unittest.TestLoader().discover('.')
    unittest.TextTestRunner(verbosity=2).run(tests)

if __name__ == '__main__':
    manager.run()
