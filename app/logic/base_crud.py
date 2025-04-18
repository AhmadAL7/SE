
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