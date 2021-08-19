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
        
        if "tag" in kwargs:
            tag_name = kwargs["tag"]
            query = query.filter(models.Post.post_tags.any(tag=tag_name))
        elif "createdAt" in kwargs:
            filter_type = kwargs["createdAt"]
            if filter_type == "newest":
                query = models.Post.query.order_by(models.Post.created_at.desc())
            elif filter_type == "oldest":
                query = models.Post.query.order_by(models.Post.created_at.asc())
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
        
                query = models.Post.query.filter(models.Post.created_at >= pastTime)
                query = query.order_by(models.Post.created_at.desc())

        return query.all()
    
    def resolve_tags(self, info, *args, **kwargs):
        query = SQLAlchemyConnectionField.get_query(
            models.Tag, info, *args, **kwargs
        )
        return query.all()
    
class Mutation(graphene.ObjectType):
    create_post = mutations.CreatePost.Field()
    update_post = mutations.UpdatePost.Field()
    delete_post = mutations.DeletePost.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
