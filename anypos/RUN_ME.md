# 🚀 How to Run AnyPos POS System - Simple Guide

## The Easiest Way (No Technical Knowledge Needed!)

### Option 1: Click START.bat (Recommended for Windows Users)

1. Open the folder: `C:\Users\Thisara\Documents\pos\anypos`
2. **Double-click the `START.bat` file**
3. Wait 30 seconds for everything to load
4. Your browser will automatically open (or manually go to http://localhost:5173)
5. **Login with:**
   - **Username:** `admin`
   - **Password:** `admin123`

That's it! ✅

---

### Option 2: Run Using PowerShell (If you prefer)

1. Open PowerShell
2. Copy and paste this command:
```powershell
cd 'C:\Users\Thisara\Documents\pos\anypos'; & '.\START.ps1'
```
3. Press Enter
4. Wait 30 seconds for everything to start
5. Go to http://localhost:5173 in your browser
6. Login with admin / admin123

---

### Option 3: Single One-Line Command (For Advanced Users)

```powershell
cd 'C:\Users\Thisara\Documents\pos\anypos'; python -m venv venv; .\venv\Scripts\Activate.ps1; pip install -q -r requirements.txt; copy .env.example .env; cd backend; python ..\scripts\init_data.py; start powershell -ArgumentList '-NoExit', '-Command', "cd '$pwd'; python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000"; cd ..; start powershell -ArgumentList '-NoExit', '-Command', "cd frontend; npm install; npm run dev"
```

---

## What Happens When You Run START.bat?

The script automatically:
1. ✅ Creates a Python virtual environment
2. ✅ Installs all required Python packages
3. ✅ Installs all required JavaScript packages
4. ✅ Sets up the database
5. ✅ Starts the backend server (http://localhost:8000)
6. ✅ Starts the frontend server (http://localhost:5173)

---

## Login Credentials

Use these to log in:

| Role | Username | Password |
|------|----------|----------|
| Admin (Full Access) | admin | admin123 |
| Manager | manager | manager123 |
| Cashier | cashier | cashier123 |

---

## Access the Application

- **Main App:** http://localhost:5173
- **API Documentation:** http://localhost:8000/docs
- **API Health Check:** http://localhost:8000/health

---

## Stop the Application

- Close both PowerShell windows (Backend and Frontend)
- Or press `Ctrl+C` in each window

---

## Troubleshooting

### "Python is not installed"
- Download from: https://www.python.org
- Make sure to check ✓ "Add Python to PATH" during installation

### "Node.js is not installed"
- Download from: https://nodejs.org
- Install the LTS version

### Port Already in Use (8000 or 5173)
- Close any other applications using those ports
- Or modify the port in the script

### Still Having Issues?
- Delete the `venv` folder and try again
- Make sure Python and Node.js are installed and in your PATH
- Run the command in PowerShell as Administrator

---

## What Each File Does

- **START.bat** - Windows batch file (easiest option, just double-click)
- **START.ps1** - PowerShell script (alternative startup method)
- **requirements.txt** - Python packages list
- **.env** - Configuration file (created automatically)
- **anypos.db** - Database file (created automatically)

---

**That's all you need to know!** 🎉

Just run START.bat and the app will be ready in 30 seconds.
