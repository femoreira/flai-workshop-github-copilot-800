import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import './App.css';
import Activities from './components/Activities';
import Leaderboard from './components/Leaderboard';
import Teams from './components/Teams';
import Users from './components/Users';
import Workouts from './components/Workouts';

function App() {
  const [darkMode, setDarkMode] = useState(() => {
    const saved = localStorage.getItem('darkMode');
    return saved === 'true';
  });

  useEffect(() => {
    localStorage.setItem('darkMode', darkMode);
    if (darkMode) {
      document.body.classList.add('dark-mode');
    } else {
      document.body.classList.remove('dark-mode');
    }
  }, [darkMode]);

  const toggleDarkMode = () => {
    setDarkMode(!darkMode);
  };

  return (
    <Router>
      <div className={`App ${darkMode ? 'dark-mode' : ''}`}>
        <nav className="navbar navbar-expand-lg navbar-dark" style={{background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'}}>
          <div className="container-fluid">
            <Link className="navbar-brand" to="/">
              <img src="/logo.png" alt="OctoFit Logo" className="navbar-logo" />
              OctoFit Tracker
            </Link>
            <button 
              className="navbar-toggler" 
              type="button" 
              data-bs-toggle="collapse" 
              data-bs-target="#navbarNav" 
              aria-controls="navbarNav" 
              aria-expanded="false" 
              aria-label="Toggle navigation"
            >
              <span className="navbar-toggler-icon"></span>
            </button>
            <div className="collapse navbar-collapse" id="navbarNav">
              <ul className="navbar-nav ms-auto">
                <li className="nav-item">
                  <Link className="nav-link" to="/activities">📊 Activities</Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/leaderboard">🏆 Leaderboard</Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/teams">👥 Teams</Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/users">👤 Users</Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/workouts">💪 Workouts</Link>
                </li>
                <li className="nav-item">
                  <button 
                    className="btn btn-link nav-link dark-mode-toggle" 
                    onClick={toggleDarkMode}
                    aria-label="Toggle dark mode"
                    title={darkMode ? "Switch to Light Mode" : "Switch to Dark Mode"}
                  >
                    {darkMode ? '☀️' : '🌙'}
                  </button>
                </li>
              </ul>
            </div>
          </div>
        </nav>

        <Routes>
          <Route path="/" element={
            <div className="container mt-4">
              <div className="hero-section text-center">
                <h1>Welcome to OctoFit Tracker</h1>
                <p className="lead">Track your fitness activities, compete with your team, and achieve your goals!</p>
                <hr className="my-4" style={{borderColor: 'rgba(255,255,255,0.3)'}} />
                <p className="mb-4">Use the navigation menu above to explore activities, view the leaderboard, manage teams, and more.</p>
                <div className="d-flex gap-3 justify-content-center flex-wrap">
                  <Link to="/activities" className="btn btn-light btn-lg">Get Started</Link>
                  <Link to="/leaderboard" className="btn btn-outline-light btn-lg">View Rankings</Link>
                </div>
              </div>
              
              <div className="row mt-5 mb-4">
                <div className="col-md-4 mb-3">
                  <Link to="/users" style={{textDecoration: 'none'}}>
                    <div className="card h-100 shadow-sm" style={{cursor: 'pointer', transition: 'transform 0.2s'}}>
                      <div className="card-body text-center">
                        <div style={{fontSize: '3rem', marginBottom: '1rem'}}>👥</div>
                        <h5 className="card-title" style={{color: '#667eea'}}>Users</h5>
                        <p className="card-text">View all fitness enthusiasts and their profiles</p>
                      </div>
                    </div>
                  </Link>
                </div>
                
                <div className="col-md-4 mb-3">
                  <Link to="/activities" style={{textDecoration: 'none'}}>
                    <div className="card h-100 shadow-sm" style={{cursor: 'pointer', transition: 'transform 0.2s'}}>
                      <div className="card-body text-center">
                        <div style={{fontSize: '3rem', marginBottom: '1rem'}}>🏃</div>
                        <h5 className="card-title" style={{color: '#667eea'}}>Activities</h5>
                        <p className="card-text">Track and log your fitness activities</p>
                      </div>
                    </div>
                  </Link>
                </div>
                
                <div className="col-md-4 mb-3">
                  <Link to="/leaderboard" style={{textDecoration: 'none'}}>
                    <div className="card h-100 shadow-sm" style={{cursor: 'pointer', transition: 'transform 0.2s'}}>
                      <div className="card-body text-center">
                        <div style={{fontSize: '3rem', marginBottom: '1rem'}}>🏆</div>
                        <h5 className="card-title" style={{color: '#667eea'}}>Leaderboard</h5>
                        <p className="card-text">See the top performers and rankings</p>
                      </div>
                    </div>
                  </Link>
                </div>
              </div>
            </div>
          } />
          <Route path="/activities" element={<Activities />} />
          <Route path="/leaderboard" element={<Leaderboard />} />
          <Route path="/teams" element={<Teams />} />
          <Route path="/users" element={<Users />} />
          <Route path="/workouts" element={<Workouts />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
