from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from .models import FAQ
from .serializers import FAQSerializer
from rest_framework import status
from django.core.cache import cache

class FAQListView(APIView):
    def get(self, request):
        lang = request.GET.get('lang', 'en')
        cache_key = f'faqs_{lang}'
        cached_data = cache.get(cache_key)

        if cached_data:
            return Response(cached_data)

        paginator = PageNumberPagination()
        paginator.page_size = 20

        faqs = FAQ.objects.all().order_by('created_at') 

        for faq in faqs:
            faq.question = faq.get_translated_question(lang)
            faq.answer = faq.get_translated_answer(lang)

        result_page = paginator.paginate_queryset(faqs, request)

        serializer = FAQSerializer(result_page, many=True)
        cache.set(cache_key, serializer.data, timeout=60 * 60)

        return paginator.get_paginated_response(serializer.data)
