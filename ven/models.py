from django.db import models
from ckeditor.fields import RichTextField
from django.core.cache import cache
from googletrans import Translator

class FAQ(models.Model):
    LANGUAGE_CHOICES = [
        ('en', 'English'),
        ('hi', 'Hindi'),
        ('bn', 'Bengali'),
    ]

    # Base fields (English)
    question = models.TextField()
    answer = RichTextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Translations
    question_hi = models.TextField(blank=True, null=True)
    answer_hi = RichTextField(blank=True, null=True)
    question_bn = models.TextField(blank=True, null=True)
    answer_bn = RichTextField(blank=True, null=True)

    class Meta:
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"
        ordering = ['-created_at']

    def __str__(self):
        return self.question[:50]

    def get_translated_field(self, field_name, lang):
        """Get translated text for a given field and language."""
        if lang == 'en':
            return getattr(self, field_name)
        
        cache_key = f'faq_{self.id}_{field_name}_{lang}'
        cached_value = cache.get(cache_key)
        
        if cached_value:
            return cached_value

        translated_field = f'{field_name}_{lang}'
        if hasattr(self, translated_field) and getattr(self, translated_field):
            translated_text = getattr(self, translated_field)
        else:
            # Fallback to translation API
            translator = Translator()
            original_text = getattr(self, field_name)
            try:
                translated_text = translator.translate(
                    original_text,
                    dest=lang
                ).text
                setattr(self, translated_field, translated_text)
                self.save()
            except Exception:
                return getattr(self, field_name)  # Fallback to English

        cache.set(cache_key, translated_text, timeout=86400)  # Cache for 24 hours
        return translated_text

    def get_question(self, lang='en'):
        """Get translated question."""
        return self.get_translated_field('question', lang)

    def get_answer(self, lang='en'):
        """Get translated answer."""
        return self.get_translated_field('answer', lang)
