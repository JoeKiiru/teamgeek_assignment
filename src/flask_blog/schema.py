import graphene
from graphene import relay, List
from graphene_sqlalchemy import SQLAlchemyConnectionField

from . import models, mutations
from .types import PostConnection, TagConnection

class Query(graphene.ObjectType):
    node = relay.Node.Field()
    posts = SQLAlchemyConnectionField(PostConnection)
    tags = SQLAlchemyConnectionField(TagConnection)

    def resolve_post_tags(self, info, *args, **kwargs):
        post_tags = List(models.Post.post_tags)

        query = SQLAlchemyConnectionField.get_query(
            post_tags, info, *args, **kwargs
        )
        
        return query.all()

    def resolve_posts(self, info, *args, **kwargs):
        query = SQLAlchemyConnectionField.get_query(
            models.Post, info, *args, **kwargs
        )
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
