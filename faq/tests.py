from django.test import TestCase
from .models import FAQ
from django.core.cache import cache

class FAQModelTest(TestCase):
    def setUp(self):
        self.faq = FAQ.objects.create(
            question="HI How are you ?",
            answer="Hello world",
        )

    def test_faq_creation(self):
        self.assertEqual(self.faq.question, "HI How are you ?")
        self.assertEqual(self.faq.answer, "Hello world")

    def test_translation(self):
        translated_question = self.faq.get_translated_question('hi')
        translated_answer = self.faq.get_translated_answer('hi')
        self.assertIn('hi', self.faq.question_translated)
        self.assertIn('hi', self.faq.answer_translated)
        self.assertEqual(translated_question, "HI How are you ?")

    def test_cache_after_save(self):
        cache_key = f"faq:{self.faq.pk}"
        cached_data = cache.get(cache_key)
        self.assertIsNotNone(cached_data)
        self.assertEqual(cached_data['question'], "HI How are you ?")
        self.assertEqual(cached_data['answer'], "Hello world")

    def test_cache_expiration(self):
        cache_key = f"faq:{self.faq.pk}"
        cache.set(cache_key, {'question': 'Test', 'answer': 'Answer'}, timeout=1)
        from time import sleep
        sleep(2)
        cached_data = cache.get(cache_key)
        self.assertIsNone(cached_data)

    def test_str_method(self):
        self.assertEqual(str(self.faq), "HI How are you ?")
