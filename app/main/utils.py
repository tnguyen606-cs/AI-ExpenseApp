from app import db


def get_count(q):
    count = db.select(db.func.count(q.id))
    return count
