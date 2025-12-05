from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()


# Ejecutar el servidor con: uvicorn users:app --reload

# Entidad users

class User(BaseModel):
    id: int
    name: str
    surname: str
    url: str
    age: int

users_list = [User(id=1, name="adrian", surname="Alvarez", url="https://youtu.be/5x-a_pTnb5w?si=5eJcB-QrrryKqk56", age=17),
               User(id=2,name="Anai", surname="Urizar", url="https://youtu.be/5x-a_pTnb5w?si=5eJcB-QrrryKqk56", age=17),
               User(id=3,name="Anibal", surname="Moran", url="https://youtu.be/5x-a_pTnb5w?si=5eJcB-QrrryKqk56", age=18)]


@router.get('/usersjson')
def usersjson():
    return [
        {"name": "adrian", "surname": "Alvarez", "url": "https://youtu.be/5x-a_pTnb5w?si=5eJcB-QrrryKqk56", "age": 17},
        {"name": "Anai", "surname": "Urizar", "url": "https://youtu.be/5x-a_pTnb5w?si=5eJcB-QrrryKqk56", "age": 17},
        {"name": "Anibal", "surname": "Moran", "url": "https://youtu.be/5x-a_pTnb5w?si=5eJcB-QrrryKqk56", "age": 18}
    ]

@router.get("/users")
async def users():
    return users_list

# Path
@router.get("/users/{id}")
async def user(id: int):
    return search_user(id)

#Query
@router.get("/user/")
async def user(id: int):
    return search_user(id)
    
@router.post("/user/", response_model=User, status_code=201) # Crear
async def user(user: User):
    if type(search_user(user.id)) == User:
            raise HTTPException(status_code= 404, detail="El Usuario ya existe") #Para manejo de errores de HTTP
   
    users_list.append(user)
    return user

@router.put("/user/")  # Actualizar
async def user(user: User):

    found = False

    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            found = True

    if not found:
        return {"error": "El Usuario no actualizado"}
    else:
        return user
    
@router.delete("/user/{id}")  # Eliminar
async def user(id: int):

    found = False

    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            users_list[index] = user
            del users_list[index]
            found = True

    if not found:
            return {"error": "El Usuario no eliminado"} 
            

def search_user(id: int):
    user = filter(lambda user: user.id == id, users_list)
    try:
        return list(user)[0]
    except IndexError:
        return {"error": "Usuario no encontrado"}
