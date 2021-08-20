import graphene
from graphene import relay
from graphql_relay.node.node import from_global_id

from .. import models, types
from ..database import db


class PostSuccess(graphene.ObjectType):
    post = graphene.Field(types.PostNode, required=True)


class PostOutput(graphene.Union):
    class Meta:
        types = (PostSuccess,)


class CreatePostInput:
    title = graphene.String(required=True)
    content = graphene.String(required=True)


class CreatePost(relay.ClientIDMutation):
    Input = CreatePostInput
    Output = PostOutput

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        new_post = models.Post(**input)

        db.session.add(new_post)
        db.session.commit()

        return PostSuccess(post=new_post)


class UpdatePostInput:
    id = graphene.String(required=True)
    title = graphene.String(required=True)
    content = graphene.String(required=True)


class UpdatePost(relay.ClientIDMutation):
    Input = UpdatePostInput
    Output = PostOutput

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        pk = from_global_id(input["id"])[1]
        post = models.Post.query.get(pk)
        post.title = input["title"]
        post.content = input["content"]
        db.session.commit()

        return PostSuccess(post=post)


class DeletePostInput:
    id = graphene.String(required=True)


class DeletePost(relay.ClientIDMutation):
    Input = DeletePostInput
    Output = PostOutput

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        pk = from_global_id(input["id"])[1]
        post = models.Post.query.get(pk)
        db.session.delete(post)
        db.session.commit()

        return PostSuccess(post=post)