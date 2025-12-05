from fastapi import FastAPI
from routers import products, users, basic_auth_users, jwt_auth_users, users_db
from fastapi.staticfiles import StaticFiles


app = FastAPI()

# Routers
app.include_router(products.router)
app.include_router(users.router)

app.include_router(basic_auth_users.router)
app.include_router(jwt_auth_users.router)

app.include_router(users_db.router)


app.mount("/static",StaticFiles(directory="static"), name="static")

'''
Esta es la ruta raíz
'''

# Url local: http://127.0.0.1:8000

@app.get('/')
def root():
    return 'Hola, Acabo de iniciar el servidor FastAPI!'

# Url local: http://127.0.0.1:8000/url


'''
Esta es la ruta /url
'''
@app.get('/url')
def url():
    return {"url":"https://youtu.be/xcO5ePwmswc?si=3HXawVXFowKmwOju"}

# Ejecutar MongoDB con: mongod
# Ejecutar el servidor con: uvicorn main:app --reload
# Detener el servidor con: Ctrl + C

# Docmentacion con Swagger: http://127.0.0.1:8000/docs
# Docmentacion con Redocly: http://127.0.0.1:8000/redoc
