from django.urls import path
from courseRS import views

urlpatterns = [
    path('user/', views.UserList.as_view()),
    path('user/<int:pk>', views.UserDetail.as_view()),
    path('college/', views.CollegeList.as_view()),
    path('college/<int:pk>', views.CollegeDetail.as_view()),
    path('course/', views.CourseList.as_view()),
    path('course/<int:pk>', views.CourseDetail.as_view()),
    path('selectionlog/', views.SelectionLogList.as_view()),
    path('selectionlog/<int:pk>', views.SelectionLogDetail.as_view()),
]
