from typing import List

from fastapi import FastAPI, HTTPException, Path, Query, Body

from app.api.serializers import Product

app = FastAPI()

productos_db = []


@app.post("/products/", response_model=Product)
async def crear_producto(producto: Product):
    productos_db.append(producto)
    return producto


@app.get("/products/", response_model=List[Product])
async def obtener_productos(skip: int = Query(0, description="Skip N records", ge=0),
                            limit: int = Query(10, description="Limit to N records", le=100)):
    return productos_db[skip: skip + limit]


@app.get("/products/{producto_id}", response_model=Product)
async def obtener_producto(producto_id: int = Path(..., description="ID del producto a obtener")):
    if producto_id < 0 or producto_id >= len(productos_db):
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return productos_db[producto_id]


@app.put("/products/{producto_id}", response_model=Product)
async def actualizar_producto(producto_id: int = Path(..., description="ID del producto a actualizar"),
                              producto: Product = Body(...)):
    if producto_id < 0 or producto_id >= len(productos_db):
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    productos_db[producto_id] = producto
    return producto


@app.delete("/products/{producto_id}", response_model=Product)
async def eliminar_producto(producto_id: int = Path(..., description="ID del producto a eliminar")):
    if producto_id < 0 or producto_id >= len(productos_db):
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    producto_eliminado = productos_db.pop(producto_id)
    return producto_eliminado
