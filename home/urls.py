from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create/',views.create,name="create"),
    path('<int:question_id>/', views.detail, name='detail'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
]