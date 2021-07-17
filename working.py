from os import name
from fastapi import FastAPI, Path, Query, HTTPException, status
from typing import Optional
from pydantic import BaseModel


class Item(BaseModel):
    name: str
    price: float
    brand: Optional[str] = None


class UpdateItem(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    brand: Optional[str] = None

# An endpoint is the point of entry in communication channel
# where a server and an API meets


app = FastAPI()

inventory = {}


@app.get("/get-item/{item_id}")
def get_item(item_id: int = Path(None, description="The ID of the item you want to see.", gt=0)):
    return inventory[item_id]


# This has endpoint like - /get-by-name?name=Milk without the test parameter
# Right now this {@name} is a required parameter when none is not applied
# Now this name parameter becomes optional
# When having multiple arguments in get function the endpoint looks like /get-by-name/test=2&name=Milk
@app.get("/get-by-name")
def get_item_by_name(*, name: Optional[str] = None, test: int):
    for item_id in inventory:
        if inventory[item_id]["name"] == name:
            return inventory[item_id]
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Data not found")


# To have query as well as path parameters
# Here, query parameters are name, test & path parameters are item_id
# The endpoint looks like this /get-by-name/1?test=2&name=Milk
@app.get("/get-by-name/{item_id}")
def get_item_by_name_and_id(*, item_id: int = Path(None, description="This will take a name and an id"),
                            name: Optional[str] = None, test: Optional[int] = None):
    for item_id in inventory:
        if inventory[item_id].name == name:
            return inventory[item_id]
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Data not found")


# Now we will create an item and add it to the API
@app.post("/create-item/{item_id}")
def create_item(item_id: int, item: Item):
    if item_id in inventory:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Item ID already exists")

    inventory[item_id] = item
    return inventory[item_id]


""" Now we will update a current item in the API
    Since Item class took both name and price as required fields, it would ask
    both of them even if we wanted to change just one of them
    for that, we made a new class having same arguments, just that all of them are optional"""


@app.put("/update-item/{item_id}")
def update_item(item_id: int, item: UpdateItem):
    if item_id not in inventory:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Item ID doesnot exist")

    if item.name != None:
        inventory[item_id].name = item.name

    if item.price != None:
        inventory[item_id].name = item.price

    if item.brand != None:
        inventory[item_id].name = item.brand

    return inventory[item_id]


# To delete an item with a specific id
@app.delete("/delete-item/{item_id}")
def delete_by_id(item_id: int = Query(..., description="The id of the item you want to delete", gt=0)):
    if item_id not in inventory:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Item ID doesnot exist")
    del inventory[item_id]
