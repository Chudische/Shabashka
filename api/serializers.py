from rest_framework import serializers

from main.models import Offer, Comment

class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = ('id', 'title', 'content', 'price', 'created')
        

class OfferDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = ('id', 'title', 'content', 'price', 'created', 'image', 'author', 'reviews', 'shared')


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('offer', 'author', 'content', 'created', 'price', 'time_amount', 'measure')
