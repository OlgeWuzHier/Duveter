import axios from 'axios';

const baseURL = 'http://127.0.0.1:5000';

export default axios.create({
  baseURL,
  headers: {
    'Content-Type': 'application/json',
    Authorization: `Bearer ${localStorage.accessToken}`,
  },
});
