// src/App.js
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import RecommendationPage from './components/RecommendationPage';
import AnalyticsPage from './components/AnalyticsPage';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <nav className="navbar">
          <div className="nav-container">
            <h1 className="nav-logo">🛋️ Furniture AI</h1>
            <div className="nav-links">
              <Link to="/" className="nav-link">Recommendations</Link>
              <Link to="/analytics" className="nav-link">Analytics</Link>
            </div>
          </div>
        </nav>

        <main className="main-content">
          <Routes>
            <Route path="/" element={<RecommendationPage />} />
            <Route path="/analytics" element={<AnalyticsPage />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;