from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response

from .models import FAQ
from .serializers import FAQSerializer


def home(request):
    return render(request, 'home.html')

# Create your views here.

class FAQViewSet(viewsets.ModelViewSet):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['lang'] = self.request.query_params.get('lang', 'en')
        return context

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        lang = request.query_params.get('lang', 'en')
        serializer = self.get_serializer(queryset, many=True, context={'lang': lang})
        return Response(serializer.data)
