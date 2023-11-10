import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect, abort

# make a Flask application object called app
app = Flask(__name__)
app.config["DEBUG"] = True

#flash  the secret key to secure sessions
app.config['SECRET_KEY'] = 'your secret key'

#flash the secret key to secure sessions
app.config['SECRET KEY'] = 'your secret key'

#function to open a connection to the database.dc file
def get_db_connection():
    #get database connection
    conn = sqlite3.connect('database.db')

    #allow us to have name based access to columns
    #db connection will return rows we can access like python dictionary
    conn.row_factory = sqlite3.Row

    #return connection object
    return conn


#function to get a post
def get_post(post_id):
    #get db connection
    conn = get_db_connection()
    edit_query = 'SELECT * FROM posts WHERE id = ?'
    post = conn.execute(edit_query, (post_id,)).fetchone()
    conn.close()

    #if something goes wrong, abort with 404
    if post is None:
            abort(404)

    return post


# use the app.route() decorator to create a Flask view function called index()
@app.route('/')
def index():
    
    #get database connection
    conn = get_db_connection()

    #execute a query to get all posts from the database
    #use fetchall() to get all rows from query result
    query = 'SELECT * FROM posts'
    posts = conn.execute(query).fetchall()

    #close the connection
    conn.close()
    
    return render_template('index.html', posts=posts)

@app.route('/create/', methods=('GET', 'POST'))
def create():

    if request.method == "POST":
        #get title and content submitted by user
        title = request.form['title']
        content = request.form['content']    

        #display error if not submitted
        #otherwise make a database connection and insert the post
        if not title:
            flash('Title is required')
        elif not content:
            flash('Content is required')
        else:
            conn = get_db_connection()
            insert_query = 'INSERT INTO posts (title, content) VALUES (?, ?)'
            conn.execute(insert_query, (title, content))
            conn.commit()
            conn.close()
            #redirect to index page when successfully submitted
            return redirect(url_for('index'))

    return render_template('create.html')

#route to edit post
@app.route('/<int:id>/edit/', methods=('GET', 'POST'))
def edit(id):
    #get id from get_post()
    post = get_post(id)

    if request.method == "POST":
        #get title and content submitted by user
        title = request.form['title']
        content = request.form['content']    

        #display error if not submitted
        #otherwise make a database connection and insert the post
        if not title:
            flash('Title is required')
        elif not content:
            flash('Content is required')
        else:
            conn = get_db_connection()
            update_query = 'UPDATE posts SET title = ?, content = ? WHERE id = ?'
            conn.execute(update_query, (title, content, id))
            conn.commit()
            conn.close()
            #redirect to index page when successfully submitted
            return redirect(url_for('index'))

    return render_template('edit.html', post=post)


# route to delete a post
@app.route('/<int:id>/delete/', methods=('POST',))
def delete(id):
    #get the post
    post = get_post(id)

    #connect to databse
    conn = get_db_connection()

    #run a delete query
    delete_query = 'DELETE FROM posts WHERE id = ?'
    conn.execute(delete_query, (id,))

    #commit changes and close connection to databse
    conn.commit()
    conn.close()

    #show sucess message if deleted
    flash('{} has been deleted'.format(post['title']))
    
    #redirect to index page
    return  redirect(url_for('index'))


app.run(host="0.0.0.0", port=5001)