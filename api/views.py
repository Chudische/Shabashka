from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from main.models import Offer, Comment
from .serializers import OfferSerializer, OfferDetailSerializer, CommentSerializer

@api_view(['GET'])
def offers(request):
    if request.method == "GET":
        offers = Offer.objects.filter(is_active=True)[:10]
        serializer = OfferSerializer(offers, many=True)
        return Response(serializer.data)


class OfferDetailView(RetrieveAPIView):
    queryset = Offer.objects.filter(is_active=True)
    serializer_class = OfferDetailSerializer


@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticatedOrReadOnly,))
def comments(request, pk):
    if request.method == 'POST':
        serializer = CommentSerializer(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, HTTP_201_CREATED)
        else:
            return Response(serializer.errors, HTTP_400_BAD_REQUEST)
    else:
        comments = Comment.objects.filter(is_active=True, offer=pk)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
        