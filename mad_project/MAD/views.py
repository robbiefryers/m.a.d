from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication


from django.contrib.auth.models import User, Group 
from models import Categories, Activities, act_day, UserProfile

from MAD.serializers import CategorySerializer, GroupSerializer, ActivitySerializer, UserSerializer, UserLoginSerializer, NewAdminSerializer, ownerSerializer


class login(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        data = request.data
        print data
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid():
            new_data = serializer.data
            return Response(new_data, status=status.HTTP_200_OK) 
        success = {"success": False}
        return Response(success, status=status.HTTP_400_BAD_REQUEST)

class setPassword(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        usr = request.user
        usr.set_password(request.data['passOne'])
        usr.save()
        usrProf = UserProfile.objects.get(user=usr)
        usrProf.firstLogIn = False
        usrProf.save()
        return Response(status=status.HTTP_200_OK)


#View for gathering a list of all activities,
#Authentication required = false, do not need an account to view this information
class activity_list(APIView):
    def get(self, request, format=None):
        acts = Activities.objects.all()
        serializer = ActivitySerializer(acts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)   

#View for gathering a list of all the different categories,
#Authentication required = No, called by categoryModal to display filter options
class category_list(APIView):
    def get(self, request, format=None):
        cats = Categories.objects.all()
        serializer = CategorySerializer(cats, many=True)
        return Response(serializer.data)  


#View to update or remove activity
#Authentication requried = True. Either a user with super or staff privillieges

class ActivityDetail(APIView):
    #permission_classes = (permissions.IsAuthenticated,)
    def get_object(self, pk):
        try:
            return Activities.objects.get(pk=pk)
        except Activities.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        act = self.get_object(pk)
        serializer = ActivitySerializer(act)
        return Response(serializer.data)

    def put(self, request, pk, format=None):

        act = self.get_object(pk)

        serializer = ActivitySerializer(act, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        else:
            return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        act = self.get_object(pk)
        act.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class staff_activiy_list(APIView):

    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, format=None):
        usr = request.user
        print usr

        if usr.groups.filter(name='SuperAdmin').exists() == True:
            print 'super user accessing api'
            acts = Activities.objects.all()
            serializer = ActivitySerializer(acts, many=True)
            return Response(serializer.data) 
        else:
            acts = Activities.objects.filter(owner=usr)
            if acts:
                serializer = ActivitySerializer(acts, many=True)
                return Response(serializer.data) 

        return Response(status=status.HTTP_204_NO_CONTENT)

#another view for super admin only
class newAdmin(APIView):

    permission_classes = (permissions.IsAuthenticated,)
    def post(self, request, format=None):
        usr = request.user
        data = request.data

        if usr.groups.filter(name='SuperAdmin').exists() == True:
            serializer = NewAdminSerializer(data=data)
            
            if serializer.is_valid():
                serializer.save()
                statusData = serializer.data
                newUsr = User.objects.get(username=data.get("username"))
                g = Group.objects.get(name='ActivityAdministrators') 
                g.user_set.add(newUsr)
                UserProfile.objects.create(user=newUsr)
        
                return Response(statusData, status=status.HTTP_200_OK)

            else:
                print 'not valid'
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)


class newEvent(APIView):
    def get(self, request, format=None):
        return Response(status=status.HTTP_200_OK)

    def post(self, request):
        
        serializer = ActivitySerializer(data=request.data)

        if serializer.is_valid():
            print 'so valid'
            serializer.save()
            return Response(serializer.data)

        else:
            return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)

    
