// SubscriptionForm.js
import React, { useState } from 'react';

function SubscriptionForm() {
  const [topic, setTopic] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (topic) {
      // Make API call to subscribe
      try {
        const response = await fetch('http://localhost:5000/subscribe', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ topic }),
        });
        const data = await response.json();
        console.log(data);
      } catch (error) {
        console.error('Error subscribing:', error);
      }
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={topic}
          onChange={(e) => setTopic(e.target.value)}
          placeholder="Enter topic to subscribe"
        />
        <button type="submit">Subscribe</button>
      </form>
    </div>
  );
}

export default SubscriptionForm; // Make sure to export the component
