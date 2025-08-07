from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, String, Numeric, Integer
from sqlalchemy.orm import declarative_base, sessionmaker

db_url = "postgresql://fareed:rYssJteYMh7UgxdeUk3Wmy0vq3wyXJmC@dpg-d29r4lqdbo4c739mbrb0-a.oregon-postgres.render.com:5432/fastapi_db_7i56"

engine = create_engine(db_url, connect_args={"sslmode": "require"})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

app = FastAPI()


class CryptoVali(BaseModel):
    id: int
    name: str
    price: float
    total_valuation: float
    total_coins: int


class CryptoInfo2(Base):
    __tablename__ = "crypto_info2"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Numeric)
    total_valuation = Column(Numeric)
    total_coins = Column(Integer)


Base.metadata.create_all(bind=engine)

@app.post("/data")
def put_data(data: CryptoVali):
    db = SessionLocal()
    try:
        new_data = CryptoInfo2(
            id=data.id,
            name=data.name,
            price=data.price,
            total_valuation=data.total_valuation,
            total_coins=data.total_coins
        )
        db.add(new_data)
        db.commit()
        return {"message": "Data inserted successfully"}
    except Exception as e:
        db.rollback()
        return {"error": str(e)}
    finally:
        db.close()

@app.get("/data")
def get_data():
    db = SessionLocal()
    try:
        result = db.query(CryptoInfo2).all()
        data = []
        for row in result:
            data.append({
                "id": row.id,
                "name": row.name,
                "price": float(row.price),
                "total_valuation": float(row.total_valuation),
                "total_coins": row.total_coins
            })
        return data
    finally:
        db.close()
