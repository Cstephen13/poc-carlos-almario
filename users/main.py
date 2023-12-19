from typing import List

from fastapi import FastAPI, HTTPException, Path, Query, Body

from app.api.serializers import User

app = FastAPI()

users_db = []


@app.post("/users/", response_model=User)
async def create_user(user: User):
    users_db.append(user)
    return user


@app.get("/users/", response_model=List[User])
async def get_users(skip: int = Query(0, description="Saltar N registros", ge=0),
                    limit: int = Query(10, description="Limitar a N registros", le=100)):
    return users_db[skip: skip + limit]


@app.get("/users/{user_id}", response_model=User)
async def get_user(user_id: int = Path(..., description="ID de la categoría a obtener")):
    if user_id < 0 or user_id >= len(users_db):
        raise HTTPException(status_code=404, detail="User not found")
    return users_db[user_id]


@app.put("/users/{user_id}", response_model=User)
async def update_user(user_id: int = Path(..., description="ID of the user to update"), user: User = Body(...)):
    if user_id < 0 or user_id >= len(users_db):
        raise HTTPException(status_code=404, detail="User not found")
    users_db[user_id] = user
    return user


@app.delete("/users/{user_id}", response_model=User)
async def delete_user(user_id: int = Path(..., description="ID of the user to delete")):
    if user_id < 0 or user_id >= len(users_db):
        raise HTTPException(status_code=404, detail="User not found")
    user_deleted = users_db.pop(user_id)
    return user_deleted
