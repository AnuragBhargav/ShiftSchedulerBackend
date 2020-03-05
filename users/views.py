from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView, GenericAPIView,ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import RetrieveDestroyAPIView
from .serializers import UserRegistrationSerializer, UserLoginSerializer, TokenSerializer ,UserDetailsSerializer , ShiftSerializer
from .models import UserInfo , Shift
import datetime
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

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.user
            token, _ = Token.objects.get_or_create(user=user)
            return Response(
                data=TokenSerializer(token).data,
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
        "G": "GeneralShift"
    }

    if request.method=='GET':
        print(request.user)
        try:
            query_set = UserInfo.objects.get(user__username=request.user)
        except:
            return Response({'responce':'we didnt find the authorised user info'})
        serialiser = UserDetailsSerializer(query_set)
        try:
            p = Shift.objects.filter(user=request.user)
        except Exception as e:
            Response(status.HTTP_404_NOT_FOUND)
        if request.method=="GET":
            data = []
            for i in p:
                shift = {
                    "Date": "",
                    "MorningShift": False,
                    "AfternoonShift": False,
                    "NightShift": False,
                    "GeneralShift": False
                }
                shift["Date"] =  i.date
                shift[shifts_dict[i.shift]] = True
                data.append(shift)
                del shift
            return  Response({
                "user_info": serialiser.data,
                "shifts":data})
        else:
            Response(status=status.HTTP_404_NOT_FOUND)


    elif request.method == "POST":
        try:
            temp_user = UserInfo.objects.get(user=request.user)
        except:
            return Response({'responce':'User need to get the access as Manager '})
        print(temp_user.permissions)
        try:
            if temp_user.permissions=='M':
                data = request.data
                print(request.data)
                list = []
                responce = {}
                for i in data:
                    try:
                        UserInfo.objects.get(user__username=i['user'])
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




# class UserDetailAPIView(RetrieveUpdateDestroyAPIView):
#     lookup_field = "key"
#     serializer_class = UserDetailsSerializer
#
#     def get_queryset(self):
#         return UserInfo.objects.filter(user=self.request.user)

