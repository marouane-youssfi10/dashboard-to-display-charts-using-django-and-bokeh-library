from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('chart/', views.chart, name='chart'),
    path('about/', views.about, name='about'),
    path('chart/create_order/', views.create_order, name='create_order'),
    path('chart/update_order/<str:pk>', views.update_order, name='update_order'),
    path('chart/delete_order/<str:pk>', views.delete_order, name='delete_order'),

]

