
@echo off
if exist ".venv\Scripts\activate.bat" call ".venv\Scripts\activate.bat"
python -m uvicorn app.main:app --reload
