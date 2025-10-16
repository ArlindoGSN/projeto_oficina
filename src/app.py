from fastapi import FastAPI, status

from .schemas import Message

app = FastAPI()


@app.get("/", response_model=Message, status_code=status.HTTP_200_OK)
def read_root():
    return Message(message="Hello, World!")


@app.get("/health", response_model=Message, status_code=status.HTTP_200_OK)
def read_health():
    return Message(message="OK")


@app.post("/items/", response_model=Message, status_code=status.HTTP_201_CREATED)
def create_item(item: Message):
    return item
