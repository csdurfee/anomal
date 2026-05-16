from typing import Annotated
from fastapi import Depends, FastAPI, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select
from sqlalchemy import Column, TEXT, UUID

from ulid import ULID

class DatasetBase(SQLModel):
    description: str

class Dataset(DatasetBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    public_id: ULID = Field(default_factory=ULID, sa_column=Column(UUID))
    
    data : str = Field(default=None, sa_column=Column(TEXT))


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
        print("creating database and tables (as necessary)")
        SQLModel.metadata.create_all(engine)
