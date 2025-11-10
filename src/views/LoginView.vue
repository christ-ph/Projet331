<template>
  <div class="login-page">
    <div class="login-container">
      <div class="login-left">
        <h1>Content de vous revoir !</h1>
        <p>Connectez-vous pour accéder à votre espace personnel.</p>
        <div class="illustration">
          <div class="icon">👨‍💻</div>
          <p>Plateforme Freelance</p>
        </div>
      </div>
      <div class="login-right">
        <div class="login-card">
          <h2>Connexion</h2>
          <form @submit.prevent="login" class="login-form">
            <div class="form-group">
              <label for="email">Email</label>
              <input 
                v-model="form.email" 
                type="email" 
                id="email"
                placeholder="votre@email.com" 
                required 
              />
            </div>
            <div class="form-group">
              <label for="password">Mot de passe</label>
              <input 
                v-model="form.password" 
                type="password" 
                id="password"
                placeholder="Votre mot de passe" 
                required 
              />
            </div>
            <button type="submit" class="btn btn-primary btn-full" :disabled="loading">
              <span v-if="loading">Connexion...</span>
              <span v-else>Se connecter</span>
            </button>
            <div class="demo-accounts" v-if="!loading">
              <p class="demo-title">Comptes de démonstration :</p>
              <div class="demo-buttons">
                <button type="button" @click="fillDemo('freelance')" class="btn-demo">
                  Freelance
                </button>
                <button type="button" @click="fillDemo('client')" class="btn-demo">
                  Client
                </button>
              </div>
            </div>
          </form>
          <p class="register-link">
            Pas de compte ? <router-link to="/register">Inscrivez-vous</router-link>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { login } from '@/services/api';

export default {
  name: 'LoginView',
  props: ['setCurrentUser'],
  data() {
    return {
      form: {
        email: '',
        password: ''
      },
      loading: false,
      demoAccounts: {
        freelance: {
          email: 'freelance@demo.com',
          password: 'demo123'
        },
        client: {
          email: 'client@demo.com',
          password: 'demo123'
        }
      }
    };
  },
  methods: {
    fillDemo(type) {
      if (this.demoAccounts[type]) {
        this.form.email = this.demoAccounts[type].email;
        this.form.password = this.demoAccounts[type].password;
      }
    },
    async login() {
      if (!this.form.email || !this.form.password) {
        alert('Veuillez remplir tous les champs');
        return;
      }

      this.loading = true;
      try {
        const credentials = {
          'email': this.form.email,
          'pass': this.form.password
        };
        
        const response = await login(credentials);
        
        if (response.data) {
          const userData = {
            ...response.data.data,
            token: response.data.token
          };
          
          this.setCurrentUser(userData);
          
          // Redirection selon le rôle
          if (userData.role === "CLIENT") {
            this.$router.push('/dashboard-client');
          } else {
            this.$router.push('/dashboard');
          }
        } else {
          alert(response.data.message || 'Erreur de connexion');
        }
      } catch (error) {
        console.error('Erreur de connexion:', error);
        alert('Erreur lors de la connexion. Vérifiez vos identifiants.');
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 1rem;
}

.login-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  max-width: 1000px;
  width: 100%;
  background: white;
  border-radius: 20px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  min-height: 600px;
}

.login-left {
  background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
  color: white;
  padding: 3rem;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
}

.login-left h1 {
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 1rem;
  line-height: 1.2;
}

.login-left p {
  font-size: 1.125rem;
  opacity: 0.9;
  margin-bottom: 2rem;
}

.illustration {
  margin-top: 2rem;
}

.illustration .icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.illustration p {
  font-size: 1rem;
  font-weight: 500;
}

.login-right {
  padding: 3rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.login-card {
  width: 100%;
  max-width: 400px;
}

.login-card h2 {
  font-size: 2rem;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 2rem;
  text-align: center;
}

.login-form {
  margin-bottom: 2rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #374151;
}

.form-group input {
  width: 100%;
  padding: 0.875rem 1rem;
  border: 2px solid #e5e7eb;
  border-radius: 10px;
  font-size: 1rem;
  transition: all 0.3s;
  background: #fafafa;
}

.form-group input:focus {
  outline: none;
  border-color: #4f46e5;
  background: white;
  box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
}

.btn-full {
  width: 100%;
  padding: 1rem;
  font-size: 1rem;
  margin-top: 1rem;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none !important;
}

.demo-accounts {
  margin-top: 2rem;
  padding-top: 2rem;
  border-top: 1px solid #e5e7eb;
}

.demo-title {
  text-align: center;
  color: #6b7280;
  margin-bottom: 1rem;
  font-size: 0.875rem;
}

.demo-buttons {
  display: flex;
  gap: 0.5rem;
}

.btn-demo {
  flex: 1;
  padding: 0.75rem;
  background: #f3f4f6;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  color: #374151;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-demo:hover {
  background: #e5e7eb;
  border-color: #9ca3af;
}

.register-link {
  text-align: center;
  color: #6b7280;
}

.register-link a {
  color: #4f46e5;
  font-weight: 600;
  text-decoration: none;
}

.register-link a:hover {
  text-decoration: underline;
}

/* Responsive */
@media (max-width: 768px) {
  .login-container {
    grid-template-columns: 1fr;
    max-width: 400px;
  }
  
  .login-left {
    padding: 2rem;
    display: none; /* Cacher l'illustration sur mobile */
  }
  
  .login-right {
    padding: 2rem;
  }
}

@media (max-width: 480px) {
  .login-page {
    padding: 0.5rem;
  }
  
  .login-right {
    padding: 1.5rem;
  }
  
  .demo-buttons {
    flex-direction: column;
  }
}
</style>