from rest_framework import serializers
from .models import CustomUser, Blogs


class Rrgistrionsiralizer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'password', 'image']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        print(instance)
        return instance


class Profilesiralizer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'image']


class Blogsiralizer(serializers.ModelSerializer):
    class Meta:
        model = Blogs
        fields = ['title', 'image', 'Nature','Technology', 'Lifestyle', 'Art','username']
        extra_kwargs = {
            'username': {'required': False}
        }
class CustomUserWithBlogsSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='username.username')

    class Meta:
        model = Blogs
        fields = ['id', 'title', 'image', 'username',
                  'Nature', "Technology", 'Lifestyle', 'Art']

  

    def to_representation(self, instance):
        request = self.context.get('request')
        return {
            'blog_id': instance.id,
            'title': instance.title,
            'image': request.build_absolute_uri(instance.image.url),
            'username': instance.username.username,
            "Nature":instance.Nature,
            "Technology":instance.Technology,
            "Lifestyle":instance.Lifestyle,
            "Art":instance.Art,
            "userImage": self.get_user_image_url(instance.username)
        }
    def get_user_image_url(self, user):
        if user.image:
            request = self.context.get('request')
            return request.build_absolute_uri(user.image.url)
        return None


class PasswordSirializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['image']
