from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Group(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(null=False, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField(verbose_name="Текст",
                            help_text="Здесь будет текст вашего поста")
    pub_date = models.DateTimeField("date published",
                                    auto_now_add=True, db_index=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name="posts")
    group = models.ForeignKey(Group, on_delete=models.SET_NULL,
                              related_name="group_posts",
                              blank=True, null=True, verbose_name="Группа",
                              help_text="Выберете группу")
    image = models.ImageField(upload_to="posts/", blank=True, null=True)

    class Meta:
        ordering = ("-pub_date",)

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name="comments")
    text = models.TextField(verbose_name="Комментарий",
                            help_text="Здесь будет текст вашего комментария")
    created = models.DateTimeField("date published",
                                   auto_now_add=True, db_index=True)

    class Meta:
        ordering = ("-created",)

    def __str__(self):
        return self.text[:15]


class Follow(models.Model):
    models.UniqueConstraint(fields=["user", "author"], name="uniq_follow")
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name="follower")
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name="following")
