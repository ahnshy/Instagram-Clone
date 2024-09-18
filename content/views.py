import logging
from uuid import uuid4
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from user.models import User
from .models import Feed, Reply, Like
import os
from InstagramClone.settings import MEDIA_ROOT

logger = logging.getLogger("InstagramClone")

class Main(APIView):
    def get(self, request):
        print("call Content get method.")

        email = request.session.get('email', None)
        # print(request.session['email']) # 로그인 계정

        if email is None:
            return render(request, "user/login.html")

        user = User.objects.filter(email=email).first()
        #print(user.name) # 로그인 사용자 이름

        if user is None:
            return render(request, "user/login.html")


        feed_list = Feed.objects.all().order_by('-id')
        return render(request, 'Instagram/index.html', context=dict(feed_list=feed_list, user=user))

    # def get(self, request):
    #     email = request.session.get('email', None)
    #
    #     if email is None:
    #         return render(request, "user/login.html")
    #
    #     user = User.objects.filter(email=email).first()
    #
    #     if user is None:
    #         return render(request, "user/login.html")
    #
    #     feed_object_list = Feed.objects.all().order_by('-id')  # select  * from content_feed;
    #     feed_list = []
    #
    #     for feed in feed_object_list:
    #         user = User.objects.filter(email=feed.email).first()
    #         reply_object_list = Reply.objects.filter(feed_id=feed.id)
    #         reply_list = []
    #         for reply in reply_object_list:
    #             user = User.objects.filter(email=reply.email).first()
    #             reply_list.append(dict(reply_content=reply.reply_content,
    #                                    nickname=user.nickname))
    #         like_count=Like.objects.filter(feed_id=feed.id, is_like=True).count()
    #         is_liked=Like.objects.filter(feed_id=feed.id, email=email, is_like=True).exists()
    #         is_marked=Bookmark.objects.filter(feed_id=feed.id, email=email, is_marked=True).exists()
    #         feed_list.append(dict(id=feed.id,
    #                               image=feed.image,
    #                               content=feed.content,
    #                               like_count=like_count,
    #                               profile_image=user.profile_image,
    #                               nickname=user.nickname,
    #                               reply_list=reply_list,
    #                               is_liked=is_liked,
    #                               is_marked=is_marked
    #                               ))
    #
    #
    #     return render(request, "instagram/index.html", context=dict(feeds=feed_list, user=user))


class UploadFeed(APIView):
    def post(self, request):

        # 일단 파일 불러와
        file = request.FILES['file']

        uuid_name = uuid4().hex
        save_path = os.path.join(MEDIA_ROOT, uuid_name)

        with open(save_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        imageName = uuid_name
        contentText = request.data.get('content')
        userEmail = request.session.get('email', "ahnshy@gmail.com")

        Feed.objects.create(image=imageName, content=contentText, email=userEmail)

        return Response(status=200)


class Profile(APIView):
    def get(self, request):
        email = request.session.get('email', None)

        if email is None:
            return render(request, "user/login.html")

        user = User.objects.filter(email=email).first()

        if user is None:
            return render(request, "user/login.html")

        feed_list = Feed.objects.filter(email=email)
        return render(request, 'content/profile.html', context=dict(feed_list=feed_list,
                                                                    user=user))
        # like_list = list(Like.objects.filter(email=email, is_like=True).values_list('feed_id', flat=True))
        # like_feed_list = Feed.objects.filter(id__in=like_list)
        # bookmark_list = list(Bookmark.objects.filter(email=email, is_marked=True).values_list('feed_id', flat=True))
        # bookmark_feed_list = Feed.objects.filter(id__in=bookmark_list)
        # return render(request, 'content/profile.html', context=dict(feed_list=feed_list,
        #                                                             like_feed_list=like_feed_list,
        #                                                             bookmark_feed_list=bookmark_feed_list,
        #                                                             user=user))

class UploadReply(APIView):
    def post(self, request):
        feed_id = request.data.get('feed_id', None)
        reply_content = request.data.get('reply_content', None)
        email = request.session.get('email', None)

        Reply.objects.create(feed_id=feed_id, reply_content=reply_content, email=email)

        return Response(status=200)

    class ToggleLike(APIView):
        def post(self, request):
            feed_id = request.data.get('feed_id', None)
            favorite_text = request.data.get('favorite_text', True)

            if favorite_text == 'favorite_border':
                is_like = True
            else:
                is_like = False
            email = request.session.get('email', None)

            like = Like.objects.filter(feed_id=feed_id, email=email).first()

            if like:
                like.is_like = is_like
                like.save()
            else:
                Like.objects.create(feed_id=feed_id, is_like=is_like, email=email)

            return Response(status=200)
