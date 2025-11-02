import React, { useState } from 'react';
import './App.css';
import NewsAggregator from './components/NewsAggregator';

// 🌍 Backend URL — automatically switches between local & Render
const BACKEND =
  process.env.REACT_APP_BACKEND_URL ||
  'https://news-aggregator-backend.onrender.com'; // 🔗 Replace with your actual Render backend URL

function App() {
  const [selectedTopic, setSelectedTopic] = useState('general'); // Default topic
  const [searchQuery, setSearchQuery] = useState(''); // Search query

  // Handle topic selection from the sidebar
  const handleTopicChange = (topic) => {
    setSelectedTopic(topic);
  };

  // Handle search input change
  const handleSearchChange = (e) => {
    setSearchQuery(e.target.value);
  };

  return (
    <div className="App">
      {/* Navbar */}
      <div className="navbar">
        <div className="logo">📰 News Aggregator</div>
        <input
          type="text"
          placeholder="Search news..."
          className="search-box"
          value={searchQuery}
          onChange={handleSearchChange}
        />
      </div>

        {/* Main News Feed */}
        <div className="content">
          {/* 🧠 Pass backend URL to NewsAggregator */}
          <NewsAggregator
            backendUrl={BACKEND}
            selectedTopic={selectedTopic}
            searchQuery={searchQuery}
          />
        </div>
      </div>

      {/* Footer */}
      <footer>
        <div className="footer-content">
          © {new Date().getFullYear()} News Aggregator. All rights reserved.
        </div>
      </footer>
    </div>
  );
}

export default App;
