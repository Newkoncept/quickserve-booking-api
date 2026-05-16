def retrieve_details(db, model, id_key: str, id_value):
    column = getattr(model, id_key, None)

    if column is None:
        return None

    return db.query(model).filter(column == id_value).first()    