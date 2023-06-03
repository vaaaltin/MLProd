import pickle
from datetime import datetime

from models import Base, Caminhao, Frete, Motorista
from redis import Redis
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import Session
from sqlalchemy.sql import text

NUM_CAMINHOES = 1000
NUM_MOTORISTAS = 900
NUM_FRETES = 3000

# URI Scheme: "postgres+psycopg2://<USERNAME>:<PASSWORD>@<IP_ADDRESS>:<PORT>/<DATABASE_NAME>"
USERNAME = "admin"
PASSWORD = "admin"
IP_ADDRESS = "localhost"
PORT = "5432"
DATABASE_NAME = "db"

POSTGRES_URI = f"postgresql://{USERNAME}:{PASSWORD}@{IP_ADDRESS}:{PORT}/{DATABASE_NAME}"


def main():
    engine = create_engine(POSTGRES_URI, echo=False)
    with Session(engine) as session:
        t0 = datetime.now()
        results = session.execute(
            text(
                """
                    SELECT tbl_motoristas.nome, tbl_motoristas.cpf, tbl_caminhoes.placa, tbl_caminhoes.tipo, tbl_fretes.valor
                    FROM tbl_motoristas, tbl_fretes, tbl_caminhoes WHERE
                    tbl_motoristas.cpf = tbl_fretes.cpf_motorista AND
                    tbl_fretes.placa_caminhao = tbl_caminhoes.placa;
                """
            )
        )
        t1 = datetime.now()
        delta = t1 - t0
        print(f"{delta.total_seconds()}s")  # 1.7s

        # i = 0
        # for result in results:
        #     print(result)
        #     i += 1
        #     if i == 100:
        #         break

        up = []
        for result in results:
            up.append(result)
        redis_client = Redis(host="localhost", port=6379, db=0)
        redis_client.setex("fretes_info", 60 * 60 * 24, pickle.dumps(up))

        t0 = datetime.now()
        fretes_info = redis_client.get("fretes_info")
        t1 = datetime.now()
        for frete in pickle.loads(fretes_info)[:100]:
            print(frete)
        delta = t1 - t0
        print(f"{delta.total_seconds()}s")  # 0.52

        redis_client = Redis(host="localhost", port=6379, db=1)
        motoristas = session.query(Motorista).all()
        for motorista in motoristas:
            delta = t0 - motorista.nascimento
            redis_client.setex(
                f"idade-{motorista.cpf}",
                60 * 60 * 24,
                int(delta.total_seconds() / (3.154 * 10**7)),
            )


if __name__ == "__main__":
    main()

# DROP SCHEMA public CASCADE;
# CREATE SCHEMA public;