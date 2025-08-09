
from fastapi import APIRouter, Depends, Response, HTTPException
from sqlalchemy.orm import Session
from datetime import date
import csv, io
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from .. import models
from ..security import get_db, get_current_user

router = APIRouter(prefix="/exports", tags=["exports"])

@router.get("/care.csv")
def export_care_csv(start: date, end: date, db: Session = Depends(get_db), user=Depends(get_current_user)):
    q = db.query(models.CareRecord).filter(models.CareRecord.date >= start, models.CareRecord.date <= end).all()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["animal_id", "date", "description", "done"])
    for r in q:
        writer.writerow([r.animal_id, r.date.isoformat(), r.description, r.done])
    return Response(content=output.getvalue(), media_type="text/csv")

@router.get("/animal/{animal_id}.pdf")
def export_animal_pdf(animal_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    animal = db.get(models.Animal, animal_id)
    if not animal: raise HTTPException(status_code=404, detail="Animal non trouvé")
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    y = height - 50
    c.setFont("Helvetica-Bold", 14); c.drawString(50, y, f"Fiche Animal — {animal.name}"); y -= 20
    c.setFont("Helvetica", 11)
    lines = [
        f"Espèce: {animal.species}",
        f"Arrivée: {animal.arrival_date}",
        f"Statut: {animal.status}",
        f"Notes: {animal.notes or '-'}",
        "",
        "Historique des soins:"
    ]
    for line in lines:
        c.drawString(50, y, line); y -= 18
    care = animal.care_records
    for r in care:
        row = f"- {r.date} | {'✅' if r.done else '⏺'} {r.description}"
        if y < 60:
            c.showPage(); y = height - 50
        c.drawString(60, y, row); y -= 16
    c.showPage(); c.save()
    pdf = buffer.getvalue(); buffer.close()
    return Response(content=pdf, media_type="application/pdf")
