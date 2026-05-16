from typing import Annotated
from fastapi import FastAPI, HTTPException, Query
from sqlmodel import select

from model import SessionDep, Dataset, DatasetBase

app = FastAPI()

@app.get("/dataset/")
def read_datasets(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Dataset]:
    datasets = session.exec(select(Dataset).offset(offset).limit(limit)).all()
    return datasets

@app.post("/dataset/", response_model=Dataset)
def create_dataset(dataset: DatasetBase, session: SessionDep) -> Dataset:
    db_dataset = Dataset.model_validate(dataset)
    session.add(db_dataset)
    session.commit()
    session.refresh(db_dataset)
    return db_dataset 