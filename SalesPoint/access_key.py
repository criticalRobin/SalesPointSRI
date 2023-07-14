from datetime import datetime
import re


class AccessKey:
    current_date = datetime.now()
    current_date_string = current_date.strftime("%d%m%Y")
    receipt_type = "01"
    ruc = ""
    enviroment_type = "1"
    bussiness_code = ""
    emition_code = ""
    series = bussiness_code + emition_code
    sequential_number = ""
    numerical_code = "12345678"
    emition_type = "1"
    verification_digit = ""

    def __init__(self, ruc, bussiness_code, emition_code, sequuential_number):
        self.ruc = ruc
        self.bussiness_code = bussiness_code
        self.emition_code = emition_code
        self.sequential_number = sequuential_number

    def set_digit_verification(self, cdg48):
        if not cdg48.isdigit():
            return -1
        add = 0
        fac = 2
        for i in range(len(cdg48) - 1, -1, -1):
            if i == len(cdg48) - 1:
                add += int(cdg48[i]) * fac
            else:
                add += int(cdg48[i : i + 1]) * fac
            print(add)

            if fac == 7:
                fac = 2
            else:
                fac += 1

        dv = 11 - (add % 11)

        if dv == 10:
            return 1
        elif dv == 11:
            return 0

        return dv


# a = AccessKey("2110201101179", "001", "001", "000000001")
# print(a.set_digit_verification("211020110117921467390011002001000000001123456781"))

dni_regex = r"^\d{10}$"


def ecuadorian_dni_validator(dni):
    if re.match(dni_regex, dni):
        province = int(dni[0:2])
        if province >= 1 and province <= 24:
            return True
    return False

print(ecuadorian_dni_validator("1301234567"))
