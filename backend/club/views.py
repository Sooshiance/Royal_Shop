from rest_framework.views import APIView
from rest_framework import permissions, status, response

from .serializers import RateSerializer, CommentSerializer
from .services import RateService, CommentService
