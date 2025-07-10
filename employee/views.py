from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from .models import CustomForm, FormField,EmployeeData
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.shortcuts import redirect


# Register View
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


# Profile View
class ProfileView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


# Change Password View
class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)

            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response({"detail": "Password updated successfully."})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    
    

def register_page(request):
    return render(request, 'reg.html')

def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            from django.contrib.auth import login
            login(request, user)
            return redirect('form-builder')  # Redirect to form builder after login
        else:
            messages.error(request, "Invalid username or password.")
    
    return render(request, 'login.html')
    
# employee/views.py


class CustomFormCreateView(generics.CreateAPIView):
    queryset = CustomForm.objects.all()
    serializer_class = CustomFormSerializer
    
    def get_permissions(self):
        return []  # Allow session authentication

class FormFieldCreateView(generics.CreateAPIView):
    queryset = FormField.objects.all()
    serializer_class = FormFieldSerializer
    
    def get_permissions(self):
        return []  # Allow session authentication

class CustomFormListView(generics.ListAPIView):
    queryset = CustomForm.objects.all()
    serializer_class = CustomFormSerializer
    
    def get_permissions(self):
        return []  # Allow session authentication





@login_required
def form_builder_view(request):
    return render(request, 'form_builder.html')

# views.py
from rest_framework.decorators import api_view



@api_view(['PATCH'])
def update_field_order(request, pk):
    try:
        field = FormField.objects.get(pk=pk)
        field.order = request.data.get("order", field.order)
        field.save()
        return Response({"status": "order updated"})
    except FormField.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)






class EmployeeCreateView(generics.CreateAPIView):
    queryset = EmployeeData.objects.all()
    serializer_class = EmployeeDataSerializer
    
    def get_permissions(self):
        return []  # Allow session authentication

class EmployeeListView(generics.ListAPIView):
    queryset = EmployeeData.objects.all()
    serializer_class = EmployeeDataSerializer
    
    def get_permissions(self):
        return []  # Allow session authentication

class EmployeeDeleteView(generics.DestroyAPIView):
    queryset = EmployeeData.objects.all()
    serializer_class = EmployeeDataSerializer
    
    def get_permissions(self):
        return []  # Allow session authentication

class EmployeeUpdateView(generics.UpdateAPIView):
    queryset = EmployeeData.objects.all()
    serializer_class = EmployeeDataSerializer
    
    def get_permissions(self):
        return []  # Allow session authentication
    
    
@login_required
def employee_form_page(request):
    form_id = request.GET.get("form_id")
    return render(request, 'employee_form.html', {'form_id': form_id})

@api_view(['POST'])
def save_multiple_fields(request):
    fields = request.data.get('fields', [])
    created = []
    errors = []

    for index, field in enumerate(fields):
        # Check for duplicate label in the same form
        if FormField.objects.filter(form_id=field['form'], label=field['label']).exists():
            errors.append({'label': field['label'], 'error': 'Field with this label already exists for this form.'})
            continue
        serializer = FormFieldSerializer(data={
            'form': field['form'],
            'label': field['label'],
            'field_type': field['field_type'],
            'order': index
        })
        if serializer.is_valid():
            serializer.save()
            created.append(serializer.data)
        else:
            errors.append({'label': field['label'], 'error': serializer.errors})

    response = {'saved_fields': created}
    if errors:
        response['errors'] = errors
    return Response(response)

class FormFieldDeleteView(generics.DestroyAPIView):
    queryset = FormField.objects.all()
    serializer_class = FormFieldSerializer
    
    def get_permissions(self):
        return []  # Allow session authentication

@login_required
def profile_page(request):
    return render(request, 'profile.html', {'user': request.user})

@login_required
def change_password_page(request):
    print(f"Request method: {request.method}")
    print(f"User authenticated: {request.user.is_authenticated}")
    
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        print(f"Old password provided: {'Yes' if old_password else 'No'}")
        print(f"New password provided: {'Yes' if new_password else 'No'}")
        print(f"Confirm password provided: {'Yes' if confirm_password else 'No'}")
        
        if new_password != confirm_password:
            print("Error: New passwords do not match")
            messages.error(request, "New passwords do not match.")
        elif not request.user.check_password(old_password):
            print("Error: Old password is incorrect")
            messages.error(request, "Old password is incorrect.")
        else:
            print("Password change successful")
            request.user.set_password(new_password)
            request.user.save()
            update_session_auth_hash(request, request.user)
            messages.success(request, "Password changed successfully.")
            return redirect('form-builder')
    return render(request, 'change_password.html')
