from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import  TokenObtainPairView,TokenRefreshView

from setting.views import ExcelImportViewSet, getProfile, updateProfile

router = routers.DefaultRouter()
router.register(r"upload", ExcelImportViewSet, basename="upload")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("setting/", include(router.urls)),
    path("api/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/login/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("profile/", getProfile, name="profile"),
    path("profile/update/", updateProfile, name="update-profile"),
]
