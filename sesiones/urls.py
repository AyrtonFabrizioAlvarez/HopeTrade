from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('users/', views.list_users, name='list_users'),
    path('edit_user/<int:user_id>/', views.edit_user, name='edit_user'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('delete/', views.delete, name='delete'),
    path('view_profile_user/<int:user_id>', views.view_profile_user, name='view_profile_user'),
    path('view_profile_helper/<int:helper_id>', views.view_profile_helper, name='view_profile_helper'),
    path('view_profile_admin/<int:admin_id>', views.view_profile_admin, name='view_profile_admin'),
    path('edit_admin/<int:admin_id>', views.edit_admin, name='edit_admin'),    
    #MILENA
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    path('recuperarclave/', views.recuperar_contrasenia, name='recuperar_contrasenia'),
    
    #IVAN
    path('signup_helper/', views.signup_helper, name='signup_helper'),
    path('edit_helper/<int:helper_id>', views.edit_intern, name='edit_helper'),
    path('helpers/', views.list_helpers, name='list_helpers'),
    path('delete_helper/<int:helper_id>', views.delete_helper, name='delete_helper'),
]
