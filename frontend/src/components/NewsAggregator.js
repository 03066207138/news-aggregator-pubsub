import React, { useState, useEffect } from 'react';
import axios from 'axios';
import {
  Container,
  Typography,
  Grid,
  CircularProgress,
  Alert,
  Button,
  Card,
  CardContent,
  CardMedia,
  Snackbar,
  Drawer,
  List,
  ListItem,
  ListItemText,
  TextField,
  IconButton,
} from '@mui/material';
import MenuIcon from '@mui/icons-material/Menu';

const NewsAggregator = () => {
  const [articles, setArticles] = useState([]);
  const [filteredArticles, setFilteredArticles] = useState([]); // For search functionality
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  const [selectedTopic, setSelectedTopic] = useState('general'); // Default topic
  const [openSnackbar, setOpenSnackbar] = useState(false); // Snackbar state for subscription success
  const [snackbarMessage, setSnackbarMessage] = useState(''); // Snackbar message content
  const [searchQuery, setSearchQuery] = useState(''); // Search bar state
  const [isDrawerOpen, setIsDrawerOpen] = useState(false); // Side navigation state

  // Fetch articles based on the selected topic
  const fetchArticles = async (topic) => {
    setLoading(true);
    setError(null); // Reset error
    try {
      const response = await axios.get(`http://localhost:5000/news?topic=${topic}`);
      setArticles(response.data.articles || []);
      setFilteredArticles(response.data.articles || []); // Initialize filtered articles
    } catch (err) {
      console.error('Error fetching articles: ', err);
      setError('Connect to internet.');
    } finally {
      setLoading(false);
    }
  };

  // Handle topic subscription
  const handleSubscription = async (topic) => {
    try {
      const response = await axios.post('http://localhost:5000/subscribe', { topic });
      setSelectedTopic(topic); // Update the selected topic
      fetchArticles(topic); // Fetch news for the selected topic

      // Show the snackbar with a success message
      setSnackbarMessage(`Successfully subscribed to ${topic} news`);
      setOpenSnackbar(true); // Open the snackbar
      setIsDrawerOpen(false); // Close the drawer
    } catch (err) {
      console.error('Error subscribing: ', err);
      setError('Failed to subscribe to the topic.');
    }
  };

  // Handle search input changes
  const handleSearch = (e) => {
    const query = e.target.value.toLowerCase();
    setSearchQuery(query);

    if (query.trim() === '') {
      setFilteredArticles(articles); // Reset to all articles if search is cleared
    } else {
      const filtered = articles.filter((article) =>
        article.title.toLowerCase().includes(query) ||
        (article.description && article.description.toLowerCase().includes(query))
      );
      setFilteredArticles(filtered);
    }
  };

  useEffect(() => {
    // Initial fetch for the default topic
    fetchArticles(selectedTopic);
  }, []); // Empty dependency array to run once on mount

  // Close the Snackbar
  const handleCloseSnackbar = () => {
    setOpenSnackbar(false); // Close the snackbar
  };

  if (loading) {
    return (
      <Container style={{ textAlign: 'center', marginTop: '50px' }}>
        <CircularProgress size={60} />
      </Container>
    );
  }

  return (
    <Container>
      {/* Header */}
      <Typography
        variant="h4"
        gutterBottom
        align="center"
        style={{ marginTop: '20px' }}
      >
        {selectedTopic.charAt(0).toUpperCase() + selectedTopic.slice(1)} News
      </Typography>
      {/* Search Bar */}
      <TextField
        fullWidth
        placeholder="Search articles..."
        value={searchQuery}
        onChange={handleSearch}
        variant="outlined"
        style={{ marginBottom: '20px' }}
      />

      {/* Side Navigation (Sidenav) */}
      <IconButton onClick={() => setIsDrawerOpen(true)} style={{ marginBottom: '20px' }}>
        <MenuIcon fontSize="large" />
      </IconButton>
      <Drawer anchor="left" open={isDrawerOpen} onClose={() => setIsDrawerOpen(false)}>
        <List>
          {['general', 'technology', 'sports', 'business', 'health'].map((topic, index) => (
            <ListItem button key={index} onClick={() => handleSubscription(topic)}>
              <ListItemText primary={topic.charAt(0).toUpperCase() + topic.slice(1)} />
            </ListItem>
          ))}
        </List>
      </Drawer>

      {/* Error Alert */}
      {error && (
        <Alert severity="error" style={{ marginBottom: '20px' }}>
          {error}
        </Alert>
      )}

      {/* News Articles */}
      <Grid container spacing={3}>
        {filteredArticles.length > 0 ? (
          filteredArticles.map((article, index) => (
            <Grid item xs={12} sm={6} md={4} key={index}>
              <Card>
                <CardMedia
                  component="img"
                  height="140"
                  image={article.urlToImage || 'https://via.placeholder.com/300'}
                  alt={article.title}
                />
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    {article.title}
                  </Typography>
                  <Typography variant="body2" color="textSecondary" paragraph>
                    {article.description || 'No description available.'}
                  </Typography>
                  {article.url && (
                    <a href={article.url} target="_blank" rel="noopener noreferrer">
                      <Button size="small" color="primary">
                        Read More
                      </Button>
                    </a>
                  )}
                </CardContent>
              </Card>
            </Grid>
          ))
        ) : (
          <Typography variant="h6" color="textSecondary" align="center" style={{ marginTop: '20px' }}>
            No articles found for the selected topic or search term.
          </Typography>
        )}
      </Grid>

      {/* Snackbar for Subscription Confirmation */}
      <Snackbar
        open={openSnackbar}
        autoHideDuration={3000}
        onClose={handleCloseSnackbar}
        message={snackbarMessage}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
      />
    </Container>
  );
};

export default NewsAggregator;
