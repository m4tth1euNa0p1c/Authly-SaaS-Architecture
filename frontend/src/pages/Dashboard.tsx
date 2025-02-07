import React, { useEffect, useState } from "react";
import { firebaseAuth } from "../services/firebaseService";
import { onAuthStateChanged, reload } from "firebase/auth";
import { useNavigate } from "react-router-dom";

interface UserInfo {
  email: string;
  displayName?: string | null;
}

const Dashboard: React.FC = () => {
  const [userInfo, setUserInfo] = useState<UserInfo | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const navigate = useNavigate();

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(firebaseAuth, async (user) => {
      if (user) {
        try {
          await reload(user);
          setUserInfo({
            email: user.email!,
            displayName: user.displayName,
          });
        } catch (error) {
          console.error("Erreur lors du rechargement des données utilisateur :", error);
          navigate("/login");
        }
      } else {
        navigate("/login");
      }
      setLoading(false);
    });

    return () => unsubscribe();
  }, [navigate]);

  if (loading) {
    return <div className="p-4 text-center">Chargement...</div>;
  }

  return (
    <div className="p-4">
      <h2 className="text-2xl font-bold mb-4">Dashboard</h2>
      {userInfo ? (
        <div>
          <p className="text-lg">Bienvenue sur le Dashboard </p>
        </div>
      ) : (
        <p>Aucun utilisateur connecté</p>
      )}
    </div>
  );
};

export default Dashboard;
