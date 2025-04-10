
from app import db

class BaseCRUD:
    @staticmethod
    def get_all(model):
        return model.query.all()

    @staticmethod
    def get_by_id(model, id):
        return model.query.get(id)

    @staticmethod
    def create(model, **kwargs):
        new_record = model(**kwargs)
        db.session.add(new_record)
        db.session.commit()
        return new_record

    @staticmethod
    def update(model, id, **kwargs):
        record = model.query.get(id)
        if record:
            for key, value in kwargs.items():
                setattr(record, key, value)
            db.session.commit()
            return record
        return None

    @staticmethod
    def delete(model, id):
        record = model.query.get(id)
        if record:
            db.session.delete(record)
            db.session.commit()
            return True
        return False