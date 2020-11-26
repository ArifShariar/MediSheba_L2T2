import cx_Oracle
from django.db import models


# Create your models here.

class DoctorName:

    def __init__(self, id, name, phone, gender, specialization, location, hospital_name, doctor_id):
        hospital_full_name = hospital_name
        '''
                if hospital_name != "NONE":
            dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
            conn = cx_Oracle.connect(user='MEDI_SHEBA', password='1234', dsn=dsn_tns)
            c = conn.cursor()
            c.execute("SELECT HOSPITAL_NAME FROM MEDI_SHEBA.HOSPITAL WHERE HOSPITAL_ID = " + str(hospital_name))
            for row in c:
                hospital_full_name = row[0]
        '''

        self.id = id
        self.name = name
        self.phone = phone
        self.gender = gender
        self.specialization = specialization
        self.location = location
        self.hospital_name = hospital_full_name
        self.doctor_id = doctor_id


class BloodBankList:

    def __init__(self, id, name, a_plus, a_minus, b_plus, b_minus, o_plus, o_minus, ab_plus, ab_minus):
        self.id = id
        self.name = name
        self.a_plus = a_plus
        self.a_minus = a_minus
        self.b_plus = b_plus
        self.b_minus = b_minus
        self.o_plus = o_plus
        self.o_minus = o_minus
        self.ab_plus = ab_plus
        self.ab_minus = ab_minus


class HospitalName:

    def __init__(self, id, name, phone, location):
        self.id = id
        self.name = name
        self.phone = phone
        self.location = location


class doctor_infos:
    def __init__(self,first_name, last_name, phone, email, hospital_id, fees, specialization):
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.email = email
        self.hospital_id = hospital_id
        self.fees = fees
        self.specialization = specialization