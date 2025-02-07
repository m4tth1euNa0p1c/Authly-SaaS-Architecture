# api/tests/test_db_connection.py

from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from app.config.settings import settings

def test_connection():
    try:
        engine = create_engine(settings.database_url)
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            value = result.scalar()
            if value == 1:
                print("Connexion à la base de données réussie.")
            else:
                print("La requête a échoué. Résultat inattendu :", value)
    except SQLAlchemyError as e:
        print("Erreur lors de la connexion à la base de données :", str(e))

if __name__ == "__main__":
    test_connection()
