export default function isAuthenticated() {
  return !!localStorage.getItem('accessToken');
}
