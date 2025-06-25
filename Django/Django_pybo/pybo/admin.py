from django.contrib import admin

# Register your models here.
# https://docs.djangoproject.com/en/4.0/ref/contrib/admin/

from .models import Question, Answer

class QuestionAdmin(admin.ModelAdmin):
    search_fields = ['subject']

admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)