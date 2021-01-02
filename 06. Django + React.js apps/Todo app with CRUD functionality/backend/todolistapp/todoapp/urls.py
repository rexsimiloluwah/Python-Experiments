from django.urls import path
from .views import TodoView, TodoDetailView

urlpatterns = [

    path('tasks', TodoView.as_view()),
    path('tasks/<int:id>', TodoDetailView.as_view()), 
    
    
]