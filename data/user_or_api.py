from sqlalchemy.orm.session import Session
from database.db import get_session
from database.db_table import User
from database.hash_password import Hash_Pass
from model.base_models import *

import random
from datetime import datetime, timedelta, date
from .jalali import *

hash = Hash_Pass()


#  check email is create account
def check_email(email, db: Session):
    email_valid = db.query(User).filter(User.email == email).first()

    if email_valid is None:
        return True
    else:
        return False

# check username is create account
def check_username(username, db: Session):
    email_valid = db.query(User).filter(User.username == username).first()

    if email_valid is None:
        return True
    else:
        return False


# unhash password from database
def unhash_pass_db(string):
    string = str(string)
    edit_dtr = string.replace("b'", "").replace('"', "").replace("'", "")
    byte_str = bytes(edit_dtr, encoding="utf-8")
    decrypted = hash.unhash_password(byte_str)
    byte_unhash = str(decrypted).replace("b'", "").replace("'", "")
    return byte_unhash


def token_user_login(token):
    token = str(token)
    edit_token = token.replace("b'", "").replace("'", "")    
    return edit_token

# create a new user
def create_user(users: User_Model, db: Session):

    message = {"status": "error"}

    if not check_username(users.username, db):
        message["status"] = "error"
        message["data"] = "The entered username already exists"
        return message

    elif not check_email(users.email, db):
        message["status"] = "error"
        message["data"] = "The entered email already exists"
        return message
    
    else:
        user = User(
            name = users.name,
            username = users.username,
            email = users.email,
            password = str(hash.hash_password(users.password))
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        message["status"] = "success"
        message["data"] = user
        return message
    


# login user with password
def login_user(users: Login_Model, db: Session):
    message = {"status": "error"}

    its_check_login = db.query(User).filter(User.username == users.username).first()

    if its_check_login is None:
        message["data"] = "login failed with username and password"
        return message
    
    if its_check_login.username == users.username:
        
        data = its_check_login
        # password is db
        password_db = its_check_login.password
        it_pass_unhash = unhash_pass_db(password_db)
        # passwword is enter user
        password_user = users.password

        if it_pass_unhash == password_user:
            random_int = random.randint(999, 99999)
            make_token_login = str(random_int) + data.username + data.email + str(random_int)
            token_login_user = hash.hash_password(make_token_login)
            token_login_user_show = token_user_login(token_login_user)
            
            # update token user
            its_check_login.token_user = token_login_user_show
            db.commit()

            message["status"] = "success"
            message["data"] = {"message": "login successfull", 
                               "user_id": data.id,
                               "username": data.username, 
                               "email": data.email,
                               "token_login": token_login_user_show
                               }
            
            return message

        else:
            message["data"] = "password is incorrect..."
            return message

    else:
        message["data"] = "user not found"
        return message



def login_user_by_token(users: Login_Model_Token, db: Session):
    message = {"status": "error"}


    token_db = db.query(User).filter(User.token_user == users.token).first()

    if token_db is None:
        message["data"] = "token not found"
        return message
    

    if token_db.token_user == users.token:
        message["status"] = "success"
        message["data"] = {"message": "token successfull", 
                               "user_id": token_db.id,
                               "username": token_db.username, 
                               "email": token_db.email,
                               "token_success": True
                               }
        
        return message

    else:
        message["data"] = "token already exists"
        return message
    

def pay_app(token: Login_Model_Token, day_pro: Pay_Enum , db: Session):
    message = {"status": "error"}

    find_token = db.query(User).filter(User.token_user == token.token).first()

    if find_token is None:
        message["data"] = "token not found"
        return message


    if find_token.token_user == token.token:

        # date now
        date_now = datetime.now()

        # date now and sum end date
        date_time_end = date_now + timedelta(days=int(day_pro))

        # date now to format 2023,5,5
        date_now_add_db = date(date_now.year, date_now.month, date_now.day)

        # date end to format 2023,5,5
        date_end_add_db = date(date_time_end.year, date_time_end.month, date_time_end.day)

        # add date pro to database
        find_token.date_buy = date_now_add_db
        find_token.date_end = date_end_add_db

        # iran date
        date_end_pe = gregorian_to_jalali(date_end_add_db.year, date_end_add_db.month, date_end_add_db.day)
        date_buy_pe = gregorian_to_jalali(find_token.date_buy.year, find_token.date_buy.month, find_token.date_buy.day)

        # day end 
        day_end = find_token.date_end - date_now_add_db

        # check if pro
        is_pro = False

        if date_now_add_db <= date_end_add_db:
            find_token.is_pro = True
            is_pro = True
        else:
            find_token.is_pro = False
            is_pro = False


        message["status"] = "success"
        message["data"] = {"message": f"buy successfull {day_pro} day", 
                               "user_id": find_token.id,
                               "username": find_token.username, 
                               "email": find_token.email,
                               "date_buy": {
                                        "date_buy_en": find_token.date_buy,
                                        "date_buy_pe": f"{date_buy_pe[0]}-{date_buy_pe[1]}-{date_buy_pe[2]}"
                                    },
                               "date_end": {
                                        "date_end_en": date_end_add_db,
                                         "date_end_pe": f"{date_end_pe[0]}-{date_end_pe[1]}-{date_end_pe[2]}"
                                    },
                               "days": day_end.days,
                               "is_pro_user": is_pro
                               }
        
        db.commit()
        return message

    else:
        message["data"] = "token already exists"
        return message



def info_user_account(token: Login_Model_Token, db: Session):
    message = {"status": "error"}

    find_token = db.query(User).filter(User.token_user == token.token).first()

    if find_token is None:
        message["data"] = "token not found"
        return message


    if find_token.token_user == token.token:

        # add date pro to database
        date_buy = find_token.date_buy
        date_end = find_token.date_end

        # iran date
        date_buy_pe = gregorian_to_jalali(date_buy.year, date_buy.month, date_buy.day)
        date_end_pe = gregorian_to_jalali(date_end.year, date_end.month, date_end.day)
        
        # day end 
        date_now = datetime.now()
        date_now_date = date(date_now.year, date_now.month, date_now.day)
        date_end_date = date(date_end.year, date_end.month, date_end.day)
        day_end = date_end_date - date_now_date


        # is pro user 
        if date_end >= date_buy:
            is_pro = True
        else:
            is_pro = False    

        message["status"] = "success"
        message["data"] = {"message": "info account successfull show", 
                               "user_id": find_token.id,
                               "name": find_token.name,
                               "username": find_token.username, 
                               "email": find_token.email,
                               "date_buy": {
                                        "date_buy_en": f"{date_buy.year}-{date_buy.month}-{date_buy.day}",
                                        "date_buy_pe": f"{date_buy_pe[0]}-{date_buy_pe[1]}-{date_buy_pe[2]}"
                                    },
                               "date_end": {
                                        "date_end_en": f"{date_end.year}-{date_end.month}-{date_end.day}",
                                         "date_end_pe": f"{date_end_pe[0]}-{date_end_pe[1]}-{date_end_pe[2]}"
                                    },
                               "days": day_end.days,
                               "is_pro_user": is_pro
                               }
        
        db.commit()
        return message

    else:
        message["data"] = "token already exists"
        return message