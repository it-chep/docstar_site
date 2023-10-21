from rest_framework import serializers
from docstar_site.models import Doctor


# class DoctorModel:
#     def __init__(self, name, inst_url):
#         self.name = name
#         self.inst_url = inst_url


# class DoctorSerializer(serializers.ModelSerializer):
#     name = serializers.CharField(max_length=255)
#     inst_url = serializers.CharField()
#     slug = serializers.CharField(max_length=225, )
#     email = serializers.CharField(max_length=100, )
#     vk_url = serializers.CharField(max_length=100)
#     dzen_url = serializers.CharField(max_length=100)
#     tg_url = serializers.CharField(max_length=100)
#     city = serializers.CharField()
#     medical_directions = serializers.CharField(max_length=100)
#     speciallity = serializers.CharField()
#     additional_speciallity = serializers.CharField(max_length=100)
#     main_blog_theme = serializers.CharField(max_length=100)
#     status_club = serializers.CharField(default=True)
#
#     def create(self, validated_data):
#         return Doctor.objects.create(**validated_data)
#
#     class Meta:
#         model = Doctor
#         fields = ('name', 'inst_url')
#
#
