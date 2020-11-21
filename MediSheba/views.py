from django.http import HttpResponse
from django.shortcuts import render, redirect
import cx_Oracle

import HelperClasses.encryptPass as decoder_encoder
from HelperClasses import json_extractor

from .models import DoctorName
from .models import BloodBankList
from .models import HospitalName
# login
user_info = {}  # holds user data across pages


def login(request):
    return render(request, "auth/LogInOrSignUp.html")


def signup(request):
    return render(request, "auth/SignUp.html")


# homepage URLs
def doctor_home(request):
    return render(request, "homepage/DoctorHome.html", {'name': user_info['f_name'] + ' ' + user_info['l_name']})


def user_home(request):
    return render(request, "homepage/UserHome.html", {'name': user_info['f_name'] + ' ' + user_info['l_name']})


def hospital_admin_home(request):
    return render(request, 'homepage/HospitalAdminHome.html')


def blood_bank_admin_home(request):
    return render(request, 'homepage/Blood_Bank_Home.html')


# log in

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
        statement = "SELECT DOCTOR_ID, PASSWORD, FIRST_NAME, LAST_NAME from MEDI_SHEBA.DOCTOR WHERE EMAIL=" + "\'" + email + "\'"
        c.execute(statement)
        if c:
            x = c.fetchone()
            return_id = x[0]
            return_password = x[1]
            return_f_name = x[2]
            return_l_name = x[3]

            user_info['pk'] = return_id
            user_info['f_name'] = return_f_name
            user_info['l_name'] = return_l_name
            user_info['email'] = email
            user_info['type'] = "doctor"

            decoded_password = decoder_encoder.EncryptPasswords(return_password).decryptPassword()

            if decoded_password == password:
                return redirect("doctor_home")
            else:
                return HttpResponse("Wrong Pass")
        else:
            return HttpResponse("Database Error or You don't exist")

    elif user == "User":
        statement = "SELECT USER_ID, PASSWORD, FIRST_NAME, LAST_NAME from MEDI_SHEBA.USERS WHERE EMAIL=" + "\'" + email + "\'"

        c.execute(statement)
        if c:
            x = c.fetchone()
            return_id = x[0]
            return_password = x[1]
            return_f_name = x[2]
            return_l_name = x[3]

            user_info['pk'] = return_id
            user_info['f_name'] = return_f_name
            user_info['l_name'] = return_l_name
            user_info['email'] = email
            user_info['type'] = "user"

            decoded_password = decoder_encoder.EncryptPasswords(return_password).decryptPassword()

            if decoded_password == password:
                return redirect("user_home")
            else:
                return HttpResponse("Wrong Pass")
        else:
            return HttpResponse("Database Error or You don't exist")

    elif user == "HospitalAdmin":
        statement = "SELECT HOSPITAL_ID,PASSWORD, FIRST_NAME, LAST_NAME from MEDI_SHEBA.HOSPITAL WHERE EMAIL=" + "\'" + email + "\'"
        c.execute(statement)
        if c:
            x = c.fetchone()
            return_id = x[0]
            return_password = x[1]
            return_f_name = x[2]
            return_l_name = x[3]

            user_info['pk'] = return_id
            user_info['f_name'] = return_f_name
            user_info['l_name'] = return_l_name
            user_info['email'] = email
            user_info['type'] = "hospital_admin"

            decoded_password = decoder_encoder.EncryptPasswords(return_password).decryptPassword()

            if decoded_password == password:
                return redirect("hospital_admin_home")
            else:
                return HttpResponse("Wrong Pass")
        else:
            return HttpResponse("Database Error or You don't exist")

    elif user == "BloodBankAdmin":
        statement = "SELECT BLOOD_BANK_ID,PASSWORD, FIRST_NAME, LAST_NAME from MEDI_SHEBA.BLOOD_BANK WHERE EMAIL=" + "\'" + email + "\'"
        c.execute(statement)
        if c:
            x = c.fetchone()
            return_id = x[0]
            return_password = x[1]
            return_f_name = x[2]
            return_l_name = x[3]

            user_info['pk'] = return_id
            user_info['f_name'] = return_f_name
            user_info['l_name'] = return_l_name
            user_info['email'] = email
            user_info['type'] = "blood_bank_admin"

            decoded_password = decoder_encoder.EncryptPasswords(return_password).decryptPassword()

            if decoded_password == password:
                return redirect("blood_bank_admin_home")
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

        statement = "SELECT DOCTOR_ID, FIRST_NAME, LAST_NAME from MEDI_SHEBA.DOCTOR WHERE EMAIL=" + "\'" + email + "\'"
        c2.execute(statement)

        if c2:
            x = c2.fetchone()
            return_id = x[0]
            return_f_name = x[1]
            return_l_name = x[2]

            user_info['pk'] = return_id
            user_info['f_name'] = return_f_name
            user_info['l_name'] = return_l_name
            user_info['email'] = email
            user_info['type'] = "doctor"

            return redirect("doctor_home")
        else:
            return HttpResponse("ERROR")  # changed here


    elif usertype == 'user':
        dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
        conn = cx_Oracle.connect(user='MEDI_SHEBA', password='1234', dsn=dsn_tns)
        c = conn.cursor()
        statement = "INSERT INTO MEDI_SHEBA.USERS(FIRST_NAME, LAST_NAME, EMAIL, PHONE,PASSWORD, GENDER) VALUES (" + "\'" + firstname + \
                    "\', " + "\'" + lastname + "\'," + "\'" + email + "\', " + "\'" + phone + "\', " + "\'" + password + "\', " + "\'" + gender + "\'" + ")"
        c.execute(statement)
        conn.commit()

        c2 = conn.cursor()

        statement = "SELECT USER_ID, FIRST_NAME, LAST_NAME from MEDI_SHEBA.USERS WHERE EMAIL=" + "\'" + email + "\'"

        c2.execute(statement)

        if c2:
            x = c2.fetchone()
            return_id = x[0]
            return_f_name = x[1]
            return_l_name = x[2]

            user_info['pk'] = return_id
            user_info['f_name'] = return_f_name
            user_info['l_name'] = return_l_name
            user_info['email'] = email
            user_info['type'] = "user"

            return redirect("user_home")
        else:
            return HttpResponse("ERROR")

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

        statement = "SELECT HOSPITAL_ID, FIRST_NAME, LAST_NAME from MEDI_SHEBA.HOSPITAL WHERE EMAIL=" + "\'" + email + "\'"

        c2.execute(statement)

        if c2:
            x = c2.fetchone()
            return_id = x[0]
            return_f_name = x[1]
            return_l_name = x[2]

            user_info['pk'] = return_id
            user_info['f_name'] = return_f_name
            user_info['l_name'] = return_l_name
            user_info['email'] = email
            user_info['type'] = "hospital_admin"

            return redirect("hospital_admin_home")
        else:
            return HttpResponse("ERROR")

    elif usertype == 'bloodbankAdmin':
        dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
        conn = cx_Oracle.connect(user='MEDI_SHEBA', password='1234', dsn=dsn_tns)
        c = conn.cursor()

        statement = "INSERT INTO MEDI_SHEBA.BLOOD_BANK(NAME, FIRST_NAME, LAST_NAME, PASSWORD, GENDER, EMAIL, PHONE) " \
                    "VALUES" \
                    " (" + "\'" + blood_bank_name + "\'," + "\'" + firstname + "\'," + "\'" + lastname + "\'," + "\'" + password + "\'," + "\'" + gender \
                    + "\'," + "\'" + email + "\'," + "\'" + phone + "\'" + ")"

        c.execute(statement)
        conn.commit()

        c2 = conn.cursor()

        statement = "SELECT BLOOD_BANK_ID, FIRST_NAME, LAST_NAME from MEDI_SHEBA.BLOOD_BANK WHERE EMAIL=" + "\'" + email + "\'"

        c2.execute(statement)

        if c2:
            x = c2.fetchone()
            return_id = x[0]
            return_f_name = x[1]
            return_l_name = x[2]

            user_info['pk'] = return_id
            user_info['f_name'] = return_f_name
            user_info['l_name'] = return_l_name
            user_info['email'] = email
            user_info['type'] = "blood_bank_admin"

            return redirect("blood_bank_admin_home")

        else:
            return HttpResponse("ERROR")


# doctor

def doctor_edit_profile(request):
    # authentication added here
    if bool(user_info) and user_info['type'] == "doctor":
        dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
        conn = cx_Oracle.connect(user='MEDI_SHEBA', password='1234', dsn=dsn_tns)
        c = conn.cursor()
        statement = "SELECT HOSPITAL_NAME FROM MEDI_SHEBA.HOSPITAL"
        c.execute(statement)

        hospital_names = []

        for i in c:
            hospital_names.append(i[0])

        location_names = json_extractor.JsonExtractor('name').extract("HelperClasses/zilla_names.json")
        location_names.sort()

        return render(request, 'homepage/DoctorProfileEditor.html',
                      {'hospital_names': hospital_names, 'locations': location_names})

    else:
        return HttpResponse("NO ACCESS TO THIS PAGE")


def submit_changed_profile_doctor(request):
    if bool(user_info) and user_info['type'] == 'doctor':
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

        dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
        conn = cx_Oracle.connect(user='MEDI_SHEBA', password='1234', dsn=dsn_tns)

        if first_name != "":
            c = conn.cursor()
            statement = "UPDATE MEDI_SHEBA.DOCTOR SET FIRST_NAME = " + "\'" + first_name + "\'" + "WHERE DOCTOR_ID = " + str(
                user_info['pk'])
            c.execute(statement)
            conn.commit()
        else:
            print("First Name NOT CHANGED ")

        if last_name != "":
            c = conn.cursor()
            statement = "UPDATE MEDI_SHEBA.DOCTOR SET LAST_NAME = " + "\'" + last_name + "\'" + "WHERE DOCTOR_ID = " + str(
                user_info['pk'])
            c.execute(statement)
            conn.commit()
        else:
            print("LAST Name NOT CHANGED ")

        if phone_number != "":
            c = conn.cursor()
            statement = "UPDATE MEDI_SHEBA.DOCTOR SET PHONE = " + "\'" + phone_number + "\'" + "WHERE DOCTOR_ID = " + str(
                user_info['pk'])
            c.execute(statement)
            conn.commit()
        else:
            print("PHONE NOT CHANGED ")

        if location != "":
            c = conn.cursor()
            statement = "UPDATE MEDI_SHEBA.DOCTOR SET LOCATION = " + "\'" + location + "\'" + "WHERE DOCTOR_ID = " + str(
                user_info['pk'])
            c.execute(statement)
            conn.commit()
        else:
            print("LOCATION NOT CHANGED ")

        if email != "":
            c = conn.cursor()
            statement = "UPDATE MEDI_SHEBA.DOCTOR SET EMAIL = " + "\'" + email + "\'" + "WHERE DOCTOR_ID = " + str(
                user_info['pk'])
            c.execute(statement)
            conn.commit()
        else:
            print("EMAIL NOT CHANGED ")

        if blood_type != "":
            c = conn.cursor()
            statement = "UPDATE MEDI_SHEBA.DOCTOR SET BLOOD_GROUP = " + "\'" + blood_type + "\'" + "WHERE DOCTOR_ID = " + str(
                user_info['pk'])
            c.execute(statement)
            conn.commit()
        else:
            print("BLOOD NOT CHANGED ")

        if hospital_name != "":
            c = conn.cursor()
            statement_1 = "SELECT HOSPITAL_ID FROM MEDI_SHEBA.HOSPITAL WHERE HOSPITAL_NAME = " + "\'" + hospital_name + "\'"
            c.execute(statement_1)

            hospital_id = 0
            for r in c:
                hospital_id = r[0]

            c = conn.cursor()
            statement = "UPDATE MEDI_SHEBA.DOCTOR SET HOSPITAL_ID = " + str(hospital_id) + " WHERE DOCTOR_ID = " \
                        + str(user_info['pk'])
            c.execute(statement)
            conn.commit()
        else:
            print("HOSPITAL NOT CHANGED ")

        if fee != "":
            c = conn.cursor()
            statement = "UPDATE MEDI_SHEBA.DOCTOR SET FEES = " + fee + " WHERE DOCTOR_ID = " + str(
                user_info['pk'])
            c.execute(statement)
            conn.commit()
        else:
            print("FEES NOT CHANGED ")

        if specialization != "":
            c = conn.cursor()
            statement = "UPDATE MEDI_SHEBA.DOCTOR SET SPECIALIZATION = " + "\'" + specialization + "\'" \
                        + " WHERE DOCTOR_ID = " + str(user_info['pk'])
            c.execute(statement)
            conn.commit()
        else:
            print("SPECIALIZATION NOT CHANGED ")
        print(additional_details)

        '''
        UPDATE DICTIONARY HERE, CAUSE NOT UPDATING THE DICTIONARY WILL SHOW WRONG INFORMATION ON THE PAGES
        
        UPDATE EMAIL, FIRST NAME, LAST NAME
        
        
        '''

        '''
        TODO: HANDLE MULTI VALUE DICT KEY ERROR IF SOMETHING IS NOT GIVEN AS INPUT, SPECIALLY DROP DOWN BOXES 
        '''
        c = conn.cursor()
        statement = "SELECT DOCTOR_ID, FIRST_NAME, LAST_NAME,EMAIL from MEDI_SHEBA.DOCTOR  WHERE DOCTOR_ID=" + str(
            user_info['pk'])
        c.execute(statement)
        if c:
            x = c.fetchone()
            id = x[0]
            f_name = x[1]
            l_name = x[2]
            email = x[3]
            user_info['pk'] = id
            user_info['f_name'] = f_name
            user_info['l_name'] = l_name
            user_info['email'] = email
        return redirect("doctor_home")
    else:
        return HttpResponse("Access not granted")


def doctor_search_options(request):
    if bool(user_info) and user_info['type'] == 'doctor':
        dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
        conn = cx_Oracle.connect(user='MEDI_SHEBA', password='1234', dsn=dsn_tns)
        c = conn.cursor()
        return render(request, 'homepage/Search_for_doctor.html')
    else:
        return HttpResponse("NO ACCESS")


def doctor_view_appointments(request):
    if bool(user_info) and user_info['type'] == 'doctor':
        return HttpResponse("Appointments Here")
    else:
        return HttpResponse("NO ACCESS")


def doctor_blood_bank_appointment(request):
    if bool(user_info) and user_info['type'] == 'doctor':
        return HttpResponse("Blood Bank Appointment Here")
    else:
        return HttpResponse("NO ACCESS")


def doctor_view_calender(request):
    if bool(user_info) and user_info['type'] == 'doctor':
        return render(request, 'schedule_editor/calendar.html')
    else:
        return HttpResponse("NO ACCESS")


def doctor_view_records(request):
    if bool(user_info) and user_info['type'] == 'doctor':
        return HttpResponse("view records")
    else:
        return HttpResponse(" NO ACCESS")


def doctor_change_schedule(request):
    if bool(user_info) and user_info['type'] == 'doctor':
        return render(request, 'schedule_editor/AddSchedule.html')
    else:
        return HttpResponse("No ACCESS")


def logout(request):
    user_info.clear()
    return redirect("login")


def search_doctors_by_doctor(request):
    return see_doctors(request)


def search_doctors_by_user(request):
    return see_doctors(request)


def search_doctors_by_bloodbank(request):
    return see_doctors(request)


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
def search_hospitals_by_doctor(request):
    return see_hospitals(request)

def search_hospitals_by_users(request):
    return see_hospitals(request)

def search_hospitals_by_bloodbank(request):
    return see_hospitals(request)

def search_hospitals_by_hospitalAdmin(request):
    return see_hospitals(request)

def see_hospitals(request):
    location_names = json_extractor.JsonExtractor('name').extract("HelperClasses/zilla_names.json")
    location_names.sort()


    hospitalList = []

    dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
    conn = cx_Oracle.connect(user='MEDI_SHEBA', password='1234', dsn=dsn_tns)
    c = conn.cursor()
    c.execute("SELECT FIRST_NAME || ' ' || LAST_NAME,PHONE,LOCATION "
              "from MEDI_SHEBA.HOSPITAL")
    index = 1
    for row in c:
        hospitalList.append(HospitalName(index, row[0], row[1],row[2]))  # HospitalName is defined in models.py
        index = index + 1
        '''print(row[2])'''
    conn.close()

    return render(request, "query_pages/hospital_query.html",
                  {'hos': hospitalList, 'opt': location_names})



# Blood_Bank

def search_blood_banks(request):
    location_names = json_extractor.JsonExtractor('name').extract("HelperClasses/zilla_names.json")
    location_names.sort()

    bbankList = []
    dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
    conn = cx_Oracle.connect(user='MEDI_SHEBA', password='1234', dsn=dsn_tns)
    c = conn.cursor()
    '''
    c.execute("SELECT NAME,'A+','A-','B+','B-','O+','O-','AB+','AB-'"
              "from MEDI_SHEBA.BLOOD_BANK")
    '''

    statement = "SELECT NAME, \"A+\", \"A-\", \"B+\", \"B-\", \"O+\", \"O-\", \"AB+\", \"AB-\" FROM MEDI_SHEBA.BLOOD_BANK"
    c.execute(statement)

    index = 1
    for row in c:
        bbankList.append(BloodBankList(index, row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]))
        index = index + 1
    conn.close()

    return render(request, "query_pages/blood_bank_query.html", {'b_banks': bbankList, 'opt': location_names})


# USER HOMEPAGE FUNCTIONS

def user_search_options(request):
    return render(request, 'homepage/Search_for_user.html')


def bloodbank_search_options(request):
    return render(request, 'homepage/Search_for_bloodbank.html')


def submit_changed_profile_user(request):
    first_name = request.POST['f_name']
    last_name = request.POST['l_name']
    phone_number = request.POST['phone']
    email = request.POST['email']
    blood_type = request.POST['blood_type']
    bio = request.POST['additional_details']

    dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
    conn = cx_Oracle.connect(user='MEDI_SHEBA', password='1234', dsn=dsn_tns)

    print(user_info['pk'])
    if first_name != "":
        c = conn.cursor()
        statement = "UPDATE MEDI_SHEBA.USERS SET FIRST_NAME = " + "\'" + first_name + "\'" + "WHERE USER_ID = " + str(
            user_info['pk'])
        c.execute(statement)
        conn.commit()
    else:
        print("First Name NOT CHANGED ")

    if last_name != "":
        c = conn.cursor()
        statement = "UPDATE MEDI_SHEBA.USERS SET LAST_NAME = " + "\'" + last_name + "\'" + "WHERE USER_ID = " + str(
            user_info['pk'])
        c.execute(statement)
        conn.commit()
    else:
        print("LAST Name NOT CHANGED ")

    if phone_number != "":
        c = conn.cursor()
        statement = "UPDATE MEDI_SHEBA.USERS SET PHONE = " + "\'" + phone_number + "\'" + "WHERE USER_ID = " + str(
            user_info['pk'])
        c.execute(statement)
        conn.commit()
    else:
        print("PHONE NOT CHANGED ")

    if email != "":
        c = conn.cursor()
        statement = "UPDATE MEDI_SHEBA.USERS SET EMAIL = " + "\'" + email + "\'" + "WHERE USER_ID = " + str(
            user_info['pk'])
        c.execute(statement)
        conn.commit()
    else:
        print("EMAIL NOT CHANGED ")

    if blood_type != "":
        c = conn.cursor()
        statement = "UPDATE MEDI_SHEBA.USERS SET BLOOD_GROUP = " + "\'" + blood_type + "\'" + "WHERE USER_ID = " + str(
            user_info['pk'])
        c.execute(statement)
        conn.commit()
    else:
        print("BLOOD NOT CHANGED ")

    '''
    UPDATE DICTIONARY HERE, CAUSE NOT UPDATING THE DICTIONARY WILL SHOW WRONG INFORMATION ON THE PAGES

    UPDATE EMAIL, FIRST NAME, LAST NAME


    '''

    '''
    TODO: HANDLE MULTI VALUE DICT KEY ERROR IF SOMETHING IS NOT GIVEN AS INPUT, SPECIALLY DROP DOWN BOXES 
    '''
    c = conn.cursor()
    statement = "SELECT USER_ID, FIRST_NAME, LAST_NAME,EMAIL from MEDI_SHEBA.USERS  WHERE USER_ID=" + str(
        user_info['pk'])
    c.execute(statement)
    if c:
        x = c.fetchone()
        id = x[0]
        f_name = x[1]
        l_name = x[2]
        email = x[3]
        user_info['pk'] = id
        user_info['f_name'] = f_name
        user_info['l_name'] = l_name
        user_info['email'] = email
    return redirect("user_home")


def user_edit_profile(request):
    # authentication added here
    if bool(user_info) and user_info['type'] == "user":
        dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
        conn = cx_Oracle.connect(user='MEDI_SHEBA', password='1234', dsn=dsn_tns)
        c = conn.cursor()
        statement = "SELECT HOSPITAL_NAME FROM MEDI_SHEBA.HOSPITAL"
        c.execute(statement)

        hospital_names = []

        for i in c:
            hospital_names.append(i[0])

        location_names = json_extractor.JsonExtractor('name').extract("HelperClasses/zilla_names.json")
        location_names.sort()

        return render(request, 'homepage/UserProfileEditor.html',
                      {'hospital_names': hospital_names, 'locations': location_names})

    else:
        return HttpResponse("NO ACCESS TO THIS PAGE")


def user_doctor_appointment(request):
    return HttpResponse("user doctor appointment")


def user_blood_bank_appointment(request):
    return HttpResponse("blood bank appointment")


def user_modify_appointment(request):
    return HttpResponse("user modify appointment")


def user_hospital_appointment(request):
    return HttpResponse("user hospital appointment")


def bloodbank_admin_edit_profile(request):
    return HttpResponse("etate kaaj kora lagbe")


def bloodbank_collection(request):
    return HttpResponse("etate kaaj kora lagbe")


def bloodbank_calender(request):
    return HttpResponse("etate kaaj kora lagbe")


def bloodbank_history(request):
    return HttpResponse("etate kaaj kora lagbe")


def bloodbank_all_appointments(request):
    return HttpResponse("blood banks appointment page")
