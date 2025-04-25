from django.contrib import admin
from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from django import forms


class Blog(models.Model):
    title = models.CharField(max_length=100, verbose_name="Заголовок")
    description = models.TextField(verbose_name="Краткое содержание")
    content = models.TextField(verbose_name="Полное содержание")
    posted = models.DateTimeField(default=timezone.now, db_index=True, verbose_name="Опубликована")
    pub_date = models.DateTimeField(default=timezone.now, verbose_name="Дата публикации")
    image = models.FileField(default = 'temp.jpg', verbose_name = "Путь")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор", blank=True, null=True)

    def get_absolute_url(self):
        return reverse("blogpost", args=[str(self.id)])

    def __str__(self):
        return self.title

    class Meta:
        db_table = "Posts"
        ordering = ["-posted"]
        verbose_name = "статья блога"
        verbose_name_plural = "статьи блога"

class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'pub_date', 'author')
    search_fields = ('title', 'content', 'author__username', 'author__first_name', 'author__last_name')
    list_filter = ('pub_date', 'author')
    date_hierarchy = 'pub_date'
    prepopulated_fields = {'description': ('title',)}
    readonly_fields = ('pub_date',)
    ordering = ('-posted',)


    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'content', 'image', 'author', 'pub_date')
        }),
    )

admin.site.register(Blog, BlogAdmin)

class Comment(models.Model):
    post = models.ForeignKey(Blog, on_delete=models.CASCADE, verbose_name="Статья")
    text = models.TextField(verbose_name = "Текст комментария")
    date = models.DateTimeField(default = timezone.now, verbose_name = "Дата комментария")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор", blank=True, null=True)

    def __str__(self):
        return self.text

    class Meta:
        db_table = "Comments"
        verbose_name = "комментарий"
        verbose_name_plural = "комментарии"

class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'date')
    search_fields = ('author', 'text', 'title')
    list_filter = ('date', 'post')
    date_hierarchy = 'date'
    readonly_fields = ('date',) 
    ordering = ('-date',)

    fieldsets = (
        (None, {
            'fields': ('post', 'author', 'text', 'date')
        }),
    )

admin.site.register(Comment, CommentAdmin)