import email

from src.models.entities.users import User


class ModelUser():

    @classmethod
    def login(self, db, user):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT * FROM users 
                    WHERE username = '{}'""".format(user.username)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row is not None:
                user = User(row[0], row[1], User.check_password(row[2], user.password), row[3])
                return user
            else:
                return None
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_by_id(self, db, id):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT id,username,fullname FROM users 
                    WHERE id = '{}'""".format(id)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row is not None:
                Logged_user = User(row[0], row[1], None, row[2])
                return Logged_user
            else:
                return None
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def register(self, db, user):
        cursor = db.connection.cursor()
        passw = user.password
        slqinsert = "INSERT INTO `users` (`id`, `username`, `password`, `fullname`) VALUES (0, '{}', '{}', " \
                    "'{}')".format(user.username, user.generate_pass(passw), user.fullname)
        cursor.execute(slqinsert)
        db.connection.commit()
        cursor.close()

    @classmethod
    def check_user(self, db, username):
        cursor = db.connection.cursor()
        cursor.execute('SELECT username FROM users WHERE username = %s', (str(username),))
        usuario = cursor.fetchone()
        return usuario

