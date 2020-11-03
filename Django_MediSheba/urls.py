from django.contrib import admin
from django.urls import path

from MediSheba import views as MediSheba_views

app_name = 'main'

urlpatterns = [
    path('admin/', admin.site.urls),

    path('submit', MediSheba_views.submit, name='submit'),
    path('signup', MediSheba_views.signup, name='signup'),
    path('', MediSheba_views.login, name='login'),

    path('doctor', MediSheba_views.doctor_home, name='doctor_home'),
    path('user', MediSheba_views.user_home, name='user_home'),
    path('hospital_admin', MediSheba_views.hospital_admin_home, name='hospital_admin_home'),
    path('blood_bank_admin', MediSheba_views.blood_bank_admin_home, name='blood_bank_admin_home'),

    path('signupSubmit', MediSheba_views.signupSubmit, name='submit'),

    path('doctor/edit_profile_details', MediSheba_views.doctor_edit_profile, name='doctor_edit_profile'),
    path('doctor/search_options', MediSheba_views.search_options, name='search_options'),
    path('doctor/view_appointments', MediSheba_views.view_appointments, name='view_appointments'),
    path('doctor/blood_bank_appointment', MediSheba_views.blood_bank_appointment, name='blood_bank_appointment'),
    path('doctor/view_calender', MediSheba_views.view_calender, name='view_calender'),
    path('doctor/view_records', MediSheba_views.view_records, name='view_records'),
    path('doctor/change_schedule', MediSheba_views.change_schedule, name='change_schedule'),
    path('doctor/logout', MediSheba_views.logout, name='log_out'),
    path('doctor/submit_changed_profile_doctor', MediSheba_views.submit_changed_profile_doctor, name='submit_changed_profile_doctor'),

    path('users/see_doctors', MediSheba_views.see_doctors, name='see_doctors'),

    path('doctor/search_doctors', MediSheba_views.search_doctors, name='search_doctors'),
    path('hospital/search_hospitals', MediSheba_views.search_hospitals, name='search_hospitals'),
    path('blood_bank/search_blood_banks', MediSheba_views.search_blood_banks, name='search_blood_banks')

]
