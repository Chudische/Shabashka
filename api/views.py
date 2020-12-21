import json
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_405_METHOD_NOT_ALLOWED
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_403_FORBIDDEN, HTTP_202_ACCEPTED

from main.models import Offer, Comment, ShaUser
from .serializers import OfferSerializer, OfferDetailSerializer, CommentSerializer

@api_view(['GET'])
def offers(request):
    if request.method == "GET":
        offers = Offer.objects.filter(is_active=True)[:30]
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
        if not request.data:
            return Response({"error": "No data found"}, HTTP_400_BAD_REQUEST)
        offer_comments = Comment.objects.filter(offer=offer)
        if request.data['status'] == 'accepted':
            winner_id = int(request.data["winner"])
            winner = ShaUser.objects.get(pk=winner_id)
            offer.status = 'a'
            offer.winner = winner
            offer.is_active = False
            offer.save()
            offer_comments.exclude(author=winner).update(is_active=False) 
        elif request.data['status'] == 'canceled':
            offer.status = 'n'
            offer.winner = None
            offer.is_active = True
            offer.save()           
            offer_comments.update(is_active=True)      
        else:
            return Response({"error": "No data found"}, HTTP_400_BAD_REQUEST)
        return Response({'status': 'ok'}, HTTP_202_ACCEPTED)
    else:
        return Response({'status': 'error', 'error': 'method not allowed'}, HTTP_405_METHOD_NOT_ALLOWED)

@api_view(["PUT"])
def favorive(request):   
    if request.method == "PUT":        
        try:
            user = ShaUser.objects.get(pk=request.user.id)
        except ShaUser.DoesNotExist:
            return Response({"error": "Forbitten"}, HTTP_403_FORBIDDEN)
        if not request.data:
            return Response({"error": "No data found"}, HTTP_400_BAD_REQUEST)
        if request.data["user_id"]:
            try:
                favorite = ShaUser.objects.get(pk=request.data["user_id"])
            except ShaUser.DoesNotExist:
                return Response({"error": "Can't add user to favorite. User does not exist"}, HTTP_400_BAD_REQUEST)
            if user.favorite.filter(pk=favorite.pk):
                user.favorite.remove(favorite)
                user.save()                
                return Response({'status': 'ok', 'message': 'removed'}, HTTP_202_ACCEPTED)
            else:
                user.favorite.add(favorite)
                user.save()
                return Response({'status': 'ok', 'message': 'added'}, HTTP_202_ACCEPTED)
            
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
        