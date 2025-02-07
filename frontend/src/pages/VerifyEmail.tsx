import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { firebaseAuth } from "../services/firebaseService";
import { onAuthStateChanged, reload } from "firebase/auth";

const VerifyEmail: React.FC = () => {
  const navigate = useNavigate();
  const [message, setMessage] = useState<string>("Vérification de votre adresse e-mail en cours...");

  useEffect(() => {
    const checkVerification = async (): Promise<void> => {
      try {
        const user = firebaseAuth.currentUser;
        if (!user) {
          setMessage("Aucun utilisateur connecté. Veuillez vous connecter ou vous inscrire.");
          return;
        }
        await reload(user);

        if (user.emailVerified) {
          const registrationDataString = localStorage.getItem("registrationData");
          if (!registrationDataString) {
            setMessage("Données d'inscription manquantes. Veuillez vous inscrire à nouveau.");
            return;
          }
          const localData = JSON.parse(registrationDataString);

          const payload = {
            email: user.email.trim().toLowerCase(),
            password: localData.password.trim(),
            first_name: (localData.first_name || "").trim(),
            last_name: (localData.last_name || "").trim()
          };

          console.log("Payload sent to finalize:", payload);

          const idToken = await user.getIdToken();

          const response = await axios.post(
            `${import.meta.env.VITE_API_BASE_URL}/auth/finalize`,
            payload,
            {
              headers: {
                Authorization: `Bearer ${idToken}`
              }
            }
          );

          console.log("Finalize response:", response.data);

          localStorage.removeItem("registrationData");

          setMessage("Votre adresse e-mail est vérifiée et votre compte est créé. Redirection...");
          setTimeout(() => {
            navigate("/dashboard");
          }, 2000);
        } else {
          setMessage("Votre adresse e-mail n'est pas encore vérifiée. Vérifiez votre boîte de réception.");
        }
      } catch (error: any) {
        console.error("Erreur lors de la vérification de l'e-mail:", error.response?.data || error.message);
        const errorDetail = error.response?.data?.detail
          ? JSON.stringify(error.response.data.detail)
          : error.message;
        setMessage(`Erreur lors de la vérification: ${errorDetail}`);
      }
    };

    const unsubscribe = onAuthStateChanged(firebaseAuth, (user) => {
      if (user) {
        checkVerification();
      } else {
        setMessage("Aucun utilisateur connecté.");
      }
    });

    return () => unsubscribe();
  }, [navigate]);

  return (
    <div className="p-4 max-w-md mx-auto text-center">
      <p className="text-xl font-bold">{message}</p>
    </div>
  );
};

export default VerifyEmail;
