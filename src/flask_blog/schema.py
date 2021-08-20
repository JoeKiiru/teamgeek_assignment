import graphene
from graphene import relay, List
from graphene_sqlalchemy import SQLAlchemyConnectionField
from datetime import datetime, timedelta

from flask_blog.views.posts import filter_by_creation

from . import models, mutations
from .types import PostConnection, TagConnection

class Query(graphene.ObjectType):
    node = relay.Node.Field()
    posts = SQLAlchemyConnectionField(
        PostConnection, 
        tag=graphene.String(),
        createdAt=graphene.String()
    )
    tags = SQLAlchemyConnectionField(TagConnection)
    
    def resolve_post_tags(self, info, *args, **kwargs):
        post_tags = List(models.Post.post_tags)
        
        query = SQLAlchemyConnectionField.get_query(
            post_tags, info, *args, **kwargs
        )
        return query.all()

    def resolve_posts(self, info, *args, **kwargs,):
        query = SQLAlchemyConnectionField.get_query(
            models.Post, info, *args, **kwargs
        )
        get_filtered_posts = filter_post(kwargs)
        print(get_filtered_posts)
        if get_filtered_posts:
            if "Invalid" == get_filtered_posts:
                query = []
                return query
            else:
                query = get_filtered_posts
        return query.all()


    def resolve_tags(self, info, *args, **kwargs):
        query = SQLAlchemyConnectionField.get_query(
            models.Tag, info, *args, **kwargs
        )
        return query.all()

def filter_post(filter_type):
    posts = None
    if "tag" in filter_type:
        tag_name = filter_type["tag"]
        posts = models.Post.query.filter(
            models.Post.post_tags.any(tag=tag_name)
        )
    elif "createdAt" in filter_type:
        time_filter = filter_type["createdAt"]
        if time_filter == "newest":
            posts = models.Post.query.order_by(
                models.Post.created_at.desc()
            )
        elif time_filter == "oldest":
            posts = models.Post.query.order_by(models.Post.created_at.asc())
        else:
            pastTime = 0
            if time_filter == "lasthour":
                pastTime = datetime.now() - timedelta(hours=1)
            elif time_filter == "lastday":
                pastTime = datetime.now() - timedelta(days=1)
            elif time_filter == "last7days":
                pastTime = datetime.now() - timedelta(days=7)
            elif time_filter == "lastmonth":
                pastTime = datetime.now() - timedelta(days=30)
            elif time_filter == "lastyear":
                pastTime = datetime.now() - timedelta(days=365)
            else:
                return "Invalid"
    
            posts = models.Post.query.filter(
                models.Post.created_at >= pastTime
            )
            posts = posts.order_by(models.Post.created_at.desc())
    
    return posts

class Mutation(graphene.ObjectType):
    create_post = mutations.CreatePost.Field()
    update_post = mutations.UpdatePost.Field()
    delete_post = mutations.DeletePost.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
