from django.db import models


# Create your models here.

class DoctorName:

    def __init__(self, id, name, phone, gender, specialization, hospital_name):
        self.id = id
        self.name = name
        self.phone = phone
        self.gender = gender
        self.specialization = specialization
        self.hospital_name = hospital_name

class  BloodBankList:

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
