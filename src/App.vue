<template>
  <div id="app">
    <nav class="navbar" v-if="currentUser !== null">
      <div class="nav-brand">
        <router-link to="/">FreelanceHub</router-link>
      </div>
      <div class="nav-links">
        <router-link to="/dashboard" v-if="currentUser.role === 'FREELANCE'">Tableau de bord</router-link>
        <router-link to="/dashboard-client" v-if="currentUser.role === 'CLIENT'">Tableau de bord</router-link>
        <router-link to="/missions" v-if="currentUser.role === 'FREELANCE'">Missions</router-link>
         <router-link to="/missions-client" v-if="currentUser.role === 'CLIENT'">Missions</router-link>
        <router-link to="/freelance-profile" v-if="currentUser.role === 'FREELANCE'">Profil Freelance</router-link>
        <router-link to="/profile">Mon Profil</router-link>
        <router-link to="/missionsApplications" v-if="currentUser.role === 'CLIENT'">Mes Candidatures</router-link>
        <button @click="handleLogout" class="btn-logout">Déconnexion</button>
      </div>
    </nav>
    
    <main class="main-content">
      <router-view 
        :currentUser="currentUser" 
        :setCurrentUser="setCurrentUser"
        :logout="logout"
      />
    </main>
  </div>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      currentUser: null
    };
  },
  methods: {
    setCurrentUser(user) {
      this.currentUser = user;
      if (user) {
        localStorage.setItem('user', JSON.stringify(user));
        if (user.token) {
          localStorage.setItem('token', user.token);
        }
      }
    },
    logout() {
      this.currentUser = null;
      localStorage.removeItem('user');
      localStorage.removeItem('token');
      this.$router.push('/');
    },
    handleLogout() {
      if (confirm('Voulez-vous vraiment vous déconnecter ?')) {
        this.logout();
      }
    }
  },
  mounted() {
    // Récupérer l'utilisateur depuis le localStorage au chargement
    const savedUser = localStorage.getItem('user');
    if (savedUser) {
      try {
        this.currentUser = JSON.parse(savedUser);
      } catch (error) {
        console.error('Erreur lors de la récupération de l\'utilisateur:', error);
        localStorage.removeItem('user');
      }
    }
  }
};
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background-color: #f8fafc;
  color: #334155;
  line-height: 1.6;
}

#app {
  min-height: 100vh;
}

.navbar {
  background: white;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: sticky;
  top: 0;
  z-index: 1000;
}

.nav-brand a {
  font-size: 1.5rem;
  font-weight: 700;
  color: #4f46e5;
  text-decoration: none;
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 2rem;
}

.nav-links a {
  color: #64748b;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.3s;
  padding: 0.5rem 1rem;
  border-radius: 6px;
}

.nav-links a:hover {
  color: #4f46e5;
  background: #f1f5f9;
}

.nav-links a.router-link-active {
  color: #4f46e5;
  background: #e0e7ff;
}

.btn-logout {
  background: #ef4444;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
  transition: background 0.3s;
}

.btn-logout:hover {
  background: #dc2626;
}

.main-content {
  min-height: calc(100vh - 80px);
}

/* Styles globaux pour les boutons */
.btn {
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-weight: 600;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 0.875rem;
  gap: 0.5rem;
}

.btn-primary {
  background: #4f46e5;
  color: white;
}

.btn-primary:hover {
  background: #4338ca;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3);
}

.btn-secondary {
  background: white;
  color: #4f46e5;
  border: 2px solid #4f46e5;
}

.btn-secondary:hover {
  background: #4f46e5;
  color: white;
}

.btn-large {
  padding: 1rem 2rem;
  font-size: 1rem;
}

/* Responsive */
@media (max-width: 768px) {
  .navbar {
    padding: 1rem;
    flex-direction: column;
    gap: 1rem;
  }
  
  .nav-links {
    gap: 1rem;
    flex-wrap: wrap;
    justify-content: center;
  }
}
</style>