/* eslint-disable no-param-reassign */
import axios from 'axios';

export default function jwtInterceptor() {
  axios.defaults.baseURL = 'http://127.0.0.1:5000';

  axios.interceptors.request.use((request) => {
    if (localStorage.accessToken) {
      request.headers.Authorization = `Bearer ${localStorage.accessToken}`;
    }
    return request;
  });
}
