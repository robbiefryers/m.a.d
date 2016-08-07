from django.contrib.auth.models import User, Group
from rest_framework import serializers
from models import Categories, Activities, act_day, act_cat
from django.contrib.auth.models import User, Group 
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token


class UserLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    token = serializers.CharField(allow_blank = True, read_only=True)
    userGroup = serializers.CharField(allow_blank = True, read_only=True)
    success = serializers.BooleanField(default=False)
    usr_obj=None
    class Meta:
        model = User
        fields = ('username', 'password', 'token', 'userGroup', 'success')
        extra_kwargs = {'password': {"write_only": True}}

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")
 
        if not username:
            raise serializers.ValidationError("No username given")

        try:
            usr_obj = User.objects.get(username=username)

        except User.DoesNotExist:
            raise serializers.ValidationError("No user with that name registered")

        #Check if usr_obj is set to a User object and then check is posted password matches
        if usr_obj:
            if not usr_obj.check_password(password):
                raise serializers.ValidationError("Incorrect Password")

            #Will get to here if there are no validation errors,
            #assign the users token and their privillege group to the response
            data['token'] = Token.objects.get(user=usr_obj)
            data['userGroup'] = usr_obj.groups.get()
            data['success'] = True
        
        return data

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

class UserSerializer(serializers.ModelSerializer):
    acs = serializers.PrimaryKeyRelatedField(many=True, queryset = Activities.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'acs')

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')

class NewAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields=('username', 'password')

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")
        usr_obj = None

        if not username:
            print 'no username'
            raise serializers.ValidationError("Blank username or password")
        if not password:
            print 'no username'
            raise serializers.ValidationError("Blank password")

        try:
            usr_obj = User.objects.get(username=username)

        except User.DoesNotExist:
            data['username'] = username
            data['password'] = password

        if usr_obj:
            raise serializers.ValidationError("Already a user with that username")
            print 'already user'

        return data

    def create(self, validated_data):
        user = User(username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        return user