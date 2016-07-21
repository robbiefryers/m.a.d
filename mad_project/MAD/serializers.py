from django.contrib.auth.models import User, Group
from rest_framework import serializers
from models import Categories, Activities, act_day, act_cat


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ('name',)


class dayTimeSerializer(serializers.ModelSerializer):
    class Meta:
    	model = act_day
        fields = ('day', 'startTime', 'endTime')


class actCatSerializer(serializers.ModelSerializer):
    catName = CategorySerializer(source='cat')
    class Meta:
        model = act_cat
        fields = ('catName',)


class ActivitySerializer(serializers.ModelSerializer):
    days = dayTimeSerializer(many=True)
    cats = actCatSerializer(many=True)

    class Meta:
        model = Activities
        fields = ('name', 'venue', 'postcode', 'agesLower', 'agesUpper', 'contactName',
        	'contactEmail', 'number', 'special', 'days', 'cats')



class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')