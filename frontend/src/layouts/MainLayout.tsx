import React from "react";
import { Outlet } from "react-router-dom";
import Header from "../components/Common/Header";

const MainLayout: React.FC = () => {
  return (
    <div className="min-h-screen flex flex-col">
      <Header />
      <main className="flex-grow container mx-auto p-4">
        <Outlet />
      </main>
      <footer className="bg-gray-800 text-white p-4 text-center">
        &copy; {new Date().getFullYear()} Authly SaaS. Tous droits réservés.
      </footer>
    </div>
  );
};

export default MainLayout;
