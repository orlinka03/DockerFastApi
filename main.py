from fastapi import FastAPI, HTTPException, status

app = FastAPI()
items = []
items_id = 1

@app.get('/')
def root():
    return {'message': 'Hello World'}

@app.get('/items')
def get_items():
    if items:
        return items
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Item list is empty')

@app.get('/items/{id}')
def get_item(id: int):
    try:
        return items[id - 1]
    except Exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Item doesn\'t exist')

@app.post('/items')
def create_item(name: str, coast: float, in_stock: bool):
    global items_id
    item = {
        'id': items_id,
        'name': name,
        'coast': coast,
        'in_stock': in_stock
    }
    items_id += 1
    items.append(item)
    return item

@app.patch('/items')
def update_item(item_id: int, new_name: str = None, new_coast: str = None, in_stock: bool = None):
    try:
        if new_name:
            items[item_id -1]['name'] = new_name
        if new_coast:
            items[item_id - 1]['coast'] = new_coast
        if in_stock:
            items[item_id - 1]['in_stock'] = in_stock

        return items[item_id - 1]
    except Exception:
        HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Item doesn\'t exist')

@app.put('/items')
def update_full_item(item_id: int, new_name: str, new_coast: str, in_stock: bool):
    try:
        items[item_id - 1]['name'] = new_name
        items[item_id - 1]['coast'] = new_coast
        items[item_id - 1]['in_stock'] = in_stock

        return items[item_id - 1]
    except Exception:
        HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Item doesn\'t exist')

@app.delete('/items')
def delete_item(item_id: int):
    try:
        global items_id
        for index in range(item_id, len(items)):
            items[index]['id'] -= 1
        item = items.pop(item_id - 1)
        items_id -= 1
        return item
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'{ex}')
