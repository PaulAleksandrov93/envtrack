
import React from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import './App.css';
import AuthContext, { AuthProvider } from './context/AuthContext'
import Header from './components/Header';
import LoginPage from './pages/LoginPage';
import ParametersListPage from './pages/ParametersListPage';
import ParametersPage from './pages/ParametersPage';
import { useContext } from 'react';

function App() {
  return (
    <Router>
      <div className="container root">
        <div className="app">
          <AuthProvider>
            <Header />
            <Routes>
              <Route
                path="/"
                element={<ProtectedRoute />}
              />
              <Route path="/login" element={<LoginPage />} />
              <Route path="/parameter/:id" element={<ParametersPage />} />
            </Routes>
          </AuthProvider>
        </div>
      </div>
    </Router>
  );
}

function ProtectedRoute() {
  let { user } = useContext(AuthContext);
  return user ? <ParametersListPage /> : <Navigate to="/login" />;
}

export default App;






