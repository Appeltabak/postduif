import hashlib
import uuid
import postduif


def register(username_val, password_val, email_val, location_val):
    salt_val = uuid.uuid4().hex.encode('utf-8')
    password_val_enc = password_val.encode('utf-8')
    password_hash = hashlib.sha512(password_val_enc + salt_val).hexdigest()

    usr = postduif.User(username=username_val, password=password_hash, salt=salt_val, email=email_val, location=location_val)
    postduif.session.add(usr)
    postduif.session.commit()


def pass_check(user_id, password):
    for user in postduif.session.query(postduif.User).filter(postduif.User.id == user_id):
        database_salt = user.salt
        database_hash = user.password
    password_val_enc = password.encode('utf-8')
    password_hash = hashlib.sha512(password_val_enc + database_salt).hexdigest()
    return password_hash == database_hash

# pswd.register("John D.", "Test", "e@mai.l", "0;0")
# print(pass_check(4, "Test"))


