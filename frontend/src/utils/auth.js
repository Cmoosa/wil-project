export function getUserFromToken() {
  const token = localStorage.getItem("token");
  if (!token) return null;

  try {
    const payload = JSON.parse(atob(token.split(".")[1]));
    return payload;
  } catch {
    return null;
  }
}

export function hasRole(...roles) {
  const user = getUserFromToken();
  return user && roles.includes(user.role);
}

export const isAuthenticated = () => {
  return Boolean(localStorage.getItem("token"));
};

export const logout = () => {
  localStorage.removeItem("token");
  window.location.href = "/login";
};

