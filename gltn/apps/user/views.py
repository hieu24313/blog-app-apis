from django.contrib.auth import authenticate
from django.db.models import Q
from django.shortcuts import render
from rest_framework import status
from .models import CustomUser
from .serializers import UserSerializer
from ultis.api_helper import api_decorator
from ultis.helper import download_image, CustomPagination

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.hashers import check_password


class RegisterAPIView(APIView):
    @api_decorator
    def post(self, request):
        phone_number = request.data.get('phone_number')
        password = request.data.get('password')

        user, created = CustomUser.objects.get_or_create(phone_number=phone_number)
        if not created:
            # data = UserSerializer(user, context={'request': request}).data
            return {}, 'Phone number has been registered!', status.HTTP_400_BAD_REQUEST
        else:
            user.set_password(password)
            user.save()
            data = UserSerializer(user, context={'request': request}).data
            return data, 'Register Successful!', status.HTTP_201_CREATED


class LoginAPIView(APIView):
    @api_decorator
    def post(self, request):
        phone_number = request.data.get('phone_number')
        password = request.data.get('password')

        user = authenticate(request, phone_number=phone_number, password=password)

        if user:
            data = {
                "id": str(user.id),
                "username": user.phone_number,
                'token': user.token
            }
            return data, 'Login Successful!', status.HTTP_200_OK
        else:
            return {}, 'Invalid credentials', status.HTTP_400_BAD_REQUEST


class UserInfoAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @api_decorator
    def get(self, request):
        data = UserSerializer(request.user, context={'request': request}).data

        return data, 'Retrieve data successfully!', status.HTTP_200_OK


class UpdateUserAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @api_decorator
    def put(self, request):
        # print(request.data)
        user = UserSerializer(request.user, data=request.data, partial=True,
                              context={'request': request})
        if user.is_valid(raise_exception=True):
            user.save()
        return user.data, 'Update user successful!', status.HTTP_200_OK


class AllUserAPIView(APIView):

    @api_decorator
    def get(self, request):
        keyword = request.query_params.get('kw')
        users = CustomUser.objects.filter()
        print(keyword)
        if keyword:
            users = users.filter(Q(full_name__icontains=keyword) | Q(phone_number__icontains=keyword))
        paginator = CustomPagination()
        paginator.add_total_record(len(users))
        result_page = paginator.paginate_queryset(users, request)
        serializer = UserSerializer(result_page, many=True, context={'request': request})
        data = paginator.get_paginated_response(serializer.data).data

        return data, 'Retrieve data successfully!', status.HTTP_200_OK


class ChangePassword(APIView):
    permission_classes = [IsAuthenticated]

    @api_decorator
    def post(self, request):
        current_password = request.data.get('current_password')
        new_password = request.data.get('new_password')
        phone = request.data.get('phone_number')

        user = CustomUser.objects.get(phone_number=phone)
        is_correct_password = check_password(current_password, user.password)

        if is_correct_password:
            user.set_password(new_password)
            user.save()
            return {}, 'Changed password successful!', status.HTTP_200_OK
        else:
            return {}, 'Current password is not correct!', status.HTTP_400_BAD_REQUEST

