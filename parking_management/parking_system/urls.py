from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name="login"),
    path('', views.base, name='base'),
    path('dashboard/', views.dashboard, name='dashboard'),  # Ensure this points to the correct view
    
    path("category/", views.categories, name="category"),
    path("update_cat/<int:id>/", views.update_cat, name="update_cat"),
    path("delete_cat/<int:id>/", views.delete_cat, name="delete_cat"),
    path('activate_cat/<int:id>/', views.activate_cat, name='activate_cat'),
    path('deactivate_cat/<int:id>/', views.deactivate_cat, name='deactivate_cat'),

    path("entry/", views.vehicle_entry, name='entry'),
    path('activate_entry/<int:id>/', views.activate_entry, name='activate_entry'),
    path('deactivate_entry/<int:id>/', views.deactivate_entry, name='deactivate_entry'),

    path("register/", views.register, name="register"),
    path("logout/", views.logout, name="logout"),

    path('showreciept/<int:id>/', views.show_receipt, name='show_receipt'),
    path('createpdf/<int:id>/', views.pdf_report_create, name='createpdf'),

    path('manage/', views.manage_vehicles, name='manage'),
    path('mark_as_leaved/<int:vehicle_id>/', views.mark_as_leaved, name='mark_as_leaved'),
    path('manage_activate/<int:id>/', views.manage_act_entry, name='manage_act_entry'),
    path('manage_deactivate/<int:id>/', views.manage_deact_entry, name='manage_deact_entry'),
    path('update_status/', views.update_status, name='update_status'),

    path('search/', views.search, name='search'),
    path('vehicle_data/', views.vehicle_entry, name='vehicle_data'),
    path('search_activate/<int:id>/', views.search_act_entry, name='search_act_entry'),
    path('search_deactivate/<int:id>/', views.search_deact_entry, name='search_deact_entry'),

    path('accounts/', views.accounts, name='accounts'),
    path('reset_password/', views.reset_password, name='reset_password'),

    path("reports/", views.reports, name="reports")
]
