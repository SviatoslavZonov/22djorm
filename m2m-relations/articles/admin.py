from django.contrib import admin

from django.forms import BaseInlineFormSet
from .models import Article, Tag, Scope
from django.core.exceptions import ValidationError


class ScopeInlineFormset(BaseInlineFormSet):
    def clean(self):
        main_tags = 0
        for form in self.forms:
            if form.cleaned_data != {}:
                main_tags += form.cleaned_data['is_main']
            if main_tags > 1:
                raise ValidationError('Главный тег должен быть один.')
                break
        return super().clean()


class ScopeInline(admin.TabularInline):
    model = Scope
    formset = ScopeInlineFormset


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [ScopeInline]
    pass


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    inlines = [ScopeInline]
