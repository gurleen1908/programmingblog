from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate
from django.db.models import Q
from django.core.mail import EmailMessage
from django.conf import settings

from .models import Blog, SavedBlog, ContactMessage
from .models import CommunityMember


# =========================================================
# HOME
# =========================================================

def home(request):

    blogs = Blog.objects.all().order_by("-created_at")

    total_blogs = Blog.objects.count()

    total_categories = Blog.objects.values(
        "category"
    ).distinct().count()

    total_views = sum(
        blog.views for blog in blogs
    )

    return render(
        request,
        "home.html",
        {
            "blogs": blogs,
            "total_blogs": total_blogs,
            "total_categories": total_categories,
            "total_views": total_views,
        }
    )

# =========================================================
# BLOG DETAIL
# =========================================================

def blog_detail(request, slug):

    blog = get_object_or_404(
        Blog,
        slug=slug
    )

    # Increase views
    blog.views += 1

    blog.save(
        update_fields=["views"]
    )

    # Related blogs
    related_blogs = Blog.objects.filter(
        category=blog.category
    ).exclude(
        id=blog.id
    ).order_by("-created_at")[:3]

    return render(
        request,
        "blog_detail.html",
        {
            "blog": blog,
            "related_blogs": related_blogs
        }
    )


# =========================================================
# ABOUT
# =========================================================

def about(request):

    latest_blogs = Blog.objects.all().order_by(
        "-created_at"
    )[:3]

    return render(
        request,
        "about.html",
        {
            "latest_blogs": latest_blogs
        }
    )


# =========================================================
# TOPIC
# =========================================================

def topic(request, topic_name):

    topic_name = topic_name.replace("-", " ")

    blogs = Blog.objects.filter(

        Q(category__icontains=topic_name) |

        Q(title__icontains=topic_name) |

        Q(content__icontains=topic_name)

    ).order_by("-created_at")

    topic_data = {

        "python": {
            "title": "Python Programming",
            "icon": "🐍",
            "description":
                "Learn Python through practical tutorials, programming concepts and real-world projects.",
            "learn":
                "Python fundamentals, functions, OOP, automation, backend development and practical programming."
        },

        "django": {
            "title": "Django Web Development",
            "icon": "🌐",
            "description":
                "Build powerful and scalable web applications with Python and Django.",
            "learn":
                "Django fundamentals, models, views, templates, authentication, databases and deployment."
        },

        "javascript": {
            "title": "JavaScript Development",
            "icon": "⚡",
            "description":
                "Create interactive, dynamic and modern web experiences using JavaScript.",
            "learn":
                "JavaScript fundamentals, DOM manipulation, events, APIs and interactive web development."
        },

        "sql": {
            "title": "SQL & Databases",
            "icon": "🗄️",
            "description":
                "Learn how to work with databases, write powerful queries and manage structured data.",
            "learn":
                "SQL queries, filtering, joins, aggregation, database design and data management."
        }
    }

    key = topic_name.lower()

    data = topic_data.get(
        key,
        {
            "title": topic_name.title(),
            "icon": "💻",
            "description":
                "Explore programming tutorials and practical development resources.",
            "learn":
                "Programming concepts, practical examples and real-world development."
        }
    )

    return render(
        request,
        "topic.html",
        {
            "topic": data,
            "blogs": blogs
        }
    )


# =========================================================
# SEARCH
# =========================================================

def search(request):

    query = request.GET.get(
        "q",
        ""
    ).strip()

    blogs = Blog.objects.all().order_by(
        "-created_at"
    )

    if query:

        blogs = blogs.filter(

            Q(title__icontains=query) |

            Q(content__icontains=query) |

            Q(short_description__icontains=query) |

            Q(category__icontains=query) |

            Q(author__icontains=query)

        ).distinct()

    return render(
        request,
        "search.html",
        {
            "blogs": blogs,
            "query": query
        }
    )


# =========================================================
# MY BLOGS
# =========================================================

@login_required
def my_blogs_view(request):

    user_blogs = Blog.objects.filter(
        author=request.user.username
    ).order_by(
        "-created_at"
    )

    return render(
        request,
        "accounts/my_blogs.html",
        {
            "blogs": user_blogs
        }
    )


# =========================================================
# LIKE BLOG
# =========================================================

@require_POST
def like_blog(request, slug):

    blog = get_object_or_404(
        Blog,
        slug=slug
    )

    liked_blogs = request.session.get(
        "liked_blogs",
        []
    )

    if slug in liked_blogs:

        blog.likes = max(
            0,
            blog.likes - 1
        )

        liked_blogs.remove(
            slug
        )

        liked = False

    else:

        blog.likes += 1

        liked_blogs.append(
            slug
        )

        liked = True

    blog.save(
        update_fields=["likes"]
    )

    request.session["liked_blogs"] = liked_blogs

    request.session.modified = True

    return JsonResponse(
        {
            "likes": blog.likes,
            "liked": liked
        }
    )


# =========================================================
# CREATE BLOG
# =========================================================

@login_required
def create_blog_view(request):

    if request.method == "POST":

        title = request.POST.get(
            "title",
            ""
        ).strip()

        category = request.POST.get(
            "category",
            ""
        ).strip()

        custom_category = request.POST.get(
            "custom_category",
            ""
        ).strip()

        short_description = request.POST.get(
            "short_description",
            ""
        ).strip()

        content = request.POST.get(
            "content",
            ""
        ).strip()

        image = request.FILES.get(
            "image"
        )

        # OTHER CATEGORY
        if category == "Other":

            category = custom_category

        # VALIDATION
        if not title:

            messages.error(
                request,
                "Please enter a blog title."
            )

            return redirect(
                "create_blog"
            )

        if not category:

            messages.error(
                request,
                "Please select or enter a category."
            )

            return redirect(
                "create_blog"
            )

        if not short_description:

            messages.error(
                request,
                "Please enter a short description."
            )

            return redirect(
                "create_blog"
            )

        if not content:

            messages.error(
                request,
                "Please write some content."
            )

            return redirect(
                "create_blog"
            )

        # CREATE BLOG
        Blog.objects.create(

            title=title,

            category=category,

            short_description=short_description,

            content=content,

            image=image,

            author=request.user.username
        )

        messages.success(
            request,
            "🎉 Your blog has been published successfully!"
        )

        return redirect(
            "my_blogs"
        )

    return render(
        request,
        "blog/create_blog.html"
    )


# =========================================================
# DELETE BLOG
# =========================================================

@login_required
def delete_blog_view(request, blog_id):

    blog = get_object_or_404(
        Blog,
        id=blog_id
    )

    # Security
    if blog.author != request.user.username:

        messages.error(
            request,
            "❌ You are not allowed to delete this blog."
        )

        return redirect(
            "my_blogs"
        )

    # POST
    if request.method == "POST":

        password = request.POST.get(
            "password",
            ""
        )

        user = authenticate(

            username=request.user.username,

            password=password
        )

        if user is not None:

            blog.delete()

            messages.success(
                request,
                "🗑️ Your blog has been deleted successfully."
            )

            return redirect(
                "my_blogs"
            )

        else:

            messages.error(
                request,
                "❌ Incorrect password. Blog was not deleted."
            )

            return render(
                request,
                "accounts/delete_blog.html",
                {
                    "blog": blog
                }
            )

    return render(
        request,
        "accounts/delete_blog.html",
        {
            "blog": blog
        }
    )


# =========================================================
# SAVE / UNSAVE BLOG
# =========================================================

@login_required
@require_POST
def save_blog(request, slug):

    blog = get_object_or_404(
        Blog,
        slug=slug
    )

    saved_blog = SavedBlog.objects.filter(
        user=request.user,
        blog=blog
    ).first()

    # Already saved → UNSAVE
    if saved_blog:

        saved_blog.delete()

        saved = False

    # Not saved → SAVE
    else:

        SavedBlog.objects.create(
            user=request.user,
            blog=blog
        )

        saved = True

    return JsonResponse(
        {
            "success": True,
            "saved": saved
        }
    )


# =========================================================
# SAVED BLOGS
# =========================================================

@login_required
def saved_blogs(request):

    saved_items = SavedBlog.objects.filter(
        user=request.user
    ).select_related(
        "blog"
    ).order_by(
        "-created_at"
    )

    blogs = [
        item.blog
        for item in saved_items
    ]

    return render(
        request,
        "saved_blogs.html",
        {
            "blogs": blogs
        }
    )


# =========================================================
# ADD COMMENT
# =========================================================

@login_required
@require_POST
def add_comment(request, slug):

    blog = get_object_or_404(
        Blog,
        slug=slug
    )

    comment_text = request.POST.get(
        "comment",
        ""
    ).strip()

    if not comment_text:

        return JsonResponse(
            {
                "success": False,
                "message": "Please write a comment."
            },
            status=400
        )

    comments = request.session.get(
        "blog_comments",
        {}
    )

    blog_comments = comments.get(
        slug,
        []
    )

    new_comment = {

        "username":
            request.user.username,

        "comment":
            comment_text,
    }

    blog_comments.append(
        new_comment
    )

    comments[slug] = blog_comments

    request.session["blog_comments"] = comments

    request.session.modified = True

    return JsonResponse(
        {
            "success": True,
            "comment": new_comment,
            "count": len(blog_comments)
        }
    )


# =========================================================
# CONTACT
# =========================================================

from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib import messages


def contact(request):

    if request.method == "POST":

        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        subject = request.POST.get("subject", "").strip()
        message = request.POST.get("message", "").strip()

        # Check empty fields
        if not name or not email or not subject or not message:

            messages.error(
                request,
                "Please fill in all the fields."
            )

            return render(
                request,
                "contact.html"
            )

        try:

            email_subject = f"CodeBlog Contact: {subject}"

            email_body = f"""
New message received from CodeBlog Contact Form

Name: {name}
Email: {email}
Subject: {subject}

Message:
{message}
"""

            mail = EmailMessage(
                subject=email_subject,
                body=email_body,
                from_email=settings.EMAIL_HOST_USER,
                to=["CodeBlog45@gmail.com"],
                reply_to=[email],
            )

            mail.send(fail_silently=False)

            messages.success(
                request,
                "✅ Your message has been sent successfully!"
            )

        except Exception as e:

            print("EMAIL ERROR:", e)

            messages.error(
                request,
                "❌ Something went wrong while sending the message."
            )

        return render(
            request,
            "contact.html"
        )

    return render(
        request,
        "contact.html"
    )
def join_community(request):

    if request.method == "POST":

        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()

        if not name or not email:

            messages.error(
                request,
                "Please fill in all the fields."
            )

            return render(
                request,
                "join_community.html"
            )

        if CommunityMember.objects.filter(email=email).exists():

            messages.warning(
                request,
                "This email is already a community member."
            )

            return render(
                request,
                "join_community.html"
            )

        CommunityMember.objects.create(
            name=name,
            email=email
        )

        messages.success(
            request,
            "🎉 Welcome to CodeBlog Community! You have joined successfully."
        )

        return render(
            request,
            "join_community.html"
        )

    return render(
        request,
        "join_community.html"
    )