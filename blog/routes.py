# blog/routes.py

from flask import render_template, Flask, redirect, url_for, request
from blog import app, db  # Import db here
from blog.models import Entry
from blog.forms import EntryForm  # Import EntryForm



#@app.route("/")
#def index():
#   return render_template("base.html")

@app.route("/")
def index():
   all_posts = Entry.query.filter_by(is_published=True).order_by(Entry.pub_date.desc())
   return render_template("homepage.html", all_posts=all_posts)


@app.route("/new-post/", methods=["GET", "POST"])
@app.route("/edit-post/<int:entry_id>", methods=["GET", "POST"])
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