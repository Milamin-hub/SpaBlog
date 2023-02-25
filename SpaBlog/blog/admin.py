from django.contrib import admin
from . import models


@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    list_filter = ('status', 'created', 'publish', 'author')    
    search_fields = ('title', 'body')    
    prepopulated_fields = {'slug': ('title',)}    
    raw_id_fields = ('author',)    
    date_hierarchy = 'publish'    
    ordering = ('status', 'publish')


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin): 
    list_display = ('author', 'email', 'post', 'created', 'active') 
    list_filter = ('active', 'created', 'updated') 
    search_fields = ('author', 'email', 'body') 


@admin.register(models.PostFile)
class PostfileAdmin(admin.ModelAdmin): 
    list_display = ('post', 'file')