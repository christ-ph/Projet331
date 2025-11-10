<template>
  <div class="register-page">
    <div class="register-container">
      <div class="register-left">
        <h1>Rejoignez notre communauté</h1>
        <p>Inscrivez-vous pour découvrir des talents ou proposer vos services.</p>
        <div class="illustration">
          <div class="icon">🚀</div>
          <p>Commencez votre aventure freelance</p>
        </div>
      </div>

      <div class="register-right">
        <div class="register-card">
          <h2>Créer un compte</h2>
          <form @submit.prevent="register" class="register-form">
            <div class="form-section">
              <h3>Informations de connexion</h3>
              <div class="form-group">
                <label for="email">Email *</label>
                <input 
                  v-model="form.email" 
                  type="email" 
                  id="email"
                  placeholder="votre@email.com" 
                  required 
                />
              </div>
              
              <div class="form-group">
                <label for="password">Mot de passe *</label>
                <input 
                  v-model="form.password" 
                  type="password" 
                  id="password"
                  placeholder="Minimum 6 caractères" 
                  required 
                  minlength="6"
                />
              </div>

              <div class="form-group">
                <label for="role">Je suis *</label>
                <select v-model="form.role" id="role" required>
                  <option value="">Choisissez votre rôle</option>
                  <option value="FREELANCE">Freelance</option>
                  <option value="CLIENT">Client</option>
                </select>
              </div>
            </div>

            <div class="form-section" v-if="form.role">
              <h3>Informations personnelles</h3>
              <div class="form-row">
                <div class="form-group">
                  <label for="first_name">Prénom</label>
                  <input 
                    v-model="form.first_name" 
                    id="first_name"
                    placeholder="Votre prénom" 
                  />
                </div>
                <div class="form-group">
                  <label for="last_name">Nom</label>
                  <input 
                    v-model="form.last_name" 
                    id="last_name"
                    placeholder="Votre nom" 
                  />
                </div>
              </div>
              
              <div class="form-group">
                <label for="title">Titre professionnel</label>
                <input 
                  v-model="form.title" 
                  id="title"
                  :placeholder="form.role === 'FREELANCE' ? 'Développeur Full Stack' : 'CEO, Manager...'" 
                />
              </div>

              <div class="form-group">
                <label for="description">Description</label>
                <textarea 
                  v-model="form.description" 
                  id="description"
                  placeholder="Parlez-nous de vous..." 
                  rows="3"
                ></textarea>
              </div>

              <div class="form-group" v-if="form.role === 'CLIENT'">
                <label for="company_name">Nom de l'entreprise</label>
                <input 
                  v-model="form.company_name" 
                  id="company_name"
                  placeholder="Le nom de votre entreprise" 
                />
              </div>

              <div class="form-group" v-if="form.role === 'FREELANCE'">
                <label for="hourly_rate">Taux horaire (€)</label>
                <input 
                  v-model.number="form.hourly_rate" 
                  type="number" 
                  id="hourly_rate"
                  placeholder="50" 
                  min="0"
                />
              </div>
            </div>

            <button type="submit" class="btn btn-primary btn-full" :disabled="loading">
              <span v-if="loading">Création du compte...</span>
              <span v-else>Créer mon compte</span>
            </button>
          </form>

          <p class="login-link">
            Déjà un compte ? <router-link to="/login">Connectez-vous</router-link>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { register, setUserProfile } from '@/services/api';

export default {
  name: 'RegisterView',
  props: ['setCurrentUser'],
  data() {
    return {
      form: {
        email: '',
        password: '',
        role: '',
        first_name: '',
        last_name: '',
        title: '',
        description: '',
        company_name: '',
        hourly_rate: null,
        availability: 'AVAILABLE',
        skills: [],
      },
      loading: false,
    };
  },
  methods: {
    async register() {
      // 1️⃣ Vérification des champs obligatoires
      if (!this.form.email || !this.form.password || !this.form.role) {
        alert('Veuillez remplir tous les champs obligatoires');
        return;
      }

      if (this.form.password.length < 6) {
        alert('Le mot de passe doit contenir au moins 6 caractères');
        return;
      }

      this.loading = true;

      try {
        console.log('Début du processus d’inscription...');

        // 2️⃣ Création de l’utilisateur
        const userResponse = await register({
          email: this.form.email,
          password: this.form.password,
          role: this.form.role
        });

        if (!userResponse?.data?.user_id) {
          alert(userResponse.data?.message || 'Erreur lors de l’inscription');
          return;
        }

        const userId = userResponse.data.user_id;

        // 3️⃣ Préparation du profil utilisateur
        const profileData = {
          first_name: this.form.first_name || '',
          last_name: this.form.last_name || '',
          description: this.form.description || '',
        };

        if (this.form.role === 'FREELANCE') {
          profileData.title = this.form.title || '';
          profileData.hourly_rate = this.form.hourly_rate || 0;
          profileData.availability = this.form.availability || 'AVAILABLE';
          profileData.skills = this.form.skills || [];
        } else if (this.form.role === 'CLIENT') {
          profileData.company_name = this.form.company_name || '';
        }

        // Nettoyage : supprimer les champs inutiles
        if (this.form.role === 'FREELANCE' && 'company_name' in profileData) {
          delete profileData.company_name;
        }

        console.log('Profil à envoyer au backend :', profileData);

        // 4️⃣ Envoi du profil au backend
        const profileResponse = await setUserProfile(userId, profileData);

        if (![200, 201].includes(profileResponse.status)) {
          throw new Error(profileResponse.data?.message || 'Erreur lors de la création du profil');
        }

        // 5️⃣ Construction de l’objet utilisateur complet
        const userWithProfile = {
          id: userId,
          email: this.form.email,
          role: this.form.role,
          token: userResponse.data.token,
          freelance_profile: this.form.role === 'FREELANCE' ? profileData : null,
          client_profile: this.form.role === 'CLIENT' ? profileData : null,
        };

        // 6️⃣ Mise à jour du contexte global (parent)
        this.setCurrentUser(userWithProfile);

        // 7️⃣ Sauvegarde locale du profil
        if (this.form.role === 'FREELANCE') {
          localStorage.setItem(
            'freelance_profile_data',
            JSON.stringify({ profile: userWithProfile.freelance_profile })
          );
        }

        // 8️⃣ Redirection selon le rôle
        if (this.form.role === 'CLIENT') {
          this.$router.push('/dashboard-client');
        } else if (this.form.role === 'FREELANCE') {
          this.$router.push('/dashboard');
        }

        console.log('✅ Inscription terminée avec succès !');

      } catch (err) {
        console.error('❌ Erreur complète d’inscription :', err);
        alert(err.message || 'Erreur lors de l’inscription. Veuillez réessayer.');
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>







<!-- <script>
import { register, setUserProfile } from '@/services/api';

export default {
  name: 'RegisterView',
  props: ['setCurrentUser'],
  data() {
    return {
      form: {
        email: '',
        password: '',
        role: '',
        first_name: '',
        last_name: '',
        title: '',
        description: '',
        company_name: ''
      },
      loading: false
    };
  },
  methods: {
    async register() {
      if (!this.form.email || !this.form.password || !this.form.role) {
        alert('Veuillez remplir tous les champs obligatoires');
        return;
      }

      if (this.form.password.length < 6) {
        alert('Le mot de passe doit contenir au moins 6 caractères');
        return;
      }

      this.loading = true;

       try {  
        // 1. Création de l'utilisateur
        const userData = {
          email: this.form.email,
          password: this.form.password,
          role: this.form.role
        };
        
        const userResponse = await register(userData);
        
        if (userResponse.data) {
          const userId = userResponse.data.user_id;
          
          // 2. Création du profil si des informations sont fournies
          const profileData = {
            first_name: this.form.first_name,
            last_name: this.form.last_name,
            title: this.form.title,
            description: this.form.description,
            company_name: this.form.company_name
          };
          
          // Filtrer les champs vides
          const filteredProfileData = Object.fromEntries(
            Object.entries(profileData).filter(([_, value]) => value !== '')
          );
          
          if (Object.keys(filteredProfileData).length > 0) {
            await setUserProfile(userId, filteredProfileData);
          }
          
          // 3. Connexion automatique
          const userWithToken = {
            id: userId,
            email: this.form.email,
            role: this.form.role,
            token: userResponse.data.token, // Si votre API retourne un token
            ...filteredProfileData
          };
          
          this.setCurrentUser(userWithToken);
          this.$router.push('/dashboard');
        } else {
          alert(userResponse.data.message);
        }
        
        
      } catch (error) {
        console.error('Erreur d\'inscription:', error);
        alert('Erreur lors de l\'inscription. Veuillez réessayer.');
      } finally {
        this.loading = false;
      }
    }
  }
  };

</script> -->

<style scoped>
.register-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 1rem;
}

.register-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  max-width: 1100px;
  width: 100%;
  background: white;
  border-radius: 20px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  min-height: 700px;
}

.register-left {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
  padding: 3rem;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
}

.register-left h1 {
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 1rem;
  line-height: 1.2;
}

.register-left p {
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

.register-right {
  padding: 2rem;
  display: flex;
  align-items: center;
  overflow-y: auto;
}

.register-card {
  width: 100%;
  max-width: 500px;
  margin: 0 auto;
}

.register-card h2 {
  font-size: 2rem;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 2rem;
  text-align: center;
}

.register-form {
  margin-bottom: 2rem;
}

.form-section {
  margin-bottom: 2rem;
  padding-bottom: 2rem;
  border-bottom: 1px solid #e5e7eb;
}

.form-section:last-of-type {
  border-bottom: none;
  margin-bottom: 1rem;
}

.form-section h3 {
  font-size: 1.125rem;
  font-weight: 600;
  color: #374151;
  margin-bottom: 1.5rem;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid #f3f4f6;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
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

.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 0.875rem 1rem;
  border: 2px solid #e5e7eb;
  border-radius: 10px;
  font-size: 1rem;
  transition: all 0.3s;
  background: #fafafa;
  font-family: inherit;
}

.form-group textarea {
  resize: vertical;
  min-height: 80px;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #10b981;
  background: white;
  box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.1);
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

.login-link {
  text-align: center;
  color: #6b7280;
}

.login-link a {
  color: #10b981;
  font-weight: 600;
  text-decoration: none;
}

.login-link a:hover {
  text-decoration: underline;
}

/* Responsive */
@media (max-width: 768px) {
  .register-container {
    grid-template-columns: 1fr;
    max-width: 500px;
  }
  
  .register-left {
    padding: 2rem;
    display: none;
  }
  
  .register-right {
    padding: 2rem;
  }
  
  .form-row {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 480px) {
  .register-page {
    padding: 0.5rem;
  }
  
  .register-right {
    padding: 1.5rem;
  }
  
  .register-card h2 {
    font-size: 1.75rem;
  }
}
</style>