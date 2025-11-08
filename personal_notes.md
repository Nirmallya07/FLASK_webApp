Steps to create the database:

from project import app, db
app.app_context().push()
db.create_all()

--------------------------------------------

Security : Hash, salt, algo version, cost factor, delimeter in hash : $, UFT-8
