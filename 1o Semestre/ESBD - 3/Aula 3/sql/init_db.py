#!/usr/bin/env python3
"""
Initializes the database
"""


import random

from faker import Faker
from models import Base, Caminhao, Frete, Motorista
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from sqlalchemy_utils import create_database, database_exists

NUM_CAMINHOES = 1000
NUM_MOTORISTAS = 900
NUM_FRETES = 3000
MULTIPLIER = 5


NUM_CAMINHOES = NUM_CAMINHOES * MULTIPLIER
NUM_MOTORISTAS = NUM_MOTORISTAS * MULTIPLIER
NUM_FRETES = NUM_FRETES * MULTIPLIER

# URI Scheme: "postgres+psycopg2://<USERNAME>:<PASSWORD>@<IP_ADDRESS>:<PORT>/<DATABASE_NAME>"
USERNAME = "admin"
PASSWORD = "admin"
IP_ADDRESS = "localhost"
PORT = "5432"
DATABASE_NAME = "db"

POSTGRES_URI = f"postgresql://{USERNAME}:{PASSWORD}@{IP_ADDRESS}:{PORT}/{DATABASE_NAME}"

FAKE = Faker("pt_BR")
# FAKE.seed_instance(42)

ABCs = [char for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"]


def main():
    engine = create_engine(POSTGRES_URI, echo=False)

    if not database_exists(engine.url):
        create_database(engine.url)
    Base.metadata.create_all(bind=engine)

    caminhoes = []
    placas = []
    for i in range(NUM_CAMINHOES):
        placa = "".join(random.sample(ABCs, 3)) + "-" + str(random.randint(0, 9999))
        while placa in placas:
            placa = "".join(random.sample(ABCs, 3)) + "-" + str(random.randint(0, 9999))

        placas.append(placa)

        caminhoes.append(
            Caminhao(
                placa=placa,
                modelo="".join(random.sample(ABCs, 6)),
                eficiencia=3 * random.random(),
                carga_maxima=5000 * random.random(),
            )
        )

    motoristas = []

    def rand_cpf():
        return random.randint(111, 999)

    cpfs = []
    for _ in range(NUM_MOTORISTAS):
        cpf = f"{rand_cpf()}.{rand_cpf()}.{rand_cpf()}-{random.randint(11,99)}"
        while cpf in cpfs:
            cpf = f"{rand_cpf()}.{rand_cpf()}.{rand_cpf()}-{random.randint(11,99)}"

        cpfs.append(cpf)
        motoristas.append(
            Motorista(
                nome=FAKE.name(),
                telefone=FAKE.phone_number(),
                cpf=cpf,
                endereco=FAKE.address(),
                nascimento=FAKE.date_of_birth(),
            )
        )

    fretes = []
    for _ in range(NUM_FRETES):
        fretes.append(
            Frete(
                cpf_motorista=random.choice(motoristas).cpf,
                placa_caminhao=random.choice(caminhoes).placa,
                timestamp=FAKE.date_of_birth(),
                distancia=9000 * random.random(),
                valor=1000 * random.random(),
            )
        )

    with Session(engine) as session:
        session.add_all(caminhoes)
        session.commit()
        session.add_all(motoristas)
        session.commit()
        session.add_all(fretes)
        session.commit()


if __name__ == "__main__":
    main()

# DROP SCHEMA public CASCADE;
# CREATE SCHEMA public;