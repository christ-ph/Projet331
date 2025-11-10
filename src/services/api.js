
import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// === Intercepteurs ===

// Token d'authentification
api.interceptors.request.use((config) => {
  const user = JSON.parse(localStorage.getItem('user'));
  if (user && user.token) {
    config.headers.Authorization = `Bearer ${user.token}`;
  }
  return config;
});

// Gestion des erreurs globales
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// === AUTHENTIFICATION ===
export const login = (data) => api.post('/login', data);
export const register = (data) => api.post('/register', data);

// === USERS ===
export const setUserProfile = (userId, data) => api.post(`/users/${userId}/profile`, data);
export const getUsers = () => api.get('/users');
export const updateUser = (id, data) => api.put(`/users/${id}`, data);
export const deleteUser = (id) => api.delete(`/users/${id}`);

// === FREELANCES ===
export const getProfiles = () => api.get('/profiles');
export const createProfile = (data) => api.post('/profiles', data);
export const getProfile = (userId) => api.get(`/profiles/${userId}`);
export const updateProfile = (userId, data) => api.put(`/profiles/${userId}`, data);
export const deleteProfile = (userId) => api.delete(`/profiles/${userId}`);

// === PORTFOLIO ===

// ✅ Récupérer tous les projets d’un freelance
export const getPortfolioItems = (profileId) =>
  api.get(`/profiles/${profileId}/portfolio`);

// ✅ Ajouter un projet
export const addPortfolioItem = (profileId, data) =>
  api.post(`/profiles/${profileId}/portfolio`, data);

// ✅ Récupérer un projet spécifique
export const getPortfolioItem = (profileId, itemId) =>
  api.get(`/profiles/${profileId}/portfolio/${itemId}`);

// ✅ Mettre à jour un projet
export const updatePortfolioItem = (profileId, itemId, data) =>
  api.put(`/profiles/${profileId}/portfolio/${itemId}`, data);

// ✅ Supprimer un projet
export const deletePortfolioItem = (profileId, itemId) =>
  api.delete(`/profiles/${profileId}/portfolio/${itemId}`);

// === MISSIONS ===
export const getMissions = (params = {}) => api.get('/missions', { params });
export const getMission = (id) => api.get(`/missions/${id}`);
export const createMission = (data) => api.post('/missions', data);
export const applyToMission = (missionId, data) =>
  api.post(`/missions/${missionId}/apply`, data);
export const getMyApplications = () => api.get('/applications/my');

// === MESSAGES ===
export const getConversations = () => api.get('/messages/conversations');
export const getMessages = (userId) => api.get(`/messages/${userId}`);
export const sendMessage = (data) => api.post('/messages', data);

export default api;


// import axios from 'axios';

// const API_BASE_URL = 'http://localhost:5000/api';

// const api = axios.create({
//   baseURL: API_BASE_URL,
//   headers: {
//     'Content-Type': 'application/json',
//   },
// });

// // Intercepteur pour ajouter le token d'authentification
// api.interceptors.request.use((config) => {
//   const user = JSON.parse(localStorage.getItem('user'));
//   if (user && user.token) {
//     config.headers.Authorization = `Bearer ${user.token}`;
//   }
//   return config;
// });

// // Intercepteur pour gérer les erreurs
// api.interceptors.response.use(
//   (response) => response,
//   (error) => {
//     if (error.response?.status === 401) {
//       localStorage.removeItem('user');
//       window.location.href = '/login';
//     }
//     return Promise.reject(error);
//   }
// );

// // Auth
// export const login = (data) => api.post('/login', data);
// export const register = (data) => api.post('/register', data);

// // Users
// export const setUserProfile = (userId, data) => api.post(`/users/${userId}/profile`, data);
// export const getUsers = () => api.get('/users');
// export const updateUser = (id, data) => api.put(`/users/${id}`, data);
// export const deleteUser = (id) => api.delete(`/users/${id}`);

// // Freelance Profiles
// export const getProfiles = () => api.get('/profiles');
// //export const createProfile = (data) => api.post('/profiles', data);
// export const updateProfile = (id, data) => api.put(`/profiles/${id}`, data);
// export const deleteProfile = (id) => api.delete(`/profiles/${id}`);
// export const addPortfolioItem = (profileId, data) => api.post(`/profiles/${profileId}/portfolio`, data);
// export const removePortfolioItem = (itemId) => api.delete(`/portfolio/${itemId}`);

// // Missions - NOUVEAU pour Module 1
// export const getMissions = (params = {}) => api.get('/missions', { params });
// export const getMission = (id) => api.get(`/missions/${id}`);
// export const createMission = (data) => api.post('/missions', data);
// export const applyToMission = (missionId, data) => api.post(`/missions/${missionId}/apply`, data);
// export const getMyApplications = () => api.get('/applications/my');

// // Messages - NOUVEAU pour Module 1
// export const getConversations = () => api.get('/messages/conversations');
// export const getMessages = (userId) => api.get(`/messages/${userId}`);
// export const sendMessage = (data) => api.post('/messages', data);

// export default api;