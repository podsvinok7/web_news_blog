from rest_framework import serializers
from .models import Article, Comment

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'title', 'text', 'category', 'created_date', 'user']
        read_only_fields = ['created_date', 'id']
    
    def validate_title(self, value):
        if len(value) < 5:
            raise serializers.ValidationError("Заголовок должен быть не менее 5 символов")
        return value
    
    def validate_text(self, value):
        if len(value) < 10:
            raise serializers.ValidationError("Содержание должно быть не менее 10 символов")
        return value

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['id']
