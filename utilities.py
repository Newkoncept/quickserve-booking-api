def create_new_id(item:list, id_key:str):
    # Check if item is an empty list
    if not item:
        return 1
    else:
        return getattr(item[-1], id_key) + 1


def retrieve_detail(items:list, id_key:str, id_value:str):
    if not items:
        return None
    
    for i in items:        
        if getattr(i, id_key) == id_value:
            return i