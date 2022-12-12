import datetime
from pony.orm import *
db = Database()


class Announcement(db.Entity):
    name = Required(str)
    surname = Required(str)
    age = Required(int)
    phonenumber = Required(str)
    bloodtype = Required(str)
    hospital = Required(str)
    district = Required(str)
    date = Required(datetime.datetime)
    note = Required(str)


class Subscriber(db.Entity):
    bloodtype = Required(str)
    district = Required(str)
    user_id = Required(str, unique=True)


db.bind(provider='postgres', user='bloodalert', password='bloodalert',
        host='localhost', database='bloodalert')

db.generate_mapping(create_tables=True, check_tables=True)
set_sql_debug(True)

'''Subscriber CRUD'''


@db_session
def get_subscriber(bloodtype: str, district: str) -> list:
    targets = Subscriber.select(
        lambda sub: sub.bloodtype == bloodtype and sub.district == district)[:]
    return list(targets)


@db_session
def add_subscriber(bloodtype: str, district: str, user_id: str) -> Subscriber:
    new_subscriber = Subscriber(
        bloodtype=bloodtype, district=district, user_id=user_id)
    return Subscriber


@db_session
def update_subscriber(req_user_id) -> list:
    user = Subscriber.select(lambda sub: sub.user_id == req_user_id)[:]
    return list(user)


@db_session
def remove_subscriber(user_id: str) -> None:
    Subscriber.select(lambda sub: sub.user_id == user_id).delete()
    # Subscriber(user_id=user_id).delete()
    return None


'''Announcement Related Functions'''


@db_session
def get_announcement(size: int = 5) -> list:
    targets = Announcement.select()
    list_targets = list(targets)[-1 * size:]
    return list_targets


@db_session
def add_annoucement(name: str, surname: str, age: int, phonenumber: str, bloodtype: str) -> Announcement:
    new_annoucement = Announcement(
        name=name, surname=surname, age=age, phonenumber=phonenumber, bloodtype=bloodtype)
    return Announcement


@db_session
def update_annoucement(req_user_id, req_data) -> Announcement:
    user = Announcement.get(user_id=req_user_id)
    # selected_user = select(subscribe for subscribe in  Subscriber if subscribe.user_id == req_user_id).get()
    user.set(**req_data)
    return user


@db_session
def remove_annoucement(user_id: str) -> Announcement:
    Announcement.select(lambda sub: sub.user_id == user_id).delete()
    # delete_annoucement = Announcement(user_id=user_id).delete()
    return ("success")
