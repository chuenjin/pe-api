API  
  
pip install uv  
cd api  
uv venv  
uv pip install "fastapi[standard]" sqlmodel  
source .venv/bin/activate  
uv run init_db.py  
uv run fastapi dev main.py
