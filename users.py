import secrets
import os
from db import db
from flask import render_template, redirect, request, session, flash
from werkzeug.security import check_password_hash, generate_password_hash

def login(username, password):
    sql = "SELECT id, password, username, admin FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return False
    if not check_password_hash(user.password, password):
        return False
    else:
        if check_password_hash(user.password, password):
            session["csrf_token"]= secrets.token_hex(16)
            session["user_id"] = user.id
            session["user_name"] = user.username
            session["admin"] = user.admin
            return True
        else:
            return False


def register(username, password, admin):
    hash_value = generate_password_hash(password)
    try:
        sql = "INSERT INTO users (admin, username, password) VALUES (':admin', :username, :password);"
        db.session.execute(sql, {"admin": admin, "username":username, "password":hash_value})
        db.session.commit()
    except:
        return False
    return login(username, password)
    
def user_id():
    return session.get("user_id", -1)

def logout():
    del session["user_id"]
    del session["user_name"]
    del session["admin"]
    del session["csrf_token"]    


def username():
    result = db.session.execute("SELECT username FROM users WHERE id=:id", {"id": session.get("user_id", -1)})
    name = str(result.fetchone())[2:-3]
    return name

def get_admin_status():
    result = db.session.execute("SELECT admin FROM users WHERE id=:id", {"id": session.get("user_id", -1)})
    admin = str(result.fetchone())[1:-2]
    return admin
