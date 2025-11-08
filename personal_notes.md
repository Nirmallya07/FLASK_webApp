Steps to create the database:

from project import app, db
app.app_context().push()
db.create_all()

--------------------------------------------

