import jwtDecode from 'jwt-decode';

export default function getUsername() {
  return jwtDecode(localStorage.getItem('accessToken')).sub;
}
