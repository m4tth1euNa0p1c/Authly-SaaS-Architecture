import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from sqlalchemy import create_engine, text
from app.config.settings import settings

def get_admin_info():
    engine = create_engine(settings.database_url)
    
    query = text("""
        SELECT 
            u.id AS user_id,
            u.email,
            u.is_active,
            u.created_at,
            u.updated_at,
            r.id AS role_id,
            r.name AS role_name,
            r.description AS role_description
        FROM authly.users u
        JOIN authly.user_roles ur ON u.id = ur.user_id
        JOIN authly.roles r ON ur.role_id = r.id
        WHERE u.email = 'testadmin@example.com'
    """)
    
    with engine.connect() as connection:
        result = connection.execute(query)
        rows = result.fetchall()
        
        if rows:
            print("Informations de l'utilisateur admin :")
            for row in rows:
                print(dict(row._mapping))
        else:
            print("Aucun administrateur trouvé.")

if __name__ == "__main__":
    get_admin_info()
