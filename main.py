from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials, OAuth2PasswordBearer
import secrets

app = FastAPI()

security = HTTPBasic()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

STATIC_TOKEN = "my-static-token"

# Admin-Authentifizierung mit HTTP Basic Auth
def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "admin")
    correct_password = secrets.compare_digest(credentials.password, "secret")
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

# Token-basierte Authentifizierung
def get_current_user(token: str = Depends(oauth2_scheme)):
    if token != STATIC_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
    return token

# Standardmäßig unsichtbare Endpunkte
@app.get("/", include_in_schema=False)
async def root(user: str = Depends(get_current_user)):
    return {"message": f"Hello, authenticated user"}

@app.get("/items/{item_id}", include_in_schema=False)
async def read_item(item_id: int, user: str = Depends(get_current_user)):
    return {"item_id": item_id, "owner": user}

# Funktion, um die geschützten Routen anzuzeigen
def show_protected_routes(app: FastAPI):
    app.openapi_schema = None
    for route in app.routes:
        if hasattr(route, "include_in_schema") and route.path != "/token":
            route.include_in_schema = True

# Funktion, um die geschützten Routen zu verstecken, außer öffentlichen Routen
def hide_protected_routes(app: FastAPI):
    app.openapi_schema = None
    for route in app.routes:
        if hasattr(route, "include_in_schema") and route.path != "/token":
            route.include_in_schema = False

# Token-Endpunkt nach erfolgreicher Admin-Authentifizierung
@app.post("/token", include_in_schema=True)
async def login(username: str = Depends(get_current_username)):
    show_protected_routes(app)
    return {"message": "Login successful. Endpoints are now visible.", "token": STATIC_TOKEN}

# Logout-Endpunkt
@app.post("/logout")
async def logout():
    hide_protected_routes(app)
    return {"message": "Logout successful. Endpoints are now hidden."}
