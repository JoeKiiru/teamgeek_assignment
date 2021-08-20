import graphene
from graphene import relay
from graphql_relay.node.node import from_global_id

from .. import models, types
from ..database import db


class CreatePostInput:
    title = graphene.String(required=True)
    content = graphene.String(required=True)


class CreatePostSuccess(graphene.ObjectType):
    post = graphene.Field(types.PostNode, required=True)


class CreatePostOutput(graphene.Union):
    class Meta:
        types = (CreatePostSuccess,)


class CreatePost(relay.ClientIDMutation):
    Input = CreatePostInput
    Output = CreatePostOutput

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        new_post = models.Post(**input)

        db.session.add(new_post)
        db.session.commit()

        return CreatePostSuccess(post=new_post)


class UpdatePostInput:
    id = graphene.String(required=True)
    title = graphene.String(required=True)
    content = graphene.String(required=True)


class UpdatePostSuccess(graphene.ObjectType):
    post = graphene.Field(types.PostNode, required=True)


class UpdatePostOutput(graphene.Union):
    class Meta:
        types = (UpdatePostSuccess,)


class UpdatePost(relay.ClientIDMutation):
    Input = UpdatePostInput
    Output = UpdatePostOutput

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        pk = from_global_id(input["id"])[1]
        post = models.Post.query.get(pk)
        post.title = input["title"]
        post.content = input["content"]
        db.session.commit()

        return UpdatePostSuccess(post=post)


class DeletePostInput:
    id = graphene.String(required=True)


class DeletePostSuccess(graphene.ObjectType):
    post = graphene.Field(types.PostNode, required=True)



class DeletePostOutput(graphene.Union):
    class Meta:
        types = (DeletePostSuccess,)


class DeletePost(relay.ClientIDMutation):
    Input = DeletePostInput
    Output = DeletePostOutput

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        pk = from_global_id(input["id"])[1]
        post = models.Post.query.get(pk)
        db.session.delete(post)
        db.session.commit()

        return DeletePostSuccess(post=post)