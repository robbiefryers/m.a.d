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


    def update(self, instance, validated_data):
        
        #Update and return an existing `activity` instance, given the validated data.
       
        instance.name = validated_data.get('name', instance.name)
        instance.venue = validated_data.get('venue', instance.venue)
        instance.postcode = validated_data.get('postcode', instance.postcode)
        instance.agesLower = validated_data.get('agesLower', instance.agesLower)
        instance.agesUpper = validated_data.get('agesUpper', instance.agesUpper)
        instance.contactName = validated_data.get('contactName', instance.contactName)
        instance.contactEmail = validated_data.get('contactEmail', instance.contactEmail)
        instance.number = validated_data.get('number', instance.number)
        instance.special = validated_data.get('special', instance.special)
        instance.save()

        act = Activities.objects.get(pk=instance.pk)
        days = act_day.objects.filter(act=act)
        cats = act_cat.objects.filter(act=act)

        # Create or update page instances that are in the request and add the days to the updatedDays
        updatedDays = []
        for item in validated_data['days']:
            updatedDays.append(item['day'])

            #check if the same day is in the modified data, if it is check if the times have changed and update them
            try:
                sameDay = days.get(act=act, day= item['day'])
                if sameDay.startTime==item['startTime'] and sameDay.endTime==item['endTime']:
                    #no change necessary as same as before
                    pass
                
                else:
                    sameDay.startTime = item['startTime']
                    sameDay.endTime = item['endTime']
                    sameDay.save()

            except:
                newDay = act_day(act=act, day=item['day'], startTime=item['startTime'], endTime=item['endTime'])
                newDay.save()
        
        # Delete any pages not included in the request
        for d in days:
            if d.day not in updatedDays:
                d.delete()
                print 'deleted'

        # Create or update category instances that are in the request
        updatedCats = []
        for item in validated_data['cats']:
            updatedCats .append(item['cat']['name'])
            try:
                print item['cat']['name']
                sameCat = cats.get(cat__name=item['cat']['name'])            
                print 'found'

            except:
                print 'adding cat'
                newCat = Categories.objects.get(name=item['cat']['name'])
                newEventCat = act_cat(act=act, cat=newCat)
                newEventCat.save()

        # Delete any categories not included in the request
        for c in cats:
            if c.cat.name not in updatedCats:
                c.delete()


        return instance





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