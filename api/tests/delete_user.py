import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import SessionLocal
from app.models.user import User

def delete_user_by_id(user_id: int) -> None:
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            db.delete(user)
            db.commit()
            print(f"Utilisateur avec l'ID {user_id} supprimé avec succès.")
        else:
            print(f"Aucun utilisateur trouvé avec l'ID {user_id}.")
    except Exception as e:
        db.rollback()
        print(f"Erreur lors de la suppression de l'utilisateur avec l'ID {user_id} : {e}")
    finally:
        db.close()

if __name__ == "__main__":
    delete_user_by_id(3)
