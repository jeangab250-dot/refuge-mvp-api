
# Refuge MVP+ — Backend FastAPI (auth + tâches + stocks + exports + notifications)

## Démarrage rapide
1) Python 3.10+ installé
2) Terminal dans ce dossier
3) Créer l'environnement + installer
   - macOS/Linux
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     pip install -r requirements.txt
     ```
   - Windows (PowerShell)
     ```powershell
     python -m venv .venv
     .\.venv\Scripts\Activate.ps1
     pip install -r requirements.txt
     ```
4) (Optionnel) copier `.env.example` → `.env` et ajuster
5) Lancer
   ```bash
   python -m uvicorn app.main:app --reload
   ```
6) Ouvrir http://127.0.0.1:8000/docs

## Comptes
- Créez d'abord un utilisateur: `POST /auth/signup`
- Connectez-vous: `POST /auth/login` → récupérez `access_token`
- Utilisez le bouton "Authorize" dans /docs pour tester les routes protégées.
