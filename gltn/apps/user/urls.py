from django.urls import path
from .views import RegisterAPIView, LoginAPIView, UserInfoAPIView, UpdateUserAPIView, AllUserAPIView, ChangePassword
from .admin import admin_site

urlpatterns = [
    path('register/', RegisterAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('user/detail/', UserInfoAPIView.as_view()),
    path('user/update/', UpdateUserAPIView.as_view()),
    path('user/all/', AllUserAPIView.as_view()),
    path('user/update/password/', ChangePassword.as_view()),
    path('admin/', admin_site.urls),

]