from rest_framework import serializers  # 引入序列化模块
from rest_framework.exceptions import ValidationError

from .models import Book


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"

    @staticmethod
    def validate_price(price):
        if price < 10:
            raise ValidationError('price should > 10')
        return price
