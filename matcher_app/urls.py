from django.urls import path
from matcher_app import views

urlpatterns = [
    path('candidates/<int:job_id>/', views.get_all_candidates_for_job),
    path('candidate/opinion/', views.add_opinion_for_candidate),
    path('candidate/note/', views.add_note_for_liked_candidate),
    path('candidates/liked/<int:job_id>/', views.get_data_for_liked_candidates),
    path('job/', views.handle_given_job),
    path('job/<int:job_id>/', views.handle_given_job),

]
