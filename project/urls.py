from django.urls import path
from project import views

urlpatterns = [
    path('348/', views.say_Hello),
    path('find-courses/', views.course_list),
    path('find-players/', views.player_list_age),
    path('player-directory/', views.player_direct),
    path('tee-times/', views.tee_time_directory),
    path('add_g/', views.add_person),
    path('add_c/', views.add_golf_course),
    path('remove_g/', views.delete_golf_player),
    path('create_tee/', views.create_tee_time_web),
    path('par/', views.update_course_par_web)
]