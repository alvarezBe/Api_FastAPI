from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


router = APIRouter(
    prefix="/basicauth",
    tags=["basicauth"],
    responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}}
)

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool

class UserDB(User):
    password: str


users_db = {
    "adrian":{
        "username": "adrian",
        "full_name": "Adrian Alvarez",
        "email": "adrian@example.com",
        "disabled": False,
        "password": "secret"
    },

    "anibal":{
        "username": "anibal",
        "full_name": "Anibal Moran",
        "email": "anibal@example.com",
        "disabled": True,
        "password": "nosecret"
    }
}


def search_user_db(username: str): # Busqueda de usuario en la base de datos
    if username in users_db:
        return UserDB(**users_db[username])
    

def search_user(username: str): 
    if username in users_db:
        return User(**users_db[username])
    
    
async def current_user(token: str = Depends(oauth2)): # Obtener el usuario actual
    user = search_user(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Credenciales de autenticacion invalidas",
              headers={"WWW-Authenticate": "Bearer"})
    
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Usuario innactivo")
    return user

    
@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not users_db:
         raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="El Usuario ya no es correcto")
    
    user = search_user_db(form.username) # Comparar contraseñas
    if not form.password == user.password:
         raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="La contraseña no es correcta")
    
    return {"access_token": user.username, "token_type": "bearer"}


@router.get("/users/me") # Operacion para obtener el usuario actual
async def me(user: User = Depends(current_user)):
    return user