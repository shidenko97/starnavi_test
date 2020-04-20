from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.template.defaultfilters import slugify
from django_currentuser.middleware import get_current_authenticated_user


class User(AbstractUser):
    """Override standard user model"""

    last_action = models.DateTimeField(editable=False, null=True)

    def save(
        self,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None
    ):
        """Override standard save method for hashing password on user saving"""

        self.set_password(self.password)
        super().save(force_insert, force_update, using, update_fields)


class Post(models.Model):
    """Model for user posts"""

    title = models.CharField(max_length=128)
    url = models.SlugField(max_length=128, editable=False, unique=True)
    user = models.IntegerField(editable=False)
    body = models.TextField()
    created = models.DateTimeField(editable=False, auto_now=True)

    class Meta:
        ordering = ["created"]

    def save(
        self,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None
    ):
        """Override standard save method for saving post's user and
        slugify post's url"""

        self.url = slugify(self.title)
        self.user = get_current_authenticated_user().id
        super().save(force_insert, force_update, using, update_fields)

    def like_post(self) -> bool:
        """
        Method for liking post
        :return: If true - the post has been liking, else - has been unliking
        :rtype: bool
        """

        return self._set_post_mark(True)

    def dislike_post(self):
        """
        Method for disliking post
        :return: If true - the post has been disliking, else - has been
        undisliking
        :rtype: bool
        """

        return self._set_post_mark(False)

    def _set_post_mark(self, mark: bool) -> bool:
        """
        Set user's mark to post
        :param mark: True - like, False - dislike
        :type mark: bool
        :return: If true - the post has been marking, else - has been unmarking
        :rtype: bool
        """

        current_user = get_current_authenticated_user()

        post_mark = PostMark.objects.filter(post=self, user=current_user,
                                            sign=mark)

        if post_mark:
            post_mark.delete()
            return False

        PostMark(post=self, user=current_user, sign=mark).save()
        return True


class PostMark(models.Model):
    """Post's marks"""

    class MarkType(models.TextChoices):
        """Possible marks"""

        LIKE = "True", "Like"
        DISLIKE = "False", "Dislike"

    post = models.ForeignKey(Post, on_delete=models.CASCADE, editable=False)
    user = models.ForeignKey(get_user_model(),
                             on_delete=models.CASCADE, editable=False)
    sign = models.CharField(
        max_length=7,
        choices=MarkType.choices
    )
    datetime = models.DateTimeField(auto_now=True)
