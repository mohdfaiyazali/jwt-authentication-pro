from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)
from .views import home_view, login_page, register_page, tasks_page


urlpatterns = [
    path('', home_view, name='home'),
    path('login/', login_page, name='login-page'),
    path('register/', register_page, name='register-page'),
    path('tasks/', tasks_page, name='tasks-page'),

    path('admin/', admin.site.urls),

    path('api/', include('accounts.urls')),
    path('api/', include('tasks.urls')),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),

    path(
        'api/docs/',
        SpectacularSwaggerView.as_view(url_name='schema'),
        name='swagger-ui',
    ),

]
