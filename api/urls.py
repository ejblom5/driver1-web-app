from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
#router.register(r'drivers', views.DriverViewSet, basename='DriverView')
#router.register(r'drivers/<int:driver_id>', views.DriverDetail.as_view()),



# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('drivers/', views.driver_list),
    path('drivers/<int:pk>', views.DriverDetail.as_view()),
    path('sponsors/', views.SponsorList.as_view()),
    path('sponsors/<int:pk>', views.SponsorDetail.as_view()),
    path('authenticate', views.authenticate_driver)
]
