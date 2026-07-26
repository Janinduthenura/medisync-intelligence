## MediSync Intelligence — Dev Commands

### Setup / environment
```cmd
cd "E:\practise projects\medisync\medisync-intelligence"
venv\Scripts\activate
pip install -r requirements.txt
```

### Run the server
```cmd
uvicorn main:app --reload
```
- `--reload` auto-restarts on file changes — but if changes don't seem to take effect, do a clean restart instead (see Troubleshooting below).
- Wait for `Whisper ready.` and `FLAN-T5 ready.` before testing.

### Health check
```cmd
curl http://localhost:8000/health
```

### Test /transcribe (audio file upload)
```cmd
curl -X POST http://localhost:8000/transcribe -F "file=@test_audio.mp3"
```

### Test /summarize (raw text in, JSON body)
```cmd
curl -X POST http://localhost:8000/summarize -H "Content-Type: application/json" -d "{\"text\": \"PASTE_TRANSCRIPT_HERE\"}"
```

### Test /pipeline (full audio-to-SOAP flow)
```cmd
curl -X POST http://localhost:8000/pipeline -F "file=@test_audio.mp3"
```

### Git — check, stage, commit, push
```cmd
git status
git add .
git commit -m "short description of what changed"
git push
```

First-time push only (if remote not yet set):
```cmd
git remote add origin https://github.com/Janinduthenura/medisync-intelligence.git
git branch -M main
git push -u origin main
```

### Troubleshooting

## Server not picking up code changes: 
```cmd
netstat -ano | findstr :8000
taskkill /PID <pid_from_above> /F
uvicorn main:app
```

## Check Hugging Face model cache (see what's downloaded):
```cmd
dir "C:\Users\LENOVO\.cache\huggingface\hub"
dir "C:\Users\LENOVO\.cache\huggingface\hub\models--google--flan-t5-large\blobs"
```

## NumPy/torch conflict fix (if it resurfaces):
```cmd
pip install "numpy<2"
```

## View git history / diff before reverting:
```cmd
git log --oneline
git diff HEAD -- path\to\file.py
git checkout HEAD -- path\to\file.py
```