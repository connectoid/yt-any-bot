from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from .models import Base, User, Sample
from config_data.config import load_config, Config

POOL_SIZE = 20
MAX_OVERFLOW = 0

config: Config = load_config()

db_user = config.db.db_user
db_password = config.db.db_password

database_url = f'postgresql://{db_user}:{db_password}@{config.db.db_host}:5432/{config.db.database}'

engine = create_engine(database_url, echo=False, pool_size=POOL_SIZE, max_overflow=MAX_OVERFLOW)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)



def add_sample(name):
    session = Session()
    new_sample = Sample(
            name=name,
        )
    session.add(new_sample)
    session.commit()



def add_user(tg_id, fname, lname):
    session = Session()
    user = session.query(User).filter(User.tg_id == tg_id).first()
    if user is None:
        new_user = User(tg_id=tg_id, fname=fname, lname=lname)
        session.add(new_user)
        session.commit()
        return True
    return False 


def get_user_id(tg_id):
    session = Session()
    user = session.query(User).filter(User.tg_id == tg_id).first()
    return user.id


