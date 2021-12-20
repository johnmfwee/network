from .models import User, Follow, Post, Like
from django.db.models import F
from datetime import datetime
from django.utils import timezone


def get_user_obj_by_username(username):
    """
    Returns user object for given username
    """

    userobj = User.objects.get(username=username)
    return userobj


def get_user_obj_by_userId(id):
    """
    Returns user object for given user id
    """

    userobj = User.objects.get(id=id)
    return userobj


def queryset_post_content(post_id):
    """
    Returns post content for given post id
    """

    contents = queryset_post_object(post_id).values_list("contents", flat=True)
    return contents


def queryset_post_object(post_id):
    """
    Returns post queryset object for gien post id
    """

    postobj = Post.objects.filter(id=post_id)
    return postobj


def update_post(post_id, contents):
    """
    save the post after edit for given post_id and contents
    """

    date_time = timezone.now()
    postobj = Post.objects.filter(id=post_id)
    postobj.update(contents=contents, date_and_time=date_time)

    return postobj


def delete_post(post_id):
    """
    delete the post, for given post_id
    """

    postobj = Post.objects.filter(id=post_id)
    if postobj:
        postobj.delete()
        return 1
    return 0


def get_follower_ids(id):
    """
    get all the followers for given user id
    """

    userobj = get_user_obj_by_userId(id)
    followers = Follow.objects.values('following').filter(following=userobj.id).values_list("follower_id", flat=True)

    return followers


def get_user_networks(id):
    """
    return user follow and following list for given user id
    """

    userobj = get_user_obj_by_userId(id)
    current_following = Follow.objects.filter(follower=userobj.id)

    if len(current_following) == 0:
        user_can_follow = User.objects.all().exclude(username=userobj).values('id', 'username')

        user_currently_follows = 0

    elif len(current_following) == len(User.objects.all().exclude(username=userobj)):
        user_can_follow = 0

        ids = Follow.objects.values_list('following', flat=True).filter(follower=userobj.id)
        user_currently_follows = User.objects.filter(id__in=set(ids)).values('id', 'username')

    else:
        user_currently_follow_ids = Follow.objects.values_list('following', flat=True).filter(follower=userobj.id)

        user_currently_follows = User.objects.filter(id__in=set(user_currently_follow_ids)).values('id', 'username')
        user_can_follow = User.objects.all().exclude(username=userobj).exclude(id__in=set(user_currently_follow_ids)).values('id', 'username')

    return user_currently_follows, user_can_follow
