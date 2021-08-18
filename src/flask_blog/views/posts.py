from datetime import datetime, timedelta
from flask import Blueprint, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort

from ..database import db
from ..models import Post, Tag

posts = Blueprint("posts", __name__)


@posts.route("/")
def index():
    posts = Post.query.all()
    return render_template("index.html", posts=posts, showFilter=True)


@posts.route("/<int:post_id>", methods=("GET", "POST"))
def post(post_id):
    post = Post.query.get(post_id)
    if not post:
        abort(404)
    else:
        if request.method == "POST":
            tag = request.form["tag"]
            
            add_tag = Tag.query.filter_by(tag=tag)
            if add_tag.all():
                if add_tag.first().post_id == post_id:
                    flash("Tag already added!")
                    return render_template("post.html", post=post)
            else:
                add_tag = Tag(tag = tag)
                db.session.add(add_tag)
                db.session.commit() 
            
            post.tags.append(add_tag)
            db.session.commit()
            
    return render_template("post.html", post=post)


@posts.route("/create", methods=("GET", "POST"))
def create():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]

        if not title:
            flash("Title is required!")
        else:
            new_post = Post(title=title, content=content)

            db.session.add(new_post)
            db.session.commit()

            return redirect(url_for("posts.index"))
    return render_template("create.html")


@posts.route("/<int:post_id>/edit", methods=("GET", "POST"))
def edit(post_id):
    post = Post.query.get(post_id)
    if not post:
        abort(404)

    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]

        if not title:
            flash("Title is required!")
        else:
            post.title = title
            post.content = content

            db.session.commit()

            return redirect(url_for("posts.index"))

    return render_template("edit.html", post=post)


@posts.route("/<int:post_id>/delete", methods=("POST",))
def delete(post_id):
    post = Post.query.get(post_id)
    if not post:
        abort(404)

    db.session.delete(post)
    db.session.commit()

    flash('"{}" was successfully deleted!'.format(post.id))
    return redirect(url_for("posts.index"))

@posts.route("/newest")
def newest():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template("index.html", posts=posts, showFilter=True)

@posts.route("/lasthour")
def lasthour():
    pastHour = datetime.now() - timedelta(hours=1)
    posts = Post.query.filter(Post.created_at >= pastHour)
    posts = posts.order_by(Post.created_at.desc())
    return render_template("index.html", posts=posts, showFilter=True)

@posts.route("/lastday")
def lastday():
    pastDay = datetime.now() - timedelta(days=1)
    posts = Post.query.filter(Post.created_at >= pastDay)
    posts = posts.order_by(Post.created_at.desc())
    return render_template("index.html", posts=posts, showFilter=True) 

@posts.route("/last7days")
def last7days():
    past7days = datetime.now() - timedelta(days=7)
    posts = Post.query.filter(Post.created_at >= past7days)
    posts = posts.order_by(Post.created_at.desc())
    return render_template("index.html", posts=posts, showFilter=True)

@posts.route("/lastmonth")
def lastmonth():
    pastMonth = datetime.now() - timedelta(days=30)
    posts = Post.query.filter(Post.created_at >= pastMonth)
    posts = posts.order_by(Post.created_at.desc())
    return render_template("index.html", posts=posts, showFilter=True)


@posts.route("/lastyear")
def lastyear():
    pastYear = datetime.now() - timedelta(days=365)
    posts = Post.query.filter(Post.created_at >= pastYear)
    posts = posts.order_by(Post.created_at.desc())
    return render_template("index.html", posts=posts, showFilter=True)
