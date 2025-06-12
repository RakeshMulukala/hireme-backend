# init_db.py

from hiremebackend.database_module import engine
from hiremebackend import models

print("Creating tables...")
models.Base.metadata.drop_all(bind=engine)  # Drops all tables - WARNING: this deletes all data!
models.Base.metadata.create_all(bind=engine)
print("Tables created successfully!")

