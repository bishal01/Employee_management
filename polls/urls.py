from django.urls import path
from . import views
urlpatterns = [
    path('', views.loginPage, name="login"),  
    path('dashboard/',views.dashboard,name="dashboard"),
    path('register/', views.registerPage, name="register"),
	path('logout/', views.logoutUser, name="logout"),
    path('customer/<str:pk>/',views.customer_pages,name="customer_pages"),
    path('create_order/<str:pk>/',views.create_order,name='create_order'),
    path('update_order/<str:pk>/',views.update_order,name='update_order'),
    path('delete_item/<str:pk>/',views.delete_item,name="delete_item"),
    path('customer_page/',views.customer_page,name="user-page"),
    path('settings/',views.cus_settings,name="settings")

]
