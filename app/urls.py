from django.urls import path

from app import views

urlpatterns = [
    path('create_checks/', views.CheckCreateView.as_view()),
    # path('create_item/', views.ItemCreateView.as_view()),
    path('new_checks/', views.CheckNewStatusRetreiveView.as_view()),
    path('check/', views.CheckPDFView.as_view())
]
