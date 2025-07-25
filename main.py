# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.staticfiles import StaticFiles  # ✅ For serving images
# import os

# # ✅ Import all routers
# from api.admin.admin import admin_router
# from api.admin.auth import auth_router
# from api.admin.country import country_router
# from api.admin.state import state_router
# from api.admin.city import city_router
# from api.admin.building import building_router
# from api.admin.manager import manager_router
# from api.admin.manager_login import manager_login_router
# from api.admin.stalls import stall_router
# from api.admin.category import category_router
# from api.admin.items import item_router
# from api.user.user import user_router
# from api.user.auth import login_router
# from api.user.cart import cart_router
# from api.user.wallet import wallet_router
# from api.user.order import order_router


# app = FastAPI(
#     title="FlipLine Admin Backend",
#     version="1.0.0",
#     docs_url="/docs",
#     openapi_url="/openapi.json"
# )

# # ✅ Enable CORS for frontend access
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=[
#         "http://localhost:3000",
#         "http://localhost:3001",  # ✅ Add this
#         "http://127.0.0.1:3001"   # ✅ Optional but recommended
#     ],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


# # ✅ Mount uploaded_images directory to serve media files
# UPLOAD_DIR = "uploaded_images"
# if not os.path.exists(UPLOAD_DIR):
#     os.makedirs(UPLOAD_DIR)
# app.mount("/uploaded_images", StaticFiles(directory=UPLOAD_DIR), name="uploaded_images")

# # ✅ Include all routers
# app.include_router(admin_router)
# app.include_router(auth_router)
# app.include_router(country_router)
# app.include_router(state_router)
# app.include_router(city_router)
# app.include_router(building_router)
# app.include_router(manager_router)
# app.include_router(stall_router)
# app.include_router(category_router)
# app.include_router(item_router)
# app.include_router(user_router) 
# app.include_router(login_router)    
# app.include_router(manager_login_router)
# app.include_router(cart_router)
# app.include_router(wallet_router)
# app.include_router(order_router)










from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

# ✅ Import all routers
from api.admin.admin import admin_router
from api.admin.auth import auth_router
from api.admin.country import country_router
from api.admin.state import state_router
from api.admin.city import city_router
from api.admin.building import building_router
from api.admin.manager import manager_router
from api.admin.manager_login import manager_login_router
from api.admin.stalls import stall_router
from api.admin.category import category_router
from api.admin.items import item_router
from api.user.user import user_router
from api.user.auth import login_router
from api.user.cart import cart_router
from api.user.wallet import wallet_router
from api.user.order import order_router

app = FastAPI(
    title="FlipLine Admin Backend",
    version="1.0.0",
    docs_url="/docs",
    openapi_url="/openapi.json"
)

# ✅ Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3001",
        "https://fliplyn-user.onrender.com",
        "https://fliplyn-customer.onrender.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ✅ Serve uploaded images
UPLOAD_DIR = "uploaded_images"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

app.mount("/uploaded_images", StaticFiles(directory=UPLOAD_DIR), name="uploaded_images")

# ✅ Include all routers
app.include_router(admin_router)
app.include_router(auth_router)
app.include_router(country_router)
app.include_router(state_router)
app.include_router(city_router)
app.include_router(building_router)
app.include_router(manager_router)
app.include_router(manager_login_router)
app.include_router(stall_router)
app.include_router(category_router)
app.include_router(item_router)
app.include_router(user_router)
app.include_router(login_router)
app.include_router(cart_router)
app.include_router(wallet_router)
app.include_router(order_router)

# ✅ For local development only
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))  # Render will set PORT automatically
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
