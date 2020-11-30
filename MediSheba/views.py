from django.http import HttpResponse
from django.shortcuts import render, redirect
import cx_Oracle

import HelperClasses.encryptPass as decoder_encoder
from HelperClasses import json_extractor

from .models import DoctorName
from .models import BloodBankList
from .models import HospitalName
from .models import HospitalCabinName
from .models import CabinName

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
    return render(request, 'homepage/HospitalAdminHome.html', {'name': user_info['f_name'] + ' ' + user_info['l_name']})


def blood_bank_admin_home(request):
    return render(request, 'homepage/Blood_Bank_Home.html', {'name': user_info['f_name'] + ' ' + user_info['l_name']})


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

        return render(request, 'profile_editor/DoctorProfileEditor.html',
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
        return render(request, 'schedule_editor/calendar2.html')
    else:
        return HttpResponse("NO ACCESS")


def doctor_view_records(request):
    if bool(user_info) and user_info['type'] == 'doctor':
        return render(request, 'homepage/records_for_doctor_table.html')
    else:
        return HttpResponse(" NO ACCESS")


def doctor_user_history_from_doctor(request):
    return render(request, 'appointment_history_pages/doctor_history/doctor_user_history.html')


def doctor_hospital_history_from_doctor(request):
    return render(request, 'appointment_history_pages/doctor_history/doctor_hospital_history.html')


def doctor_blood_bank_history_from_doctor(request):
    return render(request, 'appointment_history_pages/doctor_history/doctor_blood_bank_history.html')


def doctor_change_schedule(request):
    if bool(user_info) and user_info['type'] == 'doctor':
        return render(request, 'schedule_editor/AddSchedule.html')
    else:
        return HttpResponse("No ACCESS")


def logout(request):
    user_info.clear()
    return redirect("login")


def filter_search_doctor(request):
    specialization = request.POST.get('select_specialization', 'No Preferences')
    gender_return = request.POST.get('select_gender', 'No Preferences')
    area = request.POST.get('select_area', 'No Preferences')
    gender = gender_return
    if gender_return == "Male":
        gender = "M"
    elif gender_return == "Female":
        gender = "F"
    statement = ""
    if specialization == "No Preferences" and gender == "No Preferences" and area == "No Preferences":
        if user_info['type'] == "doctor":
            return redirect(search_doctors_by_doctor)
        elif user_info['type'] == "user":
            return redirect(search_doctors_by_user)
        elif user_info['type'] == "hospital_admin":
            return redirect(search_doctors_by_hospitals)
        elif user_info['type'] == "blood_bank_admin":
            return redirect(search_doctors_by_bloodbank)

    elif specialization == "No Preferences":
        if gender == "No Preferences":
            statement = "SELECT FIRST_NAME || ' ' || LAST_NAME,PHONE, GENDER, SPECIALIZATION, LOCATION, NVL(HOSPITAL_ID,-1), DOCTOR_ID FROM MEDI_SHEBA.DOCTOR WHERE LOCATION= " + "\'" + area + "\'"
        elif area == "No Preferences":
            statement = "SELECT FIRST_NAME || ' ' || LAST_NAME,PHONE, GENDER, SPECIALIZATION, LOCATION, NVL(HOSPITAL_ID,-1), DOCTOR_ID FROM MEDI_SHEBA.DOCTOR WHERE GENDER = " + "\'" + gender + "\'"
        else:
            statement = "SELECT FIRST_NAME || ' ' || LAST_NAME,PHONE, GENDER, SPECIALIZATION, LOCATION, NVL(HOSPITAL_ID,-1), DOCTOR_ID FROM MEDI_SHEBA.DOCTOR WHERE GENDER = " + "\'" + gender + "\'" + " AND  LOCATION = " + "\'" + area + "\'"

    elif gender == "No Preferences":
        if specialization == "No Preferences":
            statement = "SELECT FIRST_NAME || ' ' || LAST_NAME,PHONE, GENDER, SPECIALIZATION, LOCATION, NVL(HOSPITAL_ID,-1), DOCTOR_ID FROM MEDI_SHEBA.DOCTOR WHERE LOCATION = " + "\'" + area + "\'"
        elif area == "No Preferences":
            statement = "SELECT FIRST_NAME || ' ' || LAST_NAME,PHONE, GENDER, SPECIALIZATION, LOCATION, NVL(HOSPITAL_ID,-1), DOCTOR_ID FROM MEDI_SHEBA.DOCTOR WHERE SPECIALIZATION = " + "\'" + specialization + "\'"
        else:
            statement = "SELECT FIRST_NAME || ' ' || LAST_NAME,PHONE, GENDER, SPECIALIZATION, LOCATION, NVL(HOSPITAL_ID,-1), DOCTOR_ID FROM MEDI_SHEBA.DOCTOR WHERE LOCATION = " + "\'" + area + "\'" + " AND SPECIALIZATION =" + "\'" + specialization + "\'"
    elif area == "No Preferences":
        if specialization == "No Preferences":
            statement = "SELECT FIRST_NAME || ' ' || LAST_NAME,PHONE, GENDER, SPECIALIZATION, LOCATION, NVL(HOSPITAL_ID,-1), DOCTOR_ID FROM MEDI_SHEBA.DOCTOR WHERE GENDER= " + "\'" + gender + "\'"
        elif gender == "No Preferences":
            statement = "SELECT FIRST_NAME || ' ' || LAST_NAME,PHONE, GENDER, SPECIALIZATION, LOCATION, NVL(HOSPITAL_ID,-1), DOCTOR_ID FROM MEDI_SHEBA.DOCTOR WHERE SPECIALIZATION= " + "\'" + specialization + "\'"
        else:
            statement = "SELECT FIRST_NAME || ' ' || LAST_NAME,PHONE, GENDER, SPECIALIZATION, LOCATION, NVL(HOSPITAL_ID,-1), DOCTOR_ID FROM MEDI_SHEBA.DOCTOR WHERE SPECIALIZATION= " + "\'" + specialization + "\'" + " AND GENDER = " + "\'" + gender + "\'"

    location_names = json_extractor.JsonExtractor('name').extract("HelperClasses/zilla_names.json")
    location_names.sort()
    specialization_options = []
    docList = []

    # print(statement)
    dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
    conn = cx_Oracle.connect(user='MEDI_SHEBA', password='1234', dsn=dsn_tns)
    c = conn.cursor()
    c.execute(statement)
    index = 1
    for row in c:
        docList.append(DoctorName(index, row[0], row[1], row[2], row[3], row[4], row[5], row[6]))
        index = index + 1
    c.execute("SELECT DISTINCT SPECIALIZATION FROM MEDI_SHEBA.DOCTOR")
    for row in c:
        specialization_options.append(row[0])
    conn.close()
    return render(request, 'query_pages/query_page_for_doctors/doctor_custom_query.html',
                  {'doc': docList, 'opt': location_names, 'specialization': specialization_options})


def custom_search_for_doctor(request):
    if bool(user_info) and user_info['type'] == 'doctor':
        return filter_search_doctor(request)
    else:
        return HttpResponse("No Access")


def custom_search_for_doctor_by_user(request):
    if bool(user_info) and user_info['type'] == "user":
        return filter_search_doctor(request)
    else:
        return HttpResponse("NO ACCESS")


def custom_search_for_doctor_by_hospital_admin(request):
    if bool(user_info) and user_info['type'] == "hospital_admin":
        return filter_search_doctor(request)
    else:
        return HttpResponse("NO ACCESS")


def custom_search_for_doctor_by_blood_bank_admin(request):
    if bool(user_info) and user_info['type'] == "blood_bank_admin":
        return filter_search_doctor(request)
    else:
        return HttpResponse("NO ACCESS")


def search_doctors_by_doctor(request):
    return see_doctors(request)


def search_doctors_by_user(request):
    return see_doctors(request)


def search_doctors_by_bloodbank(request):
    return see_doctors(request)


def see_doctors(request):
    location_names = json_extractor.JsonExtractor('name').extract("HelperClasses/zilla_names.json")
    location_names.sort()

    specialization = []

    docList = []

    dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
    conn = cx_Oracle.connect(user='MEDI_SHEBA', password='1234', dsn=dsn_tns)
    c = conn.cursor()
    c.execute(
        "SELECT FIRST_NAME || ' ' || LAST_NAME,PHONE, GENDER, SPECIALIZATION, LOCATION, NVL(HOSPITAL_ID,-1), DOCTOR_ID "
        "from MEDI_SHEBA.DOCTOR")
    index = 1
    for row in c:
        docList.append(
            DoctorName(index, row[0], row[1], row[2], row[3], row[4], row[5],
                       row[6]))  # DoctorName is defined in models.py
        index = index + 1

    c.execute("SELECT DISTINCT SPECIALIZATION FROM MEDI_SHEBA.DOCTOR")
    for row in c:
        specialization.append(row[0])

    conn.close()

    return render(request, "query_pages/query_page_for_doctors/doctor_query.html",
                  {'doc': docList, 'opt': location_names, 'specialization': specialization})


'''

  cabin starts
  
'''


def doctor_search_cabin(request):
    return see_hospital_cabins(request)


def custom_search_for_cabin(request):
    if bool(user_info) and user_info['type'] == 'doctor':
        return filter_search_cabin(request)
    else:
        return HttpResponse("No Access")


def filter_search_cabin(request):
    return HttpResponse("No Access")


def see_hospital_cabins(request):
    location_names = json_extractor.JsonExtractor('name').extract("HelperClasses/zilla_names.json")
    location_names.sort()

    hospitalcabinList = []

    dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
    conn = cx_Oracle.connect(user='MEDI_SHEBA', password='1234', dsn=dsn_tns)
    c = conn.cursor()
    c.execute("SELECT HOSPITAL_NAME, LOCATION ,AVAILABLE_CABIN , HOSPITAL_ID from MEDI_SHEBA.HOSPITAL")
    index = 1
    for row in c:
        hospitalcabinList.append(HospitalCabinName(index, row[0], row[1], row[2], row[3]))
        index = index + 1

    conn.close()
    return render(request, "query_pages/query_page_for_doctors/cabin_query.html",
                  {'cab': hospitalcabinList, 'opt': location_names})


def see_specific_hospital_cabin_details(request):
    hospital_id = request.POST['hospital_id']
    dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
    conn = cx_Oracle.connect(user='MEDI_SHEBA', password='1234', dsn=dsn_tns)
    c = conn.cursor()

    cabinList = []
    c.execute(
        "SELECT PRICE, CATEGORY, IS_AVAILABLE, HOSPITAL_ID FROM MEDI_SHEBA.CABIN WHERE HOSPITAL_ID = " + str(
            hospital_id))

    index = 1
    for row in c:
        cabinList.append(CabinName(index, row[0], row[1], row[2], row[3]))
        index = index + 1

    conn.close()
    return render(request, "detail_showing_pages/hospital_cabin_details.html",
                  {'cab': cabinList})


'''
  cabin ends
  
'''


def see_specific_doctor_details(request):
    doctor_id = request.POST['doctor_id']
    dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
    conn = cx_Oracle.connect(user='MEDI_SHEBA', password='1234', dsn=dsn_tns)
    c = conn.cursor()

    statement = "SELECT FIRST_NAME, LAST_NAME, PHONE, LOCATION, EMAIL, NVL(HOSPITAL_ID,-1), FEES, SPECIALIZATION FROM MEDI_SHEBA.DOCTOR WHERE DOCTOR_ID = " + str(
        doctor_id)
    c.execute(statement)

    first_name = ""
    last_name = ""
    phone = ""
    location = ""
    email = ""
    hospital_id = ""
    fees = ""
    specialization = ""
    for row in c:
        first_name = row[0]
        last_name = row[1]
        phone = row[2]
        location = row[3]
        email = row[4]
        hospital_id = row[5]
        fees = row[6]
        specialization = row[7]
    hospital_full_name = ""

    if hospital_id != -1:
        dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
        conn = cx_Oracle.connect(user='MEDI_SHEBA', password='1234', dsn=dsn_tns)
        c = conn.cursor()
        c.execute("SELECT HOSPITAL_NAME FROM MEDI_SHEBA.HOSPITAL WHERE HOSPITAL_ID = " + str(hospital_id))
        for row in c:
            hospital_full_name = row[0]
    else:
        hospital_full_name = "NONE"

    return render(request, "detail_showing_pages/see_doctors_details.html",
                  {'name': first_name + " " + last_name, 'first_name': first_name,
                   'last_name': last_name, 'phone': phone, 'location': location, 'email': email,
                   'hospital_name': hospital_full_name, 'fees': fees, 'specialization': specialization})


def submit_appointment(request):
    HttpResponse("Appointment sent to doctor")


# USERS


# Hospital

# TODO: pantha write code here
def see_doctors_of_specific_hospital(request):
    location_names = json_extractor.JsonExtractor('name').extract("HelperClasses/zilla_names.json")
    location_names.sort()
    hospital_id = request.POST['hospital_id_for_doctor']
    specialization = []

    docList = []

    dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
    conn = cx_Oracle.connect(user='MEDI_SHEBA', password='1234', dsn=dsn_tns)
    c = conn.cursor()
    c.execute(
        "SELECT FIRST_NAME || ' ' || LAST_NAME,PHONE, GENDER, SPECIALIZATION, LOCATION, NVL(HOSPITAL_ID,-1), DOCTOR_ID FROM MEDI_SHEBA.DOCTOR WHERE HOSPITAL_ID = " + str(
            hospital_id))
    index = 1
    for row in c:
        docList.append(
            DoctorName(index, row[0], row[1], row[2], row[3], row[4], row[5],
                       row[6]))  # DoctorName is defined in models.py
        index = index + 1

    c.execute("SELECT DISTINCT SPECIALIZATION FROM MEDI_SHEBA.DOCTOR")
    for row in c:
        specialization.append(row[0])

    conn.close()

    return render(request, "query_pages/query_page_for_doctors/doctor_query.html",
                  {'doc': docList, 'opt': location_names, 'specialization': specialization})


def see_specific_hospital_details(request):
    hospital_id = request.POST['hospital_id']
    hospital_id_for_doctor = hospital_id
    dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
    conn = cx_Oracle.connect(user='MEDI_SHEBA', password='1234', dsn=dsn_tns)
    c = conn.cursor()

    c.execute(
        "SELECT HOSPITAL_NAME, PHONE, LOCATION, EMAIL FROM MEDI_SHEBA.HOSPITAL WHERE HOSPITAL_ID = " + str(hospital_id))

    hospital_name = ""
    phone = ""
    location = ""
    email = ""
    hospital_id = ""

    for row in c:
        hospital_name = row[0]
        phone = row[1]
        location = row[2]
        email = row[3]

    return render(request, "detail_showing_pages/see_hospital_details.html",
                  {'name': hospital_name,
                   'phone': phone, 'location': location, 'email': email,
                   'hospital_id_for_doctor': hospital_id_for_doctor
                   })


def custom_search_for_hospital_by_doctor(request):
    if bool(user_info) and user_info['type'] == 'doctor':
        return filter_search_hospital(request)
    else:
        return HttpResponse("No Access")


def custom_search_for_hospital_by_bloodbank(request):
    if bool(user_info) and user_info['type'] == 'blood_bank_admin':
        return filter_search_hospital(request)
    else:
        return HttpResponse("No Access")


def custom_search_for_hospital_by_hospital_admin(request):
    if bool(user_info) and user_info['type'] == 'hospital_admin':
        return filter_search_hospital(request)
    else:
        return HttpResponse("No Access")


def custom_search_for_hospital_by_user(request):
    if bool(user_info) and user_info['type'] == 'user':
        return filter_search_hospital(request)
    else:
        return HttpResponse("No Access")


def filter_search_hospital(request):
    area = request.POST.get('select_area', 'No Preferences')

    statement = ""
    if area == "No Preferences":
        if user_info['type'] == "doctor":
            return redirect(search_hospitals_by_doctor)
        elif user_info['type'] == "user":
            return redirect(search_hospitals_by_users)
        elif user_info['type'] == "hospital_admin":
            return redirect(search_hospitals_by_hospitals)
        elif user_info['type'] == "blood_bank_admin":
            return redirect(search_hospitals_by_bloodbank)

    else:
        statement = "SELECT HOSPITAL_NAME,PHONE, LOCATION, HOSPITAL_ID FROM MEDI_SHEBA.HOSPITAL WHERE LOCATION = " + "\'" + area + "\'"

    location_names = json_extractor.JsonExtractor('name').extract("HelperClasses/zilla_names.json")
    location_names.sort()
    hospitalList = []

    dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
    conn = cx_Oracle.connect(user='MEDI_SHEBA', password='1234', dsn=dsn_tns)
    c = conn.cursor()
    c.execute(statement)
    index = 1
    for row in c:
        hospitalList.append(HospitalName(index, row[0], row[1], row[2], row[3]))
        index = index + 1

    conn.close()
    if user_info['type'] == "doctor":
        return render(request, "query_pages/query_page_for_doctors/hospital_custom_query.html",
                      {'hos': hospitalList, 'opt': location_names})
    elif user_info['type'] == "user":
        return render(request, "query_pages/query_page_for_users/hospital_custom_query.html",
                      {'hos': hospitalList, 'opt': location_names})
    elif user_info['type'] == "hospital_admin":
        return render(request, "query_pages/query_page_for_hospital_admin/hospital_custom_query.html",
                      {'hos': hospitalList, 'opt': location_names})
    elif user_info['type'] == "blood_bank_admin":
        return render(request, "query_pages/query_page_for_blood_bank_admin/hospital_custom_query.html",
                      {'hos': hospitalList, 'opt': location_names})


def search_hospitals_by_doctor(request):
    return see_hospitals(request)


def search_hospitals_by_users(request):
    return see_hospitals(request)


def search_hospitals_by_bloodbank(request):
    return see_hospitals(request)


def see_hospitals(request):
    location_names = json_extractor.JsonExtractor('name').extract("HelperClasses/zilla_names.json")
    location_names.sort()

    hospitalList = []

    dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
    conn = cx_Oracle.connect(user='MEDI_SHEBA', password='1234', dsn=dsn_tns)
    c = conn.cursor()
    c.execute("SELECT HOSPITAL_NAME,PHONE,LOCATION , HOSPITAL_ID from MEDI_SHEBA.HOSPITAL")
    index = 1
    for row in c:
        hospitalList.append(HospitalName(index, row[0], row[1], row[2], row[3]))  # HospitalName is defined in models.py
        index = index + 1
        '''print(row[2])'''
    conn.close()

    if user_info['type'] == "doctor":
        return render(request, "query_pages/query_page_for_doctors/hospital_query.html",
                      {'hos': hospitalList, 'opt': location_names})
    elif user_info['type'] == "user":
        return render(request, "query_pages/query_page_for_users/hospital_custom_query.html",
                      {'hos': hospitalList, 'opt': location_names})
    elif user_info['type'] == "hospital_admin":
        return render(request, "query_pages/query_page_for_hospital_admin/hospital_custom_query.html",
                      {'hos': hospitalList, 'opt': location_names})
    elif user_info['type'] == "blood_bank_admin":
        return render(request, "query_pages/query_page_for_blood_bank_admin/hospital_query.html",
                      {'hos': hospitalList, 'opt': location_names})


# Blood_Bank


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

        return render(request, 'profile_editor/UserProfileEditor.html',
                      {'hospital_names': hospital_names, 'locations': location_names})

    else:
        return HttpResponse("NO ACCESS TO THIS PAGE")


def user_search_cabin(request):
    return HttpResponse("View Cabins")


def user_doctor_appointment(request):
    return render(request, 'appointment_history_pages/user_history/doctor/doctor_appointment_options.html')


def past_appointment_of_doctor_by_user(request):
    return HttpResponse("Past appointment")


def upcoming_appointment_of_doctor_by_user(request):
    return HttpResponse("Upcoming appointment")


def pending_appointment_of_doctor_by_user(request):
    return HttpResponse("Pending appointment")


def user_blood_bank_appointment(request):
    return render(request, 'appointment_history_pages/user_history/blood_bank/bloodbank_appointment_options.html')


def user_hospital_appointment(request):
    return render(request, 'appointment_history_pages/user_history/hospital/hospital_appointment_options.html')


def past_appointment_of_hospital_by_user(request):
    return HttpResponse("Past hospital appointment")


def upcoming_appointment_of_hospital_by_user(request):
    return HttpResponse("upcoming hospital appointment")


def pending_appointment_of_hospital_by_user(request):
    return HttpResponse("pending hospital appointment")


def user_modify_appointment(request):
    return HttpResponse("user modify appointment")


# BLOOD BANK ADMIN
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


# functions for hospital admin and management


def hospital_search_options(request):
    return render(request, 'homepage/search_for_hospitals.html')


def hospital_admin_edit_profile(request):
    # authentication added here
    if bool(user_info) and user_info['type'] == "hospital_admin":
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

        return render(request, 'profile_editor/HospitalProfileEditor.html',
                      {'hospital_names': hospital_names, 'locations': location_names})

    else:
        return HttpResponse("NO ACCESS TO THIS PAGE")


def submit_changed_profile_hospital(request):
    if bool(user_info) and user_info['type'] == 'hospital_admin':
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
            statement = "UPDATE MEDI_SHEBA.HOSPITAL SET FIRST_NAME = " + "\'" + first_name + "\'" + "WHERE HOSPITAL_ID = " + str(
                user_info['pk'])
            c.execute(statement)
            conn.commit()
        else:
            print("First Name NOT CHANGED ")

        if last_name != "":
            c = conn.cursor()
            statement = "UPDATE MEDI_SHEBA.HOSPITAL SET LAST_NAME = " + "\'" + last_name + "\'" + "WHERE HOSPITAL_ID = " + str(
                user_info['pk'])
            c.execute(statement)
            conn.commit()
        else:
            print("LAST Name NOT CHANGED ")

        if phone_number != "":
            c = conn.cursor()
            statement = "UPDATE MEDI_SHEBA.HOSPITAL SET PHONE = " + "\'" + phone_number + "\'" + "WHERE HOSPITAL_ID = " + str(
                user_info['pk'])
            c.execute(statement)
            conn.commit()
        else:
            print("PHONE NOT CHANGED ")

        if location != "":
            c = conn.cursor()
            statement = "UPDATE MEDI_SHEBA.HOSPITAL SET LOCATION = " + "\'" + location + "\'" + "WHERE HOSPITAL_ID = " + str(
                user_info['pk'])
            c.execute(statement)
            conn.commit()
        else:
            print("LOCATION NOT CHANGED ")

        if email != "":
            c = conn.cursor()
            statement = "UPDATE MEDI_SHEBA.HOSPITAL SET EMAIL = " + "\'" + email + "\'" + "WHERE HOSPITAL_ID = " + str(
                user_info['pk'])
            c.execute(statement)
            conn.commit()
        else:
            print("EMAIL NOT CHANGED ")

        if blood_type != "":
            c = conn.cursor()
            statement = "UPDATE MEDI_SHEBA.DOCTOR SET BLOOD_GROUP = " + "\'" + blood_type + "\'" + "WHERE HOSPITAL_ID = " + str(
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
            statement = "UPDATE MEDI_SHEBA.DOCTOR SET HOSPITAL_ID = " + str(hospital_id) + " WHERE HOSPITAL_ID = " \
                        + str(user_info['pk'])
            c.execute(statement)
            conn.commit()
        else:
            print("HOSPITAL NOT CHANGED ")

        if fee != "":
            c = conn.cursor()
            statement = "UPDATE MEDI_SHEBA.DOCTOR SET FEES = " + fee + " WHERE HOSPITAL_ID = " + str(
                user_info['pk'])
            c.execute(statement)
            conn.commit()
        else:
            print("FEES NOT CHANGED ")

        if specialization != "":
            c = conn.cursor()
            statement = "UPDATE MEDI_SHEBA.DOCTOR SET SPECIALIZATION = " + "\'" + specialization + "\'" \
                        + " WHERE HOSPITAL_ID = " + str(user_info['pk'])
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
        statement = "SELECT HOSPITAL_ID, FIRST_NAME, LAST_NAME,EMAIL from MEDI_SHEBA.HOSPITAL  WHERE HOSPITAL_ID=" + str(
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
        return redirect("hospital_admin_home")
    else:
        return HttpResponse("Access not granted")


def hospital_admin_view_appointments(request):
    return HttpResponse("Hospital admin view appointments here")


def hospital_admin_view_schedule(request):
    return HttpResponse("Hospital admin view schedule")


def hospital_admin_available_cabin(request):
    return HttpResponse("View Cabins")


def hospital_admin_view_records(request):
    return HttpResponse("Hospital admin view records")


def search_doctors_by_hospitals(request):
    return see_doctors(request)


def search_hospitals_by_hospitals(request):
    return see_hospitals(request)


# TODO:bloodbank custom search

def see_blood_banks(request):
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

    statement = "SELECT NAME, A_POS, A_NEG, B_POS, B_NEG, O_POS, O_NEG, AB_POS, AB_NEG,BLOOD_BANK_ID,LOCATION FROM MEDI_SHEBA.BLOOD_BANK"
    c.execute(statement)

    index = 1
    for row in c:
        bbankList.append(
            BloodBankList(index, row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9],
                          row[10]))
        index = index + 1
    conn.close()

    return render(request, "query_pages/query_page_for_doctors/bb_query.html",
                  {'b_banks': bbankList, 'opt': location_names})


def search_blood_banks_by_hospital_admin(request):
    return see_blood_banks(request)


def search_blood_banks_by_doctor(request):
    return see_blood_banks(request)


def search_blood_banks_by_user(request):
    return see_blood_banks(request)


def search_blood_banks_by_bloodbank(request):
    return see_blood_banks(request)


def custom_search_for_bloodbank_by_doctor(request):
    if bool(user_info) and user_info['type'] == 'doctor':
        return filter_search_bloodbank(request)
    else:
        return HttpResponse("No Access")


def filter_search_bloodbank(request):
    area = request.POST.get('select_area', 'No Preferences')
    blood_group = request.POST.get('blood_group', 'No Preferences')

    blood_type_db = ""
    if blood_group == "A+":
        blood_type_db = "A_POS"
    elif blood_group == "A-":
        blood_type_db = "A_NEG"
    elif blood_group == "B+":
        blood_type_db = "B_POS"
    elif blood_group == "B-":
        blood_type_db = "B_NEG"
    elif blood_group == "O+":
        blood_type_db = "O_POS"
    elif blood_group == "O-":
        blood_type_db = "O_NEG"
    elif blood_group == "AB+":
        blood_type_db = "AB_POS"
    elif blood_group == "AB-":
        blood_type_db = "AB_NEG"

    statement = ""
    if area == "No Preferences" and blood_group == "No Preferences":
        if user_info['type'] == "doctor":
            return redirect(search_blood_banks_by_doctor)
        elif user_info['type'] == "user":
            return redirect(search_blood_banks_by_user)
        elif user_info['type'] == "hospital_admin":
            return redirect(search_blood_banks_by_hospital_admin)
        elif user_info['type'] == "blood_bank_admin":
            return redirect(search_blood_banks_by_bloodbank)

    else:
        if blood_group == "No Preferences":
            statement = "SELECT NAME, A_POS, A_NEG, B_POS, B_NEG, O_POS, O_NEG, AB_POS, AB_NEG,BLOOD_BANK_ID,LOCATION FROM MEDI_SHEBA.BLOOD_BANK WHERE LOCATION = " + "\'" + area + "\'"

        elif area == "No Preferences":

            statement = "SELECT NAME, A_POS, A_NEG, B_POS, B_NEG, O_POS, O_NEG, AB_POS, AB_NEG,BLOOD_BANK_ID,LOCATION FROM MEDI_SHEBA.BLOOD_BANK ORDER BY  " + blood_type_db + " DESC NULLS LAST"

        else:
            statement = "SELECT NAME, A_POS, A_NEG, B_POS, B_NEG, O_POS, O_NEG, AB_POS, AB_NEG,BLOOD_BANK_ID,LOCATION FROM MEDI_SHEBA.BLOOD_BANK WHERE LOCATION = " + area + " ORDER BY  " + blood_type_db + " DESC NULLS LAST"

    location_names = json_extractor.JsonExtractor('name').extract("HelperClasses/zilla_names.json")
    location_names.sort()
    bbList = []
    # print(blood_group)
    dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
    conn = cx_Oracle.connect(user='MEDI_SHEBA', password='1234', dsn=dsn_tns)
    c = conn.cursor()
    c.execute(statement)
    index = 1
    for row in c:
        bbList.append(
            BloodBankList(index, row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[10],
                          row[10]))
        index = index + 1

    conn.close()

    statement = ""
    if user_info['type'] == "doctor":
        return render(request, "query_pages/query_page_for_doctors/bb_custom_query.html",
                      {'b_banks': bbList, 'opt': location_names})
    elif user_info['type'] == "user":
        return HttpResponse("b bank custom search user")
        # return render(request, "query_pages/query_page_for_users/hospital_custom_query.html", {'hos': hospitalList, 'opt': location_names})

    elif user_info['type'] == "hospital_admin":
        return HttpResponse("b bank custom search hospital admin")
        # return render(request, "query_pages/query_page_for_hospital_admin/hospital_custom_query.html",{'hos': hospitalList, 'opt': location_names})
    elif user_info['type'] == "blood_bank_admin":
        return HttpResponse("b bank custom search b bank admin")
        # return render(request, "query_pages/query_page_for_blood_bank_admin/hospital_custom_query.html",{'hos': hospitalList, 'opt': location_names})
