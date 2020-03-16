from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView, GenericAPIView,ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import RetrieveDestroyAPIView
from .serializers import UserRegistrationSerializer, UserLoginSerializer, TokenSerializer ,UserDetailsSerializer , ShiftSerializer
from .models import UserInfo , Shift
import datetime
from datetime import timedelta
import json
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated, IsAdminUser

class UserRegistrationAPIView(CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        user = serializer.instance
        token, created = Token.objects.get_or_create(user=user)
        data = serializer.data
        data["token"] = token.key

        headers = self.get_success_headers(serializer.data)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)


class UserLoginAPIView(GenericAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserLoginSerializer
    serializer_class1 = UserDetailsSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.user
            token, _ = Token.objects.get_or_create(user=user)
            try:
                user_details = UserInfo.objects.get(user__username=user)

                permission_dict = {
                    "projectView":False,
                    "projectEdit":False,
                    "projectAdmin":False
                }


                default_permissions = {
                    "V":"projectView",
                    "A": "projectAdmin",
                    "M":"projectEdit"
                }
                permission_dict[default_permissions[user_details.permissions]] = True
                return Response(
                    data={"username":user_details.user.username,
                            "name": user_details.full_name,
                           "projectId": str(user_details.project).lower().replace(" ", "_"),
                           "projectName": user_details.project,
                           "permissions" : permission_dict,
                          "Token": TokenSerializer(token).data},
                    status=status.HTTP_200_OK,
                )
            except:
                return Response(
                    data={
                    "Token": TokenSerializer(token).data},
                    status=status.HTTP_200_OK,
                )
        else:
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )



class UserTokenAPIView(RetrieveDestroyAPIView):
    lookup_field = "key"
    serializer_class = TokenSerializer
    queryset = Token.objects.all()

    def filter_queryset(self, queryset):
        return queryset.filter(user=self.request.user)

    def retrieve(self, request, key, *args, **kwargs):
        if key == "current":
            instance = Token.objects.get(key=request.auth.key)
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        return super(UserTokenAPIView, self).retrieve(request, key, *args, **kwargs)

    def destroy(self, request, key, *args, **kwargs):
        if key == "current":
            Token.objects.get(key=request.auth.key).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return super(UserTokenAPIView, self).destroy(request, key, *args, **kwargs)


# class UserDetailsAPIView(GenericAPIView):
#     authentication_classes = ()
#     permission_classes = ()
#     serializer_class = UserLoginSerializer
#
#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.user
#             return Response(
#                 # data=TokenSerializer(token).data,
#                 status=status.HTTP_200_OK,
#             )
#         else:
#             return Response(
#                 data=serializer.errors,
#                 status=status.HTTP_400_BAD_REQUEST,
#             )
#


class UserListCreateAPIView(ListCreateAPIView, RetrieveUpdateDestroyAPIView):
    serializer_class = UserDetailsSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return UserInfo.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ShiftScheduleListCreateAPIView(ListCreateAPIView):
    serializer_class = ShiftSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Shift.objects.filter(user=self.request.user).order_by('date')

    def perform_create(self, serializer):
        user = self.request.data['user']['username']
        serializer.save(user=user)


@api_view(['GET'])
@permission_classes([IsAuthenticated,])
def shift_schedule_view(request):
    try:
        p = User.objects.get(username=request.user)
        p = Shift.objects.filter(user__username=p)
    except Exception as e:
        Response(status.HTTP_404_NOT_FOUND)

    if request.method=="GET":
        data = []
        for i in p:
             data.append({
                "user": i.user.username,
                "date": i.date
                })
        return  Response(data)
    else:
        Response(status.HTTP_404_NOT_FOUND)


@api_view(["GET","POST"])
@permission_classes([IsAuthenticated])
def user_info_with_shifts(request):
    shifts_dict = {
        'M': "MorningShift",
        'A': "AfternoonShift",
        "N": "NightShift",
        "G": "GeneralShift",
        "L": "Leave"
    }

    if request.method=='GET':
        print(request.user)
        try:
            query_set = UserInfo.objects.get(user__username=request.user)
        except:
            return Response({'responce':'we didnt find the authorised user info'})
        serialiser = UserDetailsSerializer(query_set)
        try:
            p = Shift.objects.filter(user=request.user, date__gte=datetime.date.today(), date__lte=(datetime.date.today() +timedelta(days = 7)))
        except Exception as e:
            Response(status.HTTP_404_NOT_FOUND)

        data = []
        for i in p:
            shift = {
                "Date": "",
                "MorningShift": False,
                "AfternoonShift": False,
                "NightShift": False,
                "GeneralShift": False,
                "Leave": False
            }
            shift["Date"] =  i.date
            shift[shifts_dict[i.shift]] = True
            data.append(shift)
            del shift
        return  Response({
            "user_info": serialiser.data,
            "shifts":data})



    elif request.method == "POST":
        try:
            temp_user = UserInfo.objects.get(user=request.user)
        except:
            return Response({'responce':'User need to get the access as Manager '})
        # print(temp_user.permissions)
        try:
            if temp_user.permissions=='M':
                data = request.data
                # print(request.data)
                list = []
                responce = {}
                for i in data:
                    try:
                        user = UserInfo.objects.get(user__username=i['user'])
                        if user.project!=temp_user.project:
                            responce[i['user']] = "You can't change other project Peoples( "+i['user']+" )shifts."
                            continue
                        y,m,d = str(i['date']).split('-')
                        if datetime.date.today() <= datetime.date(int(y),int(m),int(d)):
                            temp = Shift(user=i['user'], date=i['date'], shift=i['shift'])
                            try:
                                temp.save()
                                list.append(temp)
                                responce[i['user']] = i['user'] + " Shift details are inserted."
                            except:
                                responce[i['user']] = i['user'] + " Shift details are already existed."
                                continue
                        else:
                            responce[i['user']] = i['date'] + " Wrong Date. Please select Future date."

                    except:
                        continue
                return Response(data=responce, status=status.HTTP_200_OK)
            else:
                return Response(data={'Message': "You don't have permissions to edit"},status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response(data={'Error':e },status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def shifts_info_user(request,project_id,dd,mm,yyyy):
    if request.method == "GET":
        print(project_id,dd,mm,yyyy)
        try:
            a = UserInfo.objects.filter(project=project_id)
        except:
            return Response(data={'data':"Invalid project id"})
        users = []
        info={
            "MorningShift" :[],
            "AfternoonShift": [],
            "NightShift" :[],
            "GeneralShift" :[],
            "Leave":[]
        }
        print(a)
        for i in a:
            users.append(i.user.username)
        for j in users:
            try:
                d = datetime.date(int(yyyy),int(mm),int(dd))
                b =Shift.objects.filter(user=j,date=d)
                for k in b:
                    print(k.user)
                    print(k.shift)
                    if(k.shift == "M"):
                        info["MorningShift"].append(UserInfo.objects.get(user__username=k.user).full_name)
                    if (k.shift == "A"):
                        info["AfternoonShift"].append(UserInfo.objects.get(user__username=k.user).full_name)
                    if (k.shift == "N"):
                        info["NightShift"].append(UserInfo.objects.get(user__username=k.user).full_name)
                    if (k.shift == "G"):
                        info["GeneralShift"].append(UserInfo.objects.get(user__username=k.user).full_name)
                    if (k.shift == "L"):
                        info["Leave"].append(UserInfo.objects.get(user__username=k.user).full_name)

            except:
                pass
            data = {
                "projectId" : project_id,
                "projectName": str(project_id).replace("_"," "),
                'date': str(d),
                "shifts": info
            }

        # data = request.d
        return Response(data=data,status=status.HTTP_200_OK)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_shift(request,user_id,dd,mm,yyyy):
    if request.method == "GET":
        print(user_id,dd,mm,yyyy)
        try:
            a = UserInfo.objects.get(user__username=user_id)
        except:
            return Response(data={'data':"Invalid User"})

        shifts_dict = {
            'M': "MorningShift",
            'A': "AfternoonShift",
            "N": "NightShift",
            "G": "GeneralShift",
            "L": "Leave"
        }

        print(a.user.username)
        d = datetime.date(int(yyyy),int(mm),int(dd))
        b =Shift.objects.get(user=a.user.username,date=d)
        data = {"currentShift":shifts_dict[b.shift]}
        # data = request.d
        return Response(data=data,status=status.HTTP_200_OK)



@api_view(["GET"])
@permission_classes([IsAuthenticated])
def users_project_shift(request,project_id,shift_name,dd,mm,yyyy):
    if request.method == "GET":
        # print(user_id,dd,mm,yyyy)
        try:
            a = UserInfo.objects.filter(project=project_id)
        except:
            return Response(data={'data':"Invalid Project"})
        persons = []
        print(a)
        for i in a:
            try:
                d = datetime.date(int(yyyy), int(mm), int(dd))
                b = Shift.objects.get(user=i.user.username,shift=shift_name, date=d)
                persons.append(b.user)
                print(b.user)
            except:
                pass
        data = {"persons": persons}
        # data = request.d
        return Response(data=data,status=status.HTTP_200_OK)

class UserDetailAPIView(RetrieveUpdateDestroyAPIView):
    lookup_field = "key"
    serializer_class = UserDetailsSerializer

    def get_queryset(self):
        return UserInfo.objects.filter(user=self.request.user)

