import React from 'react';
import { List, ListItem, ListItemText, Drawer, IconButton } from '@mui/material';
import MenuIcon from '@mui/icons-material/Menu';
import { Link } from 'react-router-dom';

const Sidebar = () => {
  const [isDrawerOpen, setIsDrawerOpen] = React.useState(false);

  const topics = ['general', 'technology', 'sports', 'business', 'health'];

  return (
    <div>
      <IconButton onClick={() => setIsDrawerOpen(true)}>
        <MenuIcon fontSize="large" />
      </IconButton>

      <Drawer anchor="left" open={isDrawerOpen} onClose={() => setIsDrawerOpen(false)}>
        <List>
          {topics.map((topic) => (
            <ListItem button key={topic} component={Link} to={`/${topic}`} onClick={() => setIsDrawerOpen(false)}>
              <ListItemText primary={topic.charAt(0).toUpperCase() + topic.slice(1)} />
            </ListItem>
          ))}
        </List>
      </Drawer>
    </div>
  );
};

export default Sidebar;
