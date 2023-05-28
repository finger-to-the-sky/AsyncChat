from .models import *
from .database import Base, engine, SessionLocal


class ServerStorage:
    def __init__(self):
        Base.metadata.create_all(engine)
        self.session = SessionLocal()

        self.session.query(ActiveUsers).delete()
        self.session.commit()

    def login(self, username, ip_address, port):
        """
        Метод подключения пользователя к мессенджеру.
        Если пользователь уже есть в БД, то обновить дату посещения иначе создать пользователя.
        Так же добавить данные об активности и истории.
        :param username:
        :param ip_address:
        :param port:
        :return:
        """
        print(username, ip_address, port)
        user = self.session.query(Users).filter_by(username=username).first()
        if user:
            user.last_login = datetime.now()
        else:
            user = Users(username=username)
            self.session.add(user)
            self.session.commit()

        new_active_user = ActiveUsers(ip_address=ip_address, port=port, login_time=datetime.now())
        self.session.add(new_active_user)
        history = History(username=username, date=datetime.now(), ip=ip_address, port=port)
        self.session.add(history)
        self.session.commit()

    def logout(self, username):
        """
        Метод отключения пользователя от мессенджера.
        Удаляет данные об активности пользователя
        :param username:
        :return:
        """
        user = self.session.query(Users).filter_by(username=username).first()
        self.session.query(ActiveUsers).filter_by(user_id=user.id).delete()
        self.session.commit()

    def users_list(self):
        """
        Получение всех пользователей в БД.
        :return:
        """
        query = self.session.query(
            Users.username,
            Users.last_login,
        )

        return query.all()

    def active_users_list(self):
        """
        Получение всех активных пользователей.
        :return:
        """
        query = self.session.query(
            Users.username,
            ActiveUsers.ip_address,
            ActiveUsers.port,
            ActiveUsers.login_time,
        )
        return query.all()

    def login_history(self, username=None):
        """
        Получение информации об истории посещения мессенджера.
        :param username:
        :return:
        """
        query = self.session.query(Users.username,
                                   History.date,
                                   History.ip,
                                   History.port
                                   )
        if username:
            query = query.filter(Users.username == username)
        return query.all()


if __name__ == '__main__':
    test_db = ServerStorage()
    # выполняем 'подключение' пользователя
    test_db.login('client_1', '192.168.1.4', 8888)
    test_db.login('client_2', '192.168.1.5', 7777)
    print(test_db.active_users_list())

    # выполняем 'отключение' пользователя
    test_db.logout('client_1')
    print(test_db.active_users_list())

    # запрашиваем историю входов по пользователю
    test_db.login_history('client_1')
    print(test_db.users_list())
