import random
import fastapi

app = fastapi.FastAPI()

@app.get("/generate_name")
async def generate_name():
    names = ["Abdul", "Mohideen", "Kader", "Noor", "Iqbal"] 
    random_name = random.choice(names)
    return {"name":random_name}

#Passing parameters in FastAPI
@app.get("/generate_name_qs", responses={404:{}})
async def generate_name_qs(max_length: int = None, starts_with: str = None):
    names = ["Abdul", "Mohideen", "Kader", "Noor", "Iqbal"] 
    if max_length:
        names = [name for name in names if len(name) <= max_length]
    if starts_with:
        names = [name for name in names if name.lower().startswith(starts_with.lower())]
    #Raise errors in FastAPI
    if len(names) ==0 :
        raise fastapi.HTTPException(404, detail="No names available")
    random_name = random.choice(names)
    return {"name":random_name}