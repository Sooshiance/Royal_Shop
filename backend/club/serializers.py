from rest_framework import serializers

from .models import Rate, Comment


class RateSerializer(serializers.ModelSerializer):
    user_profile = serializers.StringRelatedField(read_only=True)
    product = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Rate
        fields = [
            'pk',
            'user_profile',
            'product',
            'vote',
            'txt',
            'each_product_rate',
        ]
    
    def validate(self, attrs):
        vote = attrs.get("vote")
        if vote < 1 or vote > 5:
            raise serializers.ValidationError("must be between 1 and 5")
        return attrs


class CommentSerializer(serializers.ModelSerializer):

    user_profile = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = [
            'pk',
            'user_profile',
            'txt',
            'status',
        ]
