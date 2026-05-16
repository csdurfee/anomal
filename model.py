from typing import Annotated
from fastapi import Depends, FastAPI, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select

import uuid


# class Hero(SQLModel, table=True):
#     id: int | None = Field(default=None, primary_key=True)
#     name: str = Field(index=True)
#     age: int | None = Field(default=None, index=True)
#     secret_name: str
#     quick_test: str

class Dataset(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    public_id: uuid.UUID = Field(default_factory=uuid.uuid4)
    description: str


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(
        prog="Anomal DB tool",
    )
    parser.add_argument("--rebuild", help="rebuild the DB", action="store_true")
    args = parser.parse_args()

    if args.rebuild:
        print("rebuilding database, hope you meant to do that LOL")
        SQLModel.metadata.create_all(engine)
