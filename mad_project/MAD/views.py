from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_201_CREATED, HTTP_200_OK
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication


from django.contrib.auth.models import User, Group 
from models import Categories, Activities, act_day

from MAD.serializers import CategorySerializer, GroupSerializer, ActivitySerializer, UserSerializer, UserLoginSerializer, NewAdminSerializer


class login(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        data = request.data
        print data
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid():
            new_data = serializer.data
            return Response(new_data, status=HTTP_200_OK)
        success = {"success": False}
        return Response(success, status=HTTP_400_BAD_REQUEST)


#View for gathering a list of all activities,
#Authentication required = false, do not need an account to view this information
class activity_list(APIView):
    def get(self, request, format=None):
        acts = Activities.objects.all()
        serializer = ActivitySerializer(acts, many=True)
        return Response(serializer.data)   

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

        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        act = self.get_object(pk)
        act.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class staff_activiy_list(APIView):

    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, format=None):
        usr = request.user

        if usr.groups.filter(name='SuperAdmin').exists() == True:
            acts = Activities.objects.all()
            serializer = ActivitySerializer(acts, many=True)
            return Response(serializer.data) 
        else:
            return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)
  


    def post(self, request, format=None):
        print request.user
        serializer = ActivitySerializer(data=request.data)
        if serializer.is_valid():
            print serializer['name']
            #serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print 'not valid'
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#another view for super admin only
class newAdmin(APIView):

    permission_classes = (permissions.IsAuthenticated,)
    def post(self, request, format=None):
        usr = request.user
        data = request.data

        if usr.groups.filter(name='SuperAdmin').exists() == True:
            serializer = NewAdminSerializer(data=data)
            print serializer
            
            if serializer.is_valid():
                print 'valid'
                serializer.save()
                statusData = serializer.data
                newUsr = User.objects.get(username=data.get("username"))
                g = Group.objects.get(name='ActivityAdministrators') 
                g.user_set.add(newUsr)
                return Response(statusData, status=HTTP_200_OK)

            else:
                print 'not valid'
                return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

        else:
            return Response(data, status=HTTP_401_UNAUTHORIZED)


class newEvent(APIView):
    def get(self, request, format=None):
        return Response(status=HTTP_200_OK)

    def post(self, request):
        
        serializer = ActivitySerializer(data=request.data)
        print 'blank'
        if serializer.is_valid():
            print 'valid'
            serializer.save()
        else:
            print 'not valid'

        return Response(status=HTTP_200_OK)




    
