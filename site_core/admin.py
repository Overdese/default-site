from django.contrib import admin
from models import Post, Category, Page, Parameter


class AdminPost(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('title', 'post_date', 'body', 'tags', 'categories')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('description', 'keywords', 'published', 'attached')
        }),
    )

    list_display = ('title', 'published', 'attached', 'post_date')
    search_fields = ('title', 'body')
    date_hierarchy = 'post_date'

    def save_model(self, request, obj, form, change):

        super(AdminPost, self).save_model(request, obj, form, change)
        obj.author = request.user.username
        obj.save()


class AdminPage(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('title', 'post_date', 'body', 'parent_page', 'priority')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('description', 'keywords', 'published', 'in_menu')
        }),
    )


class AdminCategory(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('name', 'priority',)
        }),
    )

class AdminParametr(admin.ModelAdmin):
    list_display = ('name', 'value', 'enable')


admin.site.register(Post, AdminPost)
admin.site.register(Category, AdminCategory)
admin.site.register(Page, AdminPage)
admin.site.register(Parameter, AdminParametr)