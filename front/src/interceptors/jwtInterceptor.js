/* eslint-disable no-param-reassign */
import axios from 'axios';

export default function jwtInterceptor() {
  axios.defaults.baseURL = 'https://duveter-back.azurewebsites.net';

  axios.interceptors.request.use((request) => {
    if (localStorage.accessToken) {
      request.headers.Authorization = `Bearer ${localStorage.accessToken}`;
    }
    return request;
  });
}
