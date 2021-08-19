from datetime import datetime, timedelta
from flask import Blueprint, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort

from ..database import db
from ..models import Post, Tag

posts = Blueprint("posts", __name__)


@posts.route("/")
def index():
    posts = Post.query.all()
    tags = Tag.query.all()
    return render_template(
        "index.html", 
        posts=posts, 
        showFilterByCreation=True, 
        showFilterByTag=True, 
        tags=tags
    )


@posts.route("/<int:post_id>", methods=("GET", "POST"))
def post(post_id):
    post = Post.query.get(post_id)
    if not post:
        abort(404)
    elif request.method == "POST":
            redirectUrl = ("/{0}").format(post_id)
            tag = request.form["tag"]
            
            add_tag = Tag.query.filter_by(tag=tag)
            if add_tag.all():
                if add_tag.first().post_id == post_id:
                    flash("Tag already added!")
                    return redirect(redirectUrl)
                else:
                    add_tag = add_tag.first()
            else:
                add_tag = Tag(tag = tag)
                db.session.add(add_tag)
                db.session.commit() 
            
            post.post_tags.append(add_tag)
            db.session.commit()

            return redirect(redirectUrl)
            
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


@posts.route("/filterbycreation/<string:filter_type>")
def filter_by_creation(filter_type):
    
    if filter_type == "newest":
        posts = Post.query.order_by(Post.created_at.desc()).all()
    elif filter_type == "oldest":
        posts = Post.query.order_by(Post.created_at.asc()).all()
    else:
        pastTime = 0
        if filter_type == "lasthour":
            pastTime = datetime.now() - timedelta(hours=1)
        elif filter_type == "lastday":
            pastTime = datetime.now() - timedelta(days=1)
        elif filter_type == "last7days":
            pastTime = datetime.now() - timedelta(days=7)
        elif filter_type == "lastmonth":
            pastTime = datetime.now() - timedelta(days=30)
        elif filter_type == "lastyear":
            pastTime = datetime.now() - timedelta(days=365)
        
        posts = Post.query.filter(Post.created_at >= pastTime)
        posts = posts.order_by(Post.created_at.desc())

    return render_template(
        "index.html", 
        posts=posts, 
        showFilterByCreation=True,
    )


@posts.route("/filterbytag/<string:tag>")
def filter_by_tag(tag):
    posts = Post.query.filter(Post.post_tags.any(tag=tag)).all()
    tags = Tag.query.all()

    return render_template(
        "index.html", 
        posts=posts,
        tags=tags, 
        showFilterByTag=True
    )
