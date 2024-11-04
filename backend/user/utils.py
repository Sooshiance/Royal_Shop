import re


def checkUsername(username:str):
    
    pattern1 = r"09\d{9}"
    pattern2 = r"[^@]+@[^@]+\.[^@]+"

    if re.match(pattern1, username):
        return "phone"
    elif re.match(pattern2, username):
        return "email"
    else:
        return "not valid"


def sendPhoneOTP(user):
    pass


def sendEmailOTP(user):
    pass
