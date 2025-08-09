
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas
from ..security import get_db, get_current_user

router = APIRouter(prefix="/animals", tags=["animals"])

@router.get("", response_model=list[schemas.Animal])
def list_animals(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return db.query(models.Animal).all()

@router.post("", response_model=schemas.Animal, status_code=201)
def create_animal(animal: schemas.AnimalCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    db_animal = models.Animal(**animal.model_dump())
    db.add(db_animal)
    db.commit()
    db.refresh(db_animal)
    return db_animal

@router.post("/{animal_id}/care", response_model=schemas.CareRecord, status_code=201)
def add_care(animal_id: int, care: schemas.CareRecordCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    animal = db.get(models.Animal, animal_id)
    if not animal:
        raise HTTPException(status_code=404, detail="Animal non trouvé")
    record = models.CareRecord(animal_id=animal_id, **care.model_dump())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record
