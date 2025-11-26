import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// === Intercepteurs ===
api.interceptors.request.use((config) => {
  const user = JSON.parse(localStorage.getItem('user'));
  if (user) {
    if (user.token) {
      config.headers.Authorization = `Bearer ${user.token}`;
    }
    if (user.id) {
      config.headers['User-ID'] = user.id; // 🔥 Pour le backend Flask
    }
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
export const getPortfolioItems = (profileId) => api.get(`/profiles/${profileId}/portfolio`);
export const addPortfolioItem = (profileId, data) => api.post(`/profiles/${profileId}/portfolio`, data);
export const getPortfolioItem = (profileId, itemId) => api.get(`/profiles/${profileId}/portfolio/${itemId}`);
export const updatePortfolioItem = (profileId, itemId, data) => api.put(`/profiles/${profileId}/portfolio/${itemId}`, data);
export const deletePortfolioItem = (profileId, itemId) => api.delete(`/profiles/${profileId}/portfolio/${itemId}`);

// === MISSIONS ===
export const getMissions = (params = {}) => api.get('/missions', { params });

// FIX: Backticks manquants au début
export const getMission = (missionId) => api.get(`/missions/${missionId}`);

export const createMission = (data) => api.post('/missions', data);

// FIX: Backticks manquants au début et données en 3e paramètre
export const updateMission = (missionId, data) => api.put(`/missions/${missionId}`, data);

// FIX: Backticks manquants au début
export const deleteMission = (missionId) => api.delete(`/missions/${missionId}`);

// FIX: Backticks manquants au début
export const applyToMission = (missionId, data) => api.post(`/missions/${missionId}/apply`, data);

// FIX: Backticks manquants au début
export const getUserMissions = (userId) => api.get(`/users/${userId}/missions`);

// FIX: Backticks manquants au début
export const getUserApplications = (userId) => api.get(`/users/${userId}/applications`);

// FIX: Backticks manquants au début
export const getMissionLastOffers = () => api.get(`/missions/last`);

// FIX: Backticks manquants au début
export const getFreelanceMissions = (freelanceId) => api.get(`/freelancers/${freelanceId}/missions`);

// FIX: Backticks manquants au début
export const getRecommendedFreelancers = (missionId) => api.get(`/missions/${missionId}/recommended-freelancers`);

// FIX: Backticks manquants au début
export const getClientMissionsAppliedByFreelance = (clientId) => api.get(`/clients/${clientId}/missions-applied-by-freelance`);

// FIX: Backticks manquants au début
export const getFreelanceAppliedMissions = (freelanceId) => api.get(`/freelancers/${freelanceId}/missions-applied`);

// FIX: Backticks manquants au début
export const getMissionApplications = (missionId) => api.get(`/missions/${missionId}/applications`);
export const updateApplicationStatus = (applicationId, data) => api.put(`/applications/${applicationId}/status`, data);
export const getFreelanceActiveMissions = () => api.get(`/freelance/missions/active`);
export const getMissionDetailed = (missionId) => api.get(`/missions/${missionId}/detailed`);
export const completeOrCancelMission = (mission_id, data) => api.put(`/missions/${mission_id}/status`, data);

export const getMyMissions = () => {
  const user = JSON.parse(localStorage.getItem('user'));
  if (user?.id) return getUserMissions(user.id);
  return Promise.reject(new Error('User not logged in'));
};

export const getMyApplications = () => {
  const user = JSON.parse(localStorage.getItem('user'));
  if (user?.id) return getUserApplications(user.id);
  return Promise.reject(new Error('User not logged in'));
};

// === MESSAGES ===
export const getConversations = () => api.get('/messages/conversations');
export const getMessages = (userId) => api.get(`/messages/${userId}`);
export const sendMessage = (data) => api.post('/messages', data);

export default api;
