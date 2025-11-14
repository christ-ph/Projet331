<template>
  <div class="dashboard" v-if="currentUser">
    <div class="dashboard-header">
      <div class="welcome-section">
        <h1>Tableau de bord</h1>
        <p class="welcome-message">Bon retour, <strong>{{ currentUser.email }}</strong> !</p>
        <p class="welcome-subtitle" v-if="currentUser.role === 'FREELANCE'">
          Prêt à donner une nouvelle mission ? Client
        </p>
        <p class="welcome-subtitle" v-else>
          Trouvez le talent parfait pour votre projet.
        </p>
      </div>
      <div class="header-actions">
        <router-link 
          v-if="currentUser.role === 'FREELANCE'" 
          to="/freelance-profile" 
          class="btn btn-primary"
        >
          ✨ Compléter mon profil
        </router-link>
        <router-link to="/missions" class="btn btn-secondary">
          📋 Voir les missions
        </router-link>
      </div>
    </div>

    <div class="dashboard-content">
      <!-- Pour les freelances -->
      <div v-if="currentUser.role === 'FREELANCE'" class="freelance-dashboard">
        <div class="stats-grid">
          <div class="stat-card primary">
            <div class="stat-icon">🚀</div>
            <div class="stat-content">
              <h3>Missions actives</h3>
              <p class="stat-number">{{ stats.activeMissions }}</p>
              <p class="stat-trend">+2 cette semaine</p>
            </div>
          </div>
          
          <div class="stat-card success">
            <div class="stat-icon">💼</div>
            <div class="stat-content">
              <h3>Candidatures envoyées</h3>
              <p class="stat-number">{{ stats.proposalsSent }}</p>
              <p class="stat-trend">12 ce mois</p>
            </div>
          </div>
          
          <div class="stat-card warning">
            <div class="stat-icon">⭐</div>
            <div class="stat-content">
              <h3>Note moyenne</h3>
              <p class="stat-number">{{ stats.averageRating }}/5</p>
              <p class="stat-trend">24 avis</p>
            </div>
          </div>
          
          <div class="stat-card info">
            <div class="stat-icon">💰</div>
            <div class="stat-content">
              <h3>Revenus estimés</h3>
              <p class="stat-number">{{ stats.estimatedEarnings }}€</p>
              <p class="stat-trend">Ce mois</p>
            </div>
          </div>
        </div>

        <div class="content-grid">
          <div class="content-section">
            <div class="section-header">
              <h3>🎯 Offres recommandées</h3>
              <router-link to="/missions" class="see-all">Tout voir</router-link>
            </div>
            <div class="offers-list">
              <div v-for="offer in latestOffers" :key="offer.id" class="offer-card">
                <div class="offer-header">
                  <h4>{{ offer.title }}</h4>
                  <span class="budget">{{ offer.budget }}€</span>
                </div>
                <p class="offer-description">{{ offer.description }}</p>
                <div class="offer-meta">
                  <span class="deadline">⏱️ {{ offer.deadline }}</span>
                  <span class="skills">{{ offer.skills.join(', ') }}</span>
                </div>
                <div class="offer-actions">
                  <button @click="viewMission(offer.id)" class="btn btn-secondary btn-small">
                    Voir détails
                  </button>
                  <button @click="applyToMission(offer.id)" class="btn btn-primary btn-small">
                    Postuler
                  </button>
                </div>
              </div>
            </div>
            <div class="see-more-container" v-if="clientMissions.length > 2">
              <button @click="showAllMissions = !showAllMissions" class="btn btn-outline">
                {{ showAllMissions ? '← Voir moins' : 'Voir plus de missions →' }}
              </button>
            </div>
          </div>

          <div class="content-section">
            <div class="section-header">
              <h3>📈 Mes missions</h3>
              <span class="badge">{{ recentMissions.length }}</span>
            </div>
            <div class="missions-list">
              <div v-for="mission in recentMissions" :key="mission.id" class="mission-card">
                <div class="mission-status" :class="mission.status"></div>
                <div class="mission-content">
                  <h4>{{ mission.title }}</h4>
                  <p class="mission-client">Client: {{ mission.client }}</p>
                  <div class="mission-progress">
                    <div class="progress-bar">
                      <div 
                        class="progress-fill" 
                        :style="{ width: mission.progress + '%' }"
                      ></div>
                    </div>
                    <span class="progress-text">{{ mission.progress }}%</span>
                  </div>
                  <p class="mission-deadline">Échéance: {{ mission.deadline }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Pour les clients -->
      <div v-else-if="currentUser.role === 'CLIENT'" class="client-dashboard">
        <div class="stats-grid">
          <div class="stat-card primary">
            <div class="stat-icon">📊</div>
            <div class="stat-content">
              <h3>Missions publiées</h3>
              <p class="stat-number">{{ stats.publishedMissions }}</p>
              <p class="stat-trend">3 actives</p>
            </div>
          </div>
          
          <div class="stat-card success">
            <div class="stat-icon">📨</div>
            <div class="stat-content">
              <h3>Propositions reçues</h3>
              <p class="stat-number">{{ stats.proposalsReceived }}</p>
              <p class="stat-trend">12 en attente</p>
            </div>
          </div>
          
          <div class="stat-card warning">
            <div class="stat-icon">⚡</div>
            <div class="stat-content">
              <h3>Missions actives</h3>
              <p class="stat-number">{{ stats.activeMissions }}</p>
              <p class="stat-trend">En cours</p>
            </div>
          </div>
          
          <div class="stat-card info">
            <div class="stat-icon">✅</div>
            <div class="stat-content">
              <h3>Taux de réussite</h3>
              <p class="stat-number">{{ stats.successRate }}%</p>
              <p class="stat-trend">Projets terminés</p>
            </div>
          </div>
        </div>

        <div class="content-grid">
          <div class="content-section">
            <div class="section-header">
              <h3>📋 Mes missions récentes</h3>
              <router-link to="/missions?my=true" class="see-all">Gérer</router-link>
            </div>
            <div class="missions-list">
              <div v-for="mission in displayedMissions" :key="mission.id" class="mission-card">
                <div class="mission-status" :class="mission.status"></div>
                <div class="mission-content">
                  <h4>{{ mission.title }}</h4>
                  <p class="mission-meta">
                    <span class="proposals">📨 {{ mission.proposalsCount }} propositions</span>
                    <span class="budget">💰 {{ mission.budget }}€</span>
                  </p>
                  <p class="mission-deadline">⏱️ {{ mission.deadline }}</p>
                  <div class="mission-actions">
                    <button @click="viewMission(mission.id)" class="btn btn-primary btn-small">
                      Voir détails
                    </button>
                    <button @click="manageProposals(mission.id)" class="btn btn-secondary btn-small">
                      Propositions
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="content-section">
            <div class="section-header">
              <h3>👥 Freelances recommandés</h3>
              <router-link to="/profiles" class="see-all">Explorer</router-link>
            </div>
            <div class="freelancers-list">
              <div v-for="freelancer in recommendedFreelancers" :key="freelancer.id" class="freelancer-card">
                <div class="freelancer-avatar">
                  {{ freelancer.name.charAt(0) }}
                </div>
                <div class="freelancer-info">
                  <h4>{{ freelancer.name }}</h4>
                  <p class="freelancer-title">{{ freelancer.title }}</p>
                  <div class="freelancer-rating">
                    <span class="stars">⭐⭐⭐⭐⭐</span>
                    <span class="rating">4.8</span>
                  </div>
                  <p class="freelancer-skills">{{ freelancer.skills.join(', ') }}</p>
                </div>
                <button class="btn btn-primary btn-small">Contacter</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  
  <!-- Message de chargement si currentUser est null -->
  <div v-else class="loading-container">
    <div class="loading-spinner"></div>
    <p>Chargement de votre tableau de bord...</p>
  </div>
</template>

<script>
export default {
  name: 'DashboardViewClient',
  props: ['currentUser'],
  data() {
    return {
      stats: {
        // Freelance
        activeMissions: 3,
        proposalsSent: 12,
        averageRating: 4.8,
        estimatedEarnings: 2450,
        // Client
        publishedMissions: 8,
        proposalsReceived: 24,
        successRate: 95
      },
      latestOffers: [
        {
          id: 1,
          title: "Développement Application React Native",
          description: "Création d'une application mobile de gestion de tâches avec backend Node.js et base de données MongoDB.",
          budget: 3000,
          deadline: "15 décembre 2024",
          skills: ["React Native", "Node.js", "MongoDB", "API REST"]
        },
        {
          id: 2,
          title: "Design Site E-commerce Modern",
          description: "Refonte complète de l'interface utilisateur et expérience client pour une boutique en ligne.",
          budget: 1500,
          deadline: "10 décembre 2024",
          skills: ["UI/UX Design", "Figma", "Adobe XD", "Web Design"]
        },
        {
          id: 3,
          title: "API REST avec Python Flask",
          description: "Développement d'une API REST sécurisée avec authentification JWT et documentation Swagger.",
          budget: 2000,
          deadline: "20 décembre 2024",
          skills: ["Python", "Flask", "JWT", "Swagger", "PostgreSQL"]
        }
      ],
      recentMissions: [
        {
          id: 1,
          title: "Application Mobile de Réservation",
          client: "Restaurant Le Gourmet",
          progress: 75,
          status: "in-progress",
          deadline: "20 décembre 2024"
        },
        {
          id: 2,
          title: "Site Vitrine WordPress",
          client: "Cabinet Médical",
          progress: 100,
          status: "completed",
          deadline: "5 décembre 2024"
        }
      ],
      clientMissions: [
        {
          id: 1,
          title: "Refonte Site Corporate",
          proposalsCount: 8,
          budget: 5000,
          status: "review",
          deadline: "25 décembre 2024"
        },
        {
          id: 2,
          title: "Application de Gestion RH",
          proposalsCount: 12,
          budget: 8000,
          status: "in-progress",
          deadline: "15 janvier 2025"
        },
        {
          id: 3,
          title: "Site E-commerce Shopify",
          proposalsCount: 5,
          budget: 3500,
          status: "open",
          deadline: "30 décembre 2024"
        },
        {
          id: 4,
          title: "Application Mobile iOS",
          proposalsCount: 15,
          budget: 12000,
          status: "in-progress",
          deadline: "20 janvier 2025"
        },
        {
          id: 5,
          title: "Design UI/UX Dashboard",
          proposalsCount: 7,
          budget: 2500,
          status: "completed",
          deadline: "10 décembre 2024"
        },
        {
          id: 6,
          title: "API REST Backend",
          proposalsCount: 9,
          budget: 4000,
          status: "review",
          deadline: "5 janvier 2025"
        }
      ],
      showAllMissions: false,
      recommendedFreelancers: [
        {
          id: 1,
          name: "Marie Lambert",
          title: "Développeuse Full Stack",
          skills: ["React", "Node.js", "TypeScript", "AWS"],
          rating: 4.9
        },
        {
          id: 2,
          name: "Thomas Dubois",
          title: "UI/UX Designer Senior",
          skills: ["Figma", "Adobe Creative Suite", "Prototypage", "Research"],
          rating: 4.8
        }
      ]
    };
  },
  computed: {
    displayedMissions() {
      return this.showAllMissions ? this.clientMissions : this.clientMissions.slice(0, 2);
    }
  },
  mounted() {
    // Rediriger si pas d'utilisateur connecté
    if (!this.currentUser) {
      console.log('Aucun utilisateur connecté, redirection vers login...');
      this.$router.push('/login');
    }
  },
  watch: {
    currentUser(newVal) {
      if (!newVal) {
        this.$router.push('/login');
      }
    }
  },
  methods: {
    applyToMission(missionId) {
      console.log('Postulation à la mission:', missionId);
      alert(`Candidature envoyée pour la mission #${missionId}`);
    },
    viewMission(missionId) {
      console.log('Voir mission:', missionId);
      this.$router.push(`/missions/${missionId}`);
    },
    manageProposals(missionId) {
      console.log('Gérer propositions:', missionId);
    },
    toggleMissions() {
      this.showAllMissions = !this.showAllMissions;
    }
  }
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