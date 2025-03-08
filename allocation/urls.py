from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("signup/", views.signup, name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("user-dashboard/", views.user_dashboard, name="user_dashboard"),
    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("view-stands/", views.view_stands, name="view_stands"),
    path("apply-for-stand/<int:stand_id>/", views.apply_for_stand, name="apply_for_stand"),
    path("application-status/", views.view_application_status, name="view_application_status"),
    
    # Admin routes
    path("admin/manage-stands/", views.manage_stands, name="manage_stands"),
    path("admin/view-applied-stands/", views.view_applied_stands, name="view_applied_stands"),
    path("admin/approve-application/<int:application_id>/", views.approve_application, name="approve_application"),
    path("admin/reject-application/<int:application_id>/", views.reject_application, name="reject_application"),
    path("admin/add-stand/", views.add_stand, name="add_stand"),
    path("admin/edit-stand/<int:stand_id>/", views.edit_stand, name="edit_stand"),
    path("admin/delete-stand/<int:stand_id>/", views.delete_stand, name="delete_stand"),
    path("admin/generate-report/", views.generate_report, name="generate_report"),

    path("admin/manage-users/", views.manage_users, name="manage_users"),
    path("admin/add-user/", views.add_user, name="add_user"),
    path("admin/edit-user/<int:user_id>/", views.edit_user, name="edit_user"),
    path("admin/delete-user/<int:user_id>/", views.delete_user, name="delete_user"),
]

