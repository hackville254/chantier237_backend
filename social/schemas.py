from ninja import ModelSchema, Schema
from pydantic import validator
from ninja.errors import HttpError
from typing import Optional
from typing import List

from .models import MarkertPlace

class ProfileSchema(Schema):
    nom_page: str
    pays: str
    ville: str


class UpdateProfileSchema(Schema):
    nom_page: Optional[str]
    pays: Optional[str]
    ville: Optional[str]


class GetProfileSchema(Schema):
    id: str
    nom_page: str
    pays: str
    ville: str


class FollowerSchema(Schema):
    nom_page: str


class CommentSchema(Schema):
    post_id: str
    content: str


class GetCommentSchema(Schema):
    post_id: str


class ReplyCommentSchema(Schema):
    comment_id: str
    content: str


class LikeSchema(Schema):
    post_id: str




class ImageSchema(Schema):
    url: str

class ProfileSchema(Schema):
    nom_page: str
    number: str
    isFollow: bool
    photo_profil: str

class PostSchema(Schema):
    id: int
    page: ProfileSchema
    content: str
    date_creation: str
    images: List[ImageSchema]
    post_likes_count: int
    isLike: bool


