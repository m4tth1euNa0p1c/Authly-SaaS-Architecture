import React, { useState } from "react";
import LoginForm from "../components/Auth/LoginForm";
import useAuth from "../hooks/useAuth";
import { useNavigate } from "react-router-dom";

const Login: React.FC = () => {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [error, setError] = useState<string | null>(null);

  const handleLogin = async (email: string, password: string) => {
    try {
      await login(email, password);
      navigate("/dashboard");
    } catch (err) {
      console.error("Erreur lors de la connexion :", err);
      setError("Erreur lors de la connexion. Veuillez vérifier vos identifiants.");
    }
  };

  return (
    <div className="p-4">
      <h2 className="text-2xl font-bold">Connexion</h2>
      {error && <p className="text-red-500">{error}</p>}
      <LoginForm onLogin={handleLogin} />
    </div>
  );
};

export default Login;
