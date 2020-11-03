from django.http import HttpResponse
from django.shortcuts import render
import cx_Oracle

import HelperClasses.encryptPass as decoder_encoder
from HelperClasses import json_extractor

from .models import DoctorName

# login
user_info = {}  # holds user data across pages

def login(request):
    return render(request, "auth/LogInOrSignUp.html")

def signup(request):
    return render(request, "auth/SignUp.html")

# homepage URLs
def doctor_home(request):
    return render(request, "homepage/DoctorHome2.html", {'name': user_info['name']})


def user_home(request):
    return render(request, "homepage/UserHome2.html")


def hospital_admin_home(request):
    return render(request, 'homepage/HospitalAdminHome2.html')


def blood_bank_admin_home(request):
    return render(request,'homepage/BloodbankHome2.html')

def submit(request):
    email = request.POST['email']
    password = request.POST['pass']
    user = request.POST['User']

    print("EMAIL: " + email)
    print("PASS: " + password)
    print("User Type: " + user)

    dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
    conn = cx_Oracle.connect(user='MEDI_SHEBA', password='1234', dsn=dsn_tns)

    c = conn.cursor()

    # TODO: connect database and verify
    if user == "Doctor":
        statement = "SELECT DOCTOR_ID, PASSWORD, FIRST_NAME || ' ' || LAST_NAME from MEDI_SHEBA.DOCTOR WHERE EMAIL=" + "\'" + email + "\'"
        c.execute(statement)
        if c:
            x = c.fetchone()
            return_id = x[0]
            return_password = x[1]
            return_name = x[2]

            user_info['pk'] = return_id
            user_info['name'] = return_name
            user_info['email'] = email

            decoded_password = decoder_encoder.EncryptPasswords(return_password).decryptPassword()

            if decoded_password == password:
                return render(request, "homepage/DoctorHome2.html", {'name': return_name})
            else:
                return HttpResponse("Wrong Pass")
        else:
            return HttpResponse("Database Error or You don't exist")

    elif user == "User":
        statement = "SELECT USER_ID, PASSWORD, FIRST_NAME||' '||LAST_NAME from MEDI_SHEBA.USERS WHERE EMAIL=" + "\'" + email + "\'"

        c.execute(statement)
        if c:
            x = c.fetchone()
            return_id = x[0]
            return_password = x[1]
            return_name = x[2]

            user_info['pk'] = return_id
            user_info['name'] = return_name
            user_info['email'] = email

            decoded_password = decoder_encoder.EncryptPasswords(return_password).decryptPassword()

            if decoded_password == password:
                return render(request, "homepage/UserHome2.html")
            else:
                return HttpResponse("Wrong Pass")
        else:
            return HttpResponse("Database Error or You don't exist")

    elif user == "HospitalAdmin":
        statement = "SELECT HOSPITAL_ID,PASSWORD, FIRST_NAME||' '||LAST_NAME from MEDI_SHEBA.HOSPITAL WHERE EMAIL=" + "\'" + email + "\'"
        c.execute(statement)
        if c:
            x = c.fetchone()
            return_id = x[0]
            return_password = x[1]
            return_name = x[2]

            user_info['pk'] = return_id
            user_info['name'] = return_name
            user_info['email'] = email

            decoded_password = decoder_encoder.EncryptPasswords(return_password).decryptPassword()

            if decoded_password == password:
                return render(request, "homepage/HospitalAdminHome2.html")
            else:
                return HttpResponse("Wrong Pass")
        else:
            return HttpResponse("Database Error or You don't exist")

    elif user == "BloodBankAdmin":
        statement = "SELECT BLOOD_BANK_ID,PASSWORD, FIRST_NAME||' '|| LAST_NAME from MEDI_SHEBA.BLOOD_BANK WHERE EMAIL=" + "\'" + email + "\'"
        c.execute(statement)
        if c:
            x = c.fetchone()
            return_id = x[0]
            return_password = x[1]
            return_name = x[2]

            user_info['pk'] = return_id
            user_info['name'] = return_name
            user_info['email'] = email

            decoded_password = decoder_encoder.EncryptPasswords(return_password).decryptPassword()

            if decoded_password == password:
                return render(request, "homepage/BloodbankHome2.html")
            else:
                return HttpResponse("Wrong Pass")
        else:
            return HttpResponse("Database Error or You don't exist")
    return render(request, "auth/LogInOrSignUp.html")

# signup


def signupSubmit(request):
    usertype = request.POST['User']
    firstname = request.POST['fname']
    lastname = request.POST['lname']
    email = request.POST['email']
    phone = request.POST['phone']
    password_in = request.POST['pass']
    confirm_in = request.POST['cpass']
    gender_in = request.POST['Gender']
    blood_bank_name = hospital_name = request.POST['company']

    password = decoder_encoder.EncryptPasswords(password_in).encryptPassword()

    gender = ""
    if gender_in == "male":
        gender = "M"
    else:
        gender = "F"

    if usertype == 'doctor':

        dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
        conn = cx_Oracle.connect(user='MEDI_SHEBA', password='1234', dsn=dsn_tns)
        c = conn.cursor()
        c2 = conn.cursor()

        statement = "INSERT INTO MEDI_SHEBA.DOCTOR(FIRST_NAME, LAST_NAME, EMAIL, PHONE,PASSWORD, GENDER) VALUES (" + "\'" + firstname + \
                    "\', " + "\'" + lastname + "\'," + "\'" + email + "\', " + "\'" + phone + "\', " + "\'" + password + "\', " + "\'" + gender + "\'" + ")"
        c.execute(statement)
        conn.commit()

        statement = "SELECT DOCTOR_ID, FIRST_NAME || ' ' || LAST_NAME from MEDI_SHEBA.DOCTOR WHERE EMAIL=" + "\'" + email + "\'"
        c2.execute(statement)

        if c2:
            x = c2.fetchone()
            return_id = x[0]
            return_name = x[1]

            user_info['pk'] = return_id
            user_info['name'] = return_name
            user_info['email'] = email

        return render(request, "homepage/DoctorHome2.html", {'name': return_name})

    elif usertype == 'user':
        dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
        conn = cx_Oracle.connect(user='MEDI_SHEBA', password='1234', dsn=dsn_tns)
        c = conn.cursor()
        statement = "INSERT INTO MEDI_SHEBA.USERS(FIRST_NAME, LAST_NAME, EMAIL, PHONE,PASSWORD, GENDER) VALUES (" + "\'" + firstname + \
                    "\', " + "\'" + lastname + "\'," + "\'" + email + "\', " + "\'" + phone + "\', " + "\'" + password + "\', " + "\'" + gender + "\'" + ")"
        c.execute(statement)
        conn.commit()

        c2 = conn.cursor()

        statement = "SELECT USER_ID, FIRST_NAME || ' ' || LAST_NAME from MEDI_SHEBA.USERS WHERE EMAIL=" + "\'" + email + "\'"

        c2.execute(statement)

        if c2:
            x = c2.fetchone()
            return_id = x[0]
            return_name = x[1]

            user_info['pk'] = return_id
            user_info['name'] = return_name
            user_info['email'] = email

        return render(request, "homepage/UserHome.html")

    elif usertype == 'hospitalAdmin':
        dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
        conn = cx_Oracle.connect(user='MEDI_SHEBA', password='1234', dsn=dsn_tns)
        c = conn.cursor()

        statement = "INSERT INTO MEDI_SHEBA.HOSPITAL(HOSPITAL_NAME, FIRST_NAME, LAST_NAME, PASSWORD, GENDER, EMAIL, PHONE) VALUES" \
                    " (" + "\'" + hospital_name + "\'," + "\'" + firstname + "\'," + "\'" + lastname + "\'," + "\'" + password + "\'," + "\'" + gender \
                    + "\'," + "\'" + email + "\'," + "\'" + phone + "\'" + ")"

        c.execute(statement)
        conn.commit()

        c2 = conn.cursor()

        statement = "SELECT HOSPITAL_ID, FIRST_NAME || ' ' || LAST_NAME from MEDI_SHEBA.HOSPITAL WHERE EMAIL=" + "\'" + email + "\'"

        c2.execute(statement)

        if c2:
            x = c2.fetchone()
            return_id = x[0]
            return_name = x[1]

            user_info['pk'] = return_id
            user_info['name'] = return_name
            user_info['email'] = email

        return render(request, "homepage/HospitalAdminHome.html")

    elif usertype == 'bloodbankAdmin':
        dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
        conn = cx_Oracle.connect(user='MEDI_SHEBA', password='1234', dsn=dsn_tns)
        c = conn.cursor()

        statement = "INSERT INTO MEDI_SHEBA.BLOOD_BANK(NAME, FIRST_NAME, LAST_NAME, PASSWORD, GENDER, EMAIL, PHONE) VALUES" \
                    " (" + "\'" + blood_bank_name + "\'," + "\'" + firstname + "\'," + "\'" + lastname + "\'," + "\'" + password + "\'," + "\'" + gender \
                    + "\'," + "\'" + email + "\'," + "\'" + phone + "\'" + ")"

        c.execute(statement)
        conn.commit()

        c2 = conn.cursor()

        statement = "SELECT BLOOD_BANK_ID, FIRST_NAME || ' ' || LAST_NAME from MEDI_SHEBA.BLOOD_BANK WHERE EMAIL=" + "\'" + email + "\'"

        c2.execute(statement)

        if c2:
            x = c2.fetchone()
            return_id = x[0]
            return_name = x[1]

            user_info['pk'] = return_id
            user_info['name'] = return_name
            user_info['email'] = email

        return render(request, "homepage/BloodbankAdminHome.html")


# doctor

def doctor_edit_profile(request):
    dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
    conn = cx_Oracle.connect(user='MEDI_SHEBA', password='1234', dsn=dsn_tns)
    c = conn.cursor()
    statement = "SELECT HOSPITAL_NAME FROM MEDI_SHEBA.HOSPITAL"
    c.execute(statement)

    hospital_names = []

    '''
    print(user_info['pk'])
    print(user_info['name'])
    print(user_info['email'])
    '''

    for i in c:
        hospital_names.append(i[0])

    location_names = json_extractor.JsonExtractor('name').extract("HelperClasses/zilla_names.json")
    location_names.sort()

    return render(request, 'homepage/DoctorProfileEditor.html',
                  {'hospital_names': hospital_names, 'locations': location_names})


def submit_changed_profile_doctor(request):
    first_name = request.POST['f_name']
    last_name = request.POST['l_name']
    phone_number = request.POST['phone']
    location = request.POST['address']
    email = request.POST['email']
    blood_type = request.POST['blood_type']
    hospital_name = request.POST['hospital_name']
    fee = request.POST['fee']
    specialization = request.POST['specialization']
    additional_details = request.POST['additional_details']

    print(first_name)
    print(last_name)
    print(phone_number)
    print(location)
    print(email)
    print(blood_type)
    print(hospital_name)
    print(fee)
    print(specialization)
    print(additional_details)

    return HttpResponse("CHANGED PROFILE")

def search_options(request):
    dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
    conn = cx_Oracle.connect(user='MEDI_SHEBA', password='1234', dsn=dsn_tns)
    c = conn.cursor()
    return render(request, 'homepage/Search.html')

def view_appointments(request):
    return HttpResponse("Appointments Here")


def blood_bank_appointment(request):
    return HttpResponse("Blood Bank Appointment Here")


def view_calender(request):
    return HttpResponse("View Calender Here")


def view_records(request):
    return HttpResponse("view records")


def change_schedule(request):
    return render(request, 'schedule_editor/AddSchedule.html')


def logout(request):
    return HttpResponse("Log Out")

def search_doctors(request):
    return HttpResponse("Available Doctors:")

# USERS

def see_doctors(request):
    location_names = json_extractor.JsonExtractor('name').extract("HelperClasses/zilla_names.json")
    location_names.sort()

    specialization = []

    docList = []

    dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
    conn = cx_Oracle.connect(user='MEDI_SHEBA', password='1234', dsn=dsn_tns)
    c = conn.cursor()
    c.execute("SELECT FIRST_NAME || ' ' || LAST_NAME,PHONE, GENDER, SPECIALIZATION, HOSPITAL_ID "
              "from MEDI_SHEBA.DOCTOR")
    index = 1
    for row in c:
        docList.append(DoctorName(index, row[0], row[1], row[2], row[3], row[4]))  # DoctorName is defined in models.py
        index = index + 1
    conn.close()

    return render(request, "query_pages/doctor_query.html",
                  {'doc': docList, 'opt': location_names, 'specialization': specialization})

# Hospital

def search_hospitals(request):
    return HttpResponse("Available Hospitals:")

# Blood_Bank

def search_blood_banks(request):
    return HttpResponse("Available Blood Banks:")