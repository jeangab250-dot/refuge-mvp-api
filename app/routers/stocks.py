
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas
from ..security import get_db, get_current_user

router = APIRouter(prefix="/stocks", tags=["stocks"])

@router.get("", response_model=list[schemas.StockItem])
def list_items(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return db.query(models.StockItem).order_by(models.StockItem.name.asc()).all()

@router.post("", response_model=schemas.StockItem, status_code=201)
def create_item(item: schemas.StockItemCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    exists = db.query(models.StockItem).filter(models.StockItem.name == item.name).first()
    if exists:
        raise HTTPException(status_code=400, detail="Existe déjà")
    db_item = models.StockItem(**item.model_dump())
    db.add(db_item); db.commit(); db.refresh(db_item)
    return db_item

@router.patch("/{item_id}", response_model=schemas.StockItem)
def update_item(item_id: int, patch: schemas.StockItemUpdate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    it = db.get(models.StockItem, item_id)
    if not it: raise HTTPException(status_code=404, detail="Introuvable")
    data = patch.model_dump(exclude_unset=True)
    for k, v in data.items():
        setattr(it, k, v)
    db.commit(); db.refresh(it)
    return it
