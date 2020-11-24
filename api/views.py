import json
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_405_METHOD_NOT_ALLOWED
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_403_FORBIDDEN, HTTP_202_ACCEPTED

from main.models import Offer, Comment
from .serializers import OfferSerializer, OfferDetailSerializer, CommentSerializer

@api_view(['GET'])
def offers(request):
    if request.method == "GET":
        offers = Offer.objects.filter(is_active=True)[:10]
        serializer = OfferSerializer(offers, many=True)
        return Response(serializer.data)


@api_view(["PUT"])
def offer_status(request, pk):
    if request.method == 'PUT':        
        try:
            offer = Offer.objects.get(pk=pk)
        except Offer.DoesNotExist:
            return Response({'error': 'Offer does not exist'}, HTTP_404_NOT_FOUND)        
        if request.user != offer.author:
            return Response({"error": "Forbitten"}, HTTP_403_FORBIDDEN)
        elif not request.data:
            return Response({"error": "No data found"}, HTTP_400_BAD_REQUEST)
        winner = request.data["winner"]
        offer.status = 'a'
        offer.save()
        Comment.objects.filter(offer=offer).exclude(pk=winner).update(is_active=False)           
        return Response({'status': 'ok'}, HTTP_202_ACCEPTED)
    else:
        return Response({'status': 'error', 'error': 'method not allowed'}, HTTP_405_METHOD_NOT_ALLOWED)



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
        