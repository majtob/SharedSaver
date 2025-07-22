import React from 'react';
import { useNavigate } from 'react-router-dom';

const Navbar: React.FC = () => {
  const navigate = useNavigate();

  return (
    <nav className="bg-white shadow-lg">
      <div className="max-w-7xl mx-auto px-4">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <span className="text-xl font-bold">SharedSaver</span>
          </div>
          
          <div className="flex items-center space-x-4">
            <button onClick={() => navigate('/')}>Dashboard</button>
            <button onClick={() => navigate('/accounts')}>Accounts</button>
            <button onClick={() => navigate('/transactions')}>Transactions</button>
            <button onClick={() => navigate('/loans')}>Loans</button>
            <button onClick={() => navigate('/login')}>Login</button>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar; 