from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import *

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', profile_page, name='profile-page'),
    path('change-password/', change_password_page, name='change-password-page'),

    path('register-page/', register_page, name='register-page'),
    path('login-page/', login_page, name='login-page'),
    
    # JWT Login and Token Refresh
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    
    path('form/create/', CustomFormCreateView.as_view(), name='form-create'),
    path('form/fields/add/', FormFieldCreateView.as_view(), name='field-add'),
    path('form/list/', CustomFormListView.as_view(), name='form-list'),
    
    path('form/builder/', form_builder_view, name='form-builder'),
    path('update-field-order/<int:pk>/', update_field_order),
    
    
    path('employee/create/', EmployeeCreateView.as_view(), name='employee-create'),
    path('employee/list/', EmployeeListView.as_view(), name='employee-list'),
    path('employee/delete/<int:pk>/', EmployeeDeleteView.as_view(), name='employee-delete'),
    path('employee/update/<int:pk>/', EmployeeUpdateView.as_view(), name='employee-update'),
    
    path('form/ui/', employee_form_page, name='employee-form-ui'),
    path('form/fields/save-multiple/', save_multiple_fields, name='save-multiple-fields'),
    path('form/fields/delete/<int:pk>/', FormFieldDeleteView.as_view(), name='formfield-delete'),


]
