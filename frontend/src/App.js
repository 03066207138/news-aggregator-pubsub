import React, { useState } from 'react';
import './App.css';
import NewsAggregator from './components/NewsAggregator';

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
        <div className="logo">News Aggregator</div>
      
      </div>

      {/* Sidebar + Content */}
      {/* <div style={{ display: 'flex', flexDirection: 'row', height: 'calc(100vh - 50px)' }}> */}
        {/* Sidebar */}
        {/* <div className="sidebar">
          <ul>
            <li onClick={() => handleTopicChange('general')}>Home</li>
            <li onClick={() => handleTopicChange('sports')}>Sports</li>
            <li onClick={() => handleTopicChange('technology')}>Technology</li>
            <li onClick={() => handleTopicChange('business')}>Business</li>
            <li onClick={() => handleTopicChange('entertainment')}>Entertainment</li>
            <li onClick={() => handleTopicChange('health')}>Health</li>
          </ul>
        </div> */}

        {/* Main Content */}
        {/* <div className="content"> */}
          <NewsAggregator selectedTopic={selectedTopic} searchQuery={searchQuery} />
        {/* </div> */}
      {/* </div> */}

      {/* Footer */}
      <footer>
        <div className="footer-content">© {new Date().getFullYear()} News Aggregator. All rights reserved.</div>
      </footer>
    </div>
  );
}

export default App;
