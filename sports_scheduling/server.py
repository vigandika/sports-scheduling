from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/schedule")
async def generate_schedule(body: dict):
    print(body)
    # parse_data(body)
    return body
