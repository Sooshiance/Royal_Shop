from rest_framework import permissions, generics

from .services import RateService, CommentService
from .serializers import RateSerializer, CommentSerializer

from store.repositories import ProductRepository


class RateListView(generics.ListAPIView):
    serializer_class = RateSerializer

    def get_queryset(self):
        product_id = self.kwargs['product_id']
        product = ProductRepository.get_product_by_id(product_id)
        rate = RateService.read_all_rate_of_product(product)
        return rate


class RateCreateView(generics.CreateAPIView):
    serializer_class = RateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        product_id = self.kwargs['product_id']
        product = ProductRepository.get_product_by_id(product_id)
        serializer.save(user_profile=self.request.user, product=product)


class CommentListView(generics.ListAPIView):
    queryset = CommentService.get_all_comments()
    serializer_class = CommentSerializer


class CommentCreateView(generics.CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user_profile=self.request.user)


class CommentUpdateView(generics.UpdateAPIView):
    queryset = CommentService.get_all_comments()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        serializer.save(user_profile=self.request.user)


class CommentDeleteView(generics.DestroyAPIView):
    queryset = CommentService.get_all_comments()
    permission_classes = [permissions.IsAuthenticated]
