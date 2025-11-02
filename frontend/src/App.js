import React, { useState, useEffect } from "react";
import axios from "axios";
import "./App.css";

// 🌍 Backend URL — auto switch between local & Render
const BACKEND =
  process.env.REACT_APP_BACKEND_URL ||
  "https://news-aggregator-backend.onrender.com";

function App() {
  const [topic, setTopic] = useState("general");
  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");
  const [source, setSource] = useState("frontend");
  const [newsList, setNewsList] = useState([]);
  const [searchQuery, setSearchQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // 📰 Fetch news from backend
  const fetchNews = async () => {
    setLoading(true);
    setError("");
    try {
      const { data } = await axios.get(
        `${BACKEND}/subscribe?topic=${topic}&limit=10`
      );
      setNewsList(data.messages || []);
    } catch (err) {
      console.error("Error fetching news:", err);
      setError("Failed to load news. Please check backend connection.");
    } finally {
      setLoading(false);
    }
  };

  // 🕒 Auto-fetch whenever topic changes
  useEffect(() => {
    fetchNews();
  }, [topic]);

  // 🗞️ Publish new article
  const publishNews = async () => {
    if (!title || !content) {
      alert("Please enter both title and content.");
      return;
    }
    try {
      await axios.post(`${BACKEND}/publish`, {
        topic,
        title,
        content,
        source,
      });
      alert("✅ News published successfully!");
      setTitle("");
      setContent("");
      fetchNews();
    } catch (err) {
      console.error("Error publishing news:", err);
      alert("❌ Failed to publish. Check backend or RabbitMQ connection.");
    }
  };

  // 🔍 Filter news by search query
  const filteredNews = newsList.filter(
    (n) =>
      n.title?.toLowerCase().includes(searchQuery.toLowerCase()) ||
      n.content?.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="App">
      {/* 🧭 Navbar */}
      <div className="navbar">
        <div className="logo">📰 News Aggregator</div>
        <input
          type="text"
          className="search-box"
          placeholder="Search news..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
        />
      </div>

      {/* 📚 Sidebar + Main */}
      <div className="main-layout">
        <div className="sidebar">
          <h3>Topics</h3>
          {["general", "sports", "technology", "business", "health", "science", "entertainment"].map(
            (t) => (
              <div
                key={t}
                className={`topic ${topic === t ? "active" : ""}`}
                onClick={() => setTopic(t)}
              >
                {t.charAt(0).toUpperCase() + t.slice(1)}
              </div>
            )
          )}
        </div>

        <div className="content">
          {/* 🗞️ Publisher Form */}
          <div className="publisher-form">
            <h2>Publish News</h2>
            <input
              type="text"
              placeholder="Title"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
            />
            <textarea
              placeholder="Content"
              value={content}
              onChange={(e) => setContent(e.target.value)}
            />
            <input
              type="text"
              placeholder="Source (optional)"
              value={source}
              onChange={(e) => setSource(e.target.value)}
            />
            <button onClick={publishNews}>Publish</button>
          </div>

          {/* 📰 News Feed */}
          <div className="news-section">
            <h2>
              {topic.charAt(0).toUpperCase() + topic.slice(1)} News
            </h2>
            {loading && <p>Loading news...</p>}
            {error && <p className="error">{error}</p>}
            {!loading && filteredNews.length === 0 && (
              <p>No news found for this topic.</p>
            )}
            <div className="news-grid">
              {filteredNews.map((n, i) => (
                <div className="news-card" key={i}>
                  <h3>{n.title || "Untitled"}</h3>
                  <p>{n.content}</p>
                  <small>
                    Source: {n.source || "Unknown"} | Topic: {n.topic}
                  </small>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* ⚓ Footer */}
      <footer>
        <p>© {new Date().getFullYear()} News Aggregator | Powered by Flask + RabbitMQ</p>
      </footer>
    </div>
  );
}

export default App;
