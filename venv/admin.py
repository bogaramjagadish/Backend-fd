from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import FAQ
from ckeditor.widgets import CKEditorWidget
from django import forms

class FAQAdminForm(forms.ModelForm):
    class Meta:
        model = FAQ
        fields = '__all__'
        widgets = {
            'answer': CKEditorWidget(), 
        }

class FAQAdmin(admin.ModelAdmin):
    form = FAQAdminForm

    list_display = ('question', 'get_translations', 'id', 'created_at', 'updated_at')
    search_fields = ('question',)
    list_filter = ('created_at', 'updated_at')
    
    fieldsets = (
        (None, {
            'fields': ('question', 'answer')
        }),
        (_('Translations'), {
            'fields': ('question_translated', 'answer_translated')
        }),
    )

    def get_translations(self, obj):
        translations = [
            f"en: {obj.get_translated_question('en')}",
            f"hi: {obj.get_translated_question('hi')}",
            f"bn: {obj.get_translated_question('bn')}",
            f"sw: {obj.get_translated_question('sw')}"
        ]
        return ', '.join(translations)

    get_translations.short_description = _('Translations')

admin.site.register(FAQ, FAQAdmin)
