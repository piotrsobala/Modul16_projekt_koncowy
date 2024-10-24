# blog/routes.py

from flask import render_template, Flask, redirect, url_for, request, session, flash
from blog import app, db  # Import db here
from blog.models import Entry, db
from blog.forms import EntryForm, LoginForm
import functools

def login_required(view_func):
   @functools.wraps(view_func)
   def check_permissions(*args, **kwargs):
      if session.get('logged_in'):
         return view_func(*args, **kwargs)
      return redirect(url_for('login', next=request.path))
   return check_permissions

#@app.route("/")
#def index():
#   return render_template("base.html")

@app.route("/")
def index():
   all_posts = Entry.query.filter_by(is_published=True).order_by(Entry.pub_date.desc())
   return render_template("homepage.html", all_posts=all_posts)


@app.route("/new-post/", methods=["GET", "POST"])
@app.route("/edit-post/<int:entry_id>", methods=["GET", "POST"])
@login_required
def manage_entry(entry_id=None):
   # If entry_id is provided, we are editing; otherwise, we are creating
   entry = Entry.query.filter_by(id=entry_id).first() if entry_id else None
   form = EntryForm(obj=entry)  # Prepopulate the form with entry data if editing
   errors = None

   if request.method == 'POST':
      if form.validate_on_submit():
         if entry:  # If editing, update the existing entry
            form.populate_obj(entry)
         else:  # If creating, create a new entry
            entry = Entry(
               title=form.title.data,
               body=form.body.data,
               is_published=form.is_published.data
               )
            db.session.add(entry)

         db.session.commit()  # Commit the changes

         # Optionally redirect after creating or editing
         return redirect(url_for('index'))  # Redirect to homepage or another page after success
      else:
         errors = form.errors

   return render_template("entry_form.html", form=form, errors=errors)

@app.route("/login/", methods=['GET', 'POST'])
def login():
   form = LoginForm()
   next_url = request.args.get('next')
   errors = None

   if request.method == 'POST':
      if form.validate_on_submit():
         session['logged_in'] = True
         session.permanent = True  # Use cookie to store session.
         flash('You are now logged in.', 'success')
         return redirect(next_url or url_for('index'))
      else:
         errors = form.errors

   return render_template("login_form.html", form=form, errors=errors)


@app.route('/logout/', methods=['GET', 'POST'])
def logout():
   if request.method == 'POST':
       session.clear()
       flash('You are now logged out.', 'success')
   return redirect(url_for('index'))

@app.route("/drafts/", methods=['GET'])
@login_required
def list_drafts():
   drafts = Entry.query.filter_by(is_published=False).order_by(Entry.pub_date.desc())
   return render_template("drafts.html", drafts=drafts)

@app.route('/delete/<int:entry_id>', methods=['POST'])
@login_required
def delete_entry(entry_id):
    # Pobierz wpis z bazy danych
    entry = Entry.query.get(entry_id)

    # Sprawdź, czy wpis istnieje
    if entry is None:
        flash("Wpis o podanym ID nie istnieje.", 'danger')
        return redirect(url_for('index'))

    # Usuń wpis z bazy danych
    db.session.delete(entry)
    db.session.commit()

    # Wiadomość typu flash
    flash("Wpis został usunięty.", 'success')

    # Przekierowanie na stronę główną
    return redirect(url_for('index'))