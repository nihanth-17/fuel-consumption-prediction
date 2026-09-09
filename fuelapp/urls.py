from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('admin-login/', views.admin_login, name='admin_login'),
    path('user-login/', views.user_login, name='user_login'),
    path('register/', views.register, name='register'),
    path('user-dashboard/', views.user_dashboard, name='user_dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('upload-dataset/', views.upload_dataset, name='upload_dataset'),
    path('train-model/', views.train_model, name='train_model'),
    path('predict-fuel/', views.predict_fuel, name='predict_fuel'),
    path('view-predictions-user/', views.view_predictions_user, name='view_predictions_user'),
    path('view-predictions-admin/', views.view_predictions_admin, name='view_predictions_admin'),
    path('view-users/', views.view_users, name='view_users'),
    path('about-us/', views.about_us, name='about_us'),
    path('user-profile/', views.user_profile, name='user_profile'),
    path('logout/', views.logout_view, name='logout'),
]