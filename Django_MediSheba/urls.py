from django.contrib import admin
from django.urls import path

from MediSheba import views as MediSheba_views

app_name = 'main'

urlpatterns = [
    path('admin/', admin.site.urls),

    path('submit', MediSheba_views.submit, name='submit'),
    path('signup', MediSheba_views.signup, name='signup'),
    path('', MediSheba_views.login, name='login'),

    path('doctor/', MediSheba_views.doctor_home, name='doctor_home'),
    path('user/', MediSheba_views.user_home, name='user_home'),
    path('hospital_admin/', MediSheba_views.hospital_admin_home, name='hospital_admin_home'),
    path('bloodbank/', MediSheba_views.blood_bank_admin_home, name='blood_bank_admin_home'),

    path('signupSubmit', MediSheba_views.signupSubmit, name='submit'),

    # URL FOR DOCTORS
    path('doctor/edit_profile_details/', MediSheba_views.doctor_edit_profile, name='doctor_edit_profile'),
    path('doctor/search_options/', MediSheba_views.doctor_search_options, name='doctor_search_options'),
    path('doctor/view_appointments/', MediSheba_views.doctor_view_appointments, name='doctor_view_appointments'),
    path('doctor/blood_bank_appointment/', MediSheba_views.doctor_blood_bank_appointment,
         name='doctor_blood_bank_appointment'),
    path('doctor/view_calender/', MediSheba_views.doctor_view_calender, name='doctor_view_calender'),
    path('doctor/view_records/', MediSheba_views.doctor_view_records, name='doctor_view_records'),
    path('doctor/change_schedule/', MediSheba_views.doctor_change_schedule, name='doctor_change_schedule'),
    path('doctor/logout', MediSheba_views.logout, name='log_out'),
    path('doctor/submit_changed_profile_doctor/', MediSheba_views.submit_changed_profile_doctor,
         name='submit_changed_profile_doctor'),
    path('doctor/search_options/search_doctors/', MediSheba_views.search_doctors_by_doctor,
         name='search_doctors_by_doctor'),
    path('doctor/search_options/search_doctors/custom_search_for_doctor', MediSheba_views.custom_search_for_doctor,
         name='custom_search_for_doctor'),
    path('doctor/search_options/search_doctors/see_specific_doctor_details', MediSheba_views.see_specific_doctor_details, name="see_specific_doctor_details"),

    path('doctor/search_options/search_hospitals/', MediSheba_views.search_hospitals_by_doctor,
         name='search_hospitals_by_doctor'),
    path('doctor/search_options/search_blood_banks/', MediSheba_views.search_blood_banks, name='search_blood_banks'),

    # URL FOR USERS
    path('users/search_options/', MediSheba_views.user_search_options, name='user_search_options'),
    path('users/search_options/search_doctors/', MediSheba_views.search_doctors_by_user, name='search_doctors_by_user'),
    path('users/search_options/search_doctors/custom_search_for_doctor', MediSheba_views.custom_search_for_doctor_by_user, name='customer_search_for_doctor_by_user'),
    path('users/search_options/search_hospitals/', MediSheba_views.search_hospitals_by_users,
         name='search_hospitals_by_users'),

    path('users/user_edit_profile/', MediSheba_views.user_edit_profile, name='user_edit_profile'),
    path('users/user_doctor_appointment/', MediSheba_views.user_doctor_appointment, name='user_doctor_appointment'),
    path('users/user_blood_bank_appointment/', MediSheba_views.user_blood_bank_appointment,
         name='user_blood_bank_appointment'),
    path('users/submit_changed_profile_user/', MediSheba_views.submit_changed_profile_user,
         name='submit_changed_profile_user'),
    path('users/user_modify_appointment/', MediSheba_views.user_modify_appointment, name='user_modify_appointment'),
    path('users/user_hospital_appointment/', MediSheba_views.user_hospital_appointment,
         name='user_hospital_appointment'),

    # URL FOR BLOOD BANK ADMIN
    path('bloodbank/bloodbank_search_options/search_doctors/', MediSheba_views.search_doctors_by_bloodbank,
         name='search_doctors_by_bloodbank'),
    path('bloodbank/bloodbank_search_options/search_doctors/custom_search_for_doctor', MediSheba_views.custom_search_for_doctor_by_blood_bank_admin,
         name='custom_search_for_doctor_by_blood_bank_admin'),
    path('bloodbank/bloodbank_search_options/search_hospitals/', MediSheba_views.search_hospitals_by_bloodbank,
         name='search_hospitals_by_bloodbank'),
    path('bloodbank/bloodbank_search_options/', MediSheba_views.bloodbank_search_options,
         name='bloodbank_search_options'),
    path('bloodbank/bloodbank_edit_profile/', MediSheba_views.bloodbank_admin_edit_profile,
         name='blood_bank_admin_edit_profile'),
    path('bloodbank/bloodbank_collection/', MediSheba_views.bloodbank_collection, name='blood_bank_collection'),
    path('bloodbank/bloodbank_calender/', MediSheba_views.bloodbank_calender, name='blood_bank_calender'),
    path('bloodbank/bloodbank_history/', MediSheba_views.bloodbank_history, name='blood_bank_history'),
    path('bloodbank/bloodbank_all_appointments/', MediSheba_views.bloodbank_all_appointments,
         name='bloodbank_all_appointments'),

    # URL FOR HOSPITAL ADMIN
    path('hospital_admin/hospital_search_options/', MediSheba_views.hospital_search_options,
         name='hospital_search_options'),
    path('hospital_admin/hospital_admin_edit_profile/', MediSheba_views.hospital_admin_edit_profile,
         name='hospital_admin_edit_profile'),
    path('hospital_admin/hospital_admin_view_appointments/', MediSheba_views.hospital_admin_view_appointments,
         name='hospital_admin_view_appointments'),
    path('hospital_admin/hospital_admin_view_schedule/', MediSheba_views.hospital_admin_view_schedule,
         name='hospital_admin_view_schedule'),
    path('hospital_admin/hospital_admin_cabin_management/', MediSheba_views.hospital_admin_cabin_management,
         name='hospital_admin_cabin_management'),
    path('hospital_admin/hospital_admin_view_records/', MediSheba_views.hospital_admin_view_records,
         name='hospital_admin_view_records'),
    path('hospital_admin/hospital_search_options/search_doctors/', MediSheba_views.search_doctors_by_hospitals,
         name='search_doctors_by_hospitals'),
    path('hospital_admin/hospital_search_options/search_doctors/custom_search_for_doctor', MediSheba_views.custom_search_for_doctor_by_hospital_admin,
         name='custom_search_for_doctor_by_hospital_admin'),
    path('hospital_admin/hospital_search_options/search_hospitals/', MediSheba_views.search_hospitals_by_hospitals,
         name='search_hospitals_by_hospitals'),
    path('hospital_admin/hospital_search_options/search_blood_banks/', MediSheba_views.search_blood_banks_by_hospitals,
         name='search_blood_banks_by_hospitals'),

    # URLS FOR CUSTOM SEARCH


]
