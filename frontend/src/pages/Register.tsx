import React from 'react';
import RegisterForm from '../components/Auth/RegisterForm';

const Register: React.FC = () => {
  const handleRegister = (idToken: string) => {
    console.log("ID Token reçu après inscription :", idToken);
  };

  return (
    <div className="p-4">
      <h2 className="text-2xl font-bold">Inscription</h2>
      <RegisterForm onRegister={handleRegister} />
    </div>
  );
};

export default Register;
