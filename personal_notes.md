Steps to create the database:

from project import app, db
app.app_context().push()
db.create_all()

from Docs

--------------------------------------------

Security : Hash, salt, algo version, cost factor, delimeter in hash : $, UFT-8 (flask-bcrypt)
For managing user loggin session : flask_login

--------------------------------------------

Fixed the bug for Operation Error, where it was saying the database user was missing. Fixed with db.creat_all() to create the tables.
Fixed the bug for mispell logot to logouy

Fixed these lines with strip so it can have the correct route name
    next_page = request.args.get('next')   # Need to know it better and remember this.
            flash('You have been logged in!', 'success')
            return redirect(url_for(next_page.strip("/"))) if next_page else redirect(url_for('home')) # Normal ternary operation.
