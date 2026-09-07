from django.db import models
from django.utils.text import slugify


class Blog(models.Model):

    title = models.CharField(
        max_length=200
    )

    slug = models.SlugField(
        unique=True,
        blank=True,
        max_length=250
    )

    category = models.CharField(
        max_length=100,
        default="Programming"
    )

    short_description = models.TextField(
        max_length=300
    )

    content = models.TextField()

    image = models.ImageField(
        upload_to="blog_images/",
        blank=True,
        null=True
    )

    author = models.CharField(
        max_length=100,
        default="Gurleen"
    )

    reading_time = models.IntegerField(
        default=5
    )

    views = models.IntegerField(
        default=0
    )

    # ❤️ Likes count
    likes = models.PositiveIntegerField(
        default=0
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def save(self, *args, **kwargs):

        # Title se base slug generate hoga
        base_slug = slugify(self.title)

        # Agar title se slug generate na ho
        if not base_slug:
            base_slug = "blog"

        slug = base_slug
        counter = 1

        # Same slug already database mein hai?
        # Current object ko exclude karenge taaki edit karte waqt
        # problem na aaye.
        while Blog.objects.filter(
            slug=slug
        ).exclude(
            pk=self.pk
        ).exists():

            slug = f"{base_slug}-{counter}"
            counter += 1

        self.slug = slug

        # Reading time automatically calculate
        if self.content:

            word_count = len(
                self.content.split()
            )

            # Approximately 200 words = 1 minute
            self.reading_time = max(
                1,
                (word_count + 199) // 200
            )

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Category(models.Model):

    name = models.CharField(
        max_length=100
    )

    def __str__(self):
        return self.name

class Comment(models.Model):

    blog = models.ForeignKey(
        Blog,
        on_delete=models.CASCADE,
        related_name="comments"
    )

    name = models.CharField(
        max_length=100
    )

    text = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.name} - {self.blog.title}"


class SavedBlog(models.Model):

    blog = models.ForeignKey(
        Blog,
        on_delete=models.CASCADE,
        related_name="saved_by"
    )

    user = models.ForeignKey(
        "auth.User",
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = ("blog", "user")

    def __str__(self):
        return f"{self.user.username} saved {self.blog.title}"

class ContactMessage(models.Model):

    name = models.CharField(max_length=100)

    email = models.EmailField()

    subject = models.CharField(max_length=200)

    message = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"

from django.db import models


class CommunityMember(models.Model):

    name = models.CharField(max_length=100)

    email = models.EmailField(unique=True)

    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name