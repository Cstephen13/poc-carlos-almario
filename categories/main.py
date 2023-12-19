from typing import List

from fastapi import FastAPI, HTTPException, Path, Query, Body

from app.api.serializers import Category

app = FastAPI()

categorias_db = []


@app.post("/categories/", response_model=Category)
async def crear_categoria(categoria: Category):
    categorias_db.append(categoria)
    return categoria


@app.get("/categories/", response_model=List[Category])
async def obtener_categorias(skip: int = Query(0, description="Saltar N registros", ge=0),
                             limit: int = Query(10, description="Limitar a N registros", le=100)):
    return categorias_db[skip: skip + limit]


@app.get("/categories/{categoria_id}", response_model=Category)
async def obtener_categoria(categoria_id: int = Path(..., description="ID de la categoría a obtener")):
    if categoria_id < 0 or categoria_id >= len(categorias_db):
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return categorias_db[categoria_id]


@app.put("/categories/{categoria_id}", response_model=Category)
async def actualizar_categoria(categoria_id: int = Path(..., description="ID de la categoría a actualizar"),
                               categoria: Category = Body(...)):
    if categoria_id < 0 or categoria_id >= len(categorias_db):
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    categorias_db[categoria_id] = categoria
    return categoria


@app.delete("/categories/{categoria_id}", response_model=Category)
async def eliminar_categoria(categoria_id: int = Path(..., description="ID de la categoría a eliminar")):
    if categoria_id < 0 or categoria_id >= len(categorias_db):
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    categoria_eliminada = categorias_db.pop(categoria_id)
    return categoria_eliminada
