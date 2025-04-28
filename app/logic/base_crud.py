
from operator import and_, or_
from app import db

class BaseCRUD:
    @staticmethod
    def get_all(model):
        return model.query.all() # return all table content

    @staticmethod
    def get_by_id(model, id):
        return model.query.get(id) # return row by id
    
    @staticmethod
    def create(model, **kwargs):
        new_record = model(**kwargs) # set the model with the attributes(kwargs)
        db.session.add(new_record)  # create a table 
        db.session.commit()
        return new_record  # returns the record in case of immediate access
    
    @staticmethod
    def get_row(model, **kwargs):
        return model.query.filter_by(**kwargs).first() #  get a single row based on the kwargs
    
    @staticmethod
    def get_all_records_by_filter(model, **kwargs):
        return model.query.filter_by(**kwargs).all() # get all rows based on the kwargs
    
    
    @staticmethod
    def get_first_record_by_filter(model, **kwargs):
        return model.query.filter_by(**kwargs).first() # getone row based on the kwargs
    @staticmethod
    def update(model, id, **kwargs):
        record = model.query.get(id) # get the record by id
        if record:
            for key, value in kwargs.items(): # go through the kwargs as a dictionary
                if value is not None:         # ensure there is a value passed in (refer to MenuLogic)
                    setattr(record, key, value) # set the new value to its key
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
    
    @staticmethod
    def get_records_by_date_range(model, column, start_date=None, end_date=None, **kwargs):
        query = model.query.filter_by(**kwargs) # build up the query only no data is returned 
        if start_date:
            query = query.filter(column >= start_date) # apply additional filters
        if end_date:
            query = query.filter(column <= end_date)
        return query.all() # get the data
    
    @staticmethod # get notification for either specific staff or for role based
    def get_staff_sensitive_notifications(model, staff_id, role_name):
        return model.query.filter(
            or_(
                model.staff_id == staff_id,
                and_(model.staff_id == None, model.role == role_name)
            )
        ).order_by(model.timestamp.desc()).all()