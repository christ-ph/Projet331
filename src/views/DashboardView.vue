<template>
  <div class="dashboard" v-if="currentUser">
    <div class="dashboard-header">
      <div class="welcome-section">
        <h1>Tableau de bord</h1>
        <p class="welcome-message">Bon retour, <strong>{{ currentUser.email }}</strong> !</p>
        <p class="welcome-subtitle">
          Prêt à trouver votre prochaine mission ?
        </p>
      </div>
      <div class="header-actions">
        <router-link to="/missions" class="btn btn-secondary">
          📋 Voir les missions
        </router-link>
      </div>
    </div>

    <div class="dashboard-content">
      <div class="freelance-dashboard">
        <!-- Stats freelance -->
        <div class="stats-grid">
          <div class="stat-card primary">
            <div class="stat-icon">🚀</div>
            <div class="stat-content">
              <h3>Missions actives</h3>
              <p class="stat-number">{{ stats.activeMissions }}</p>
            </div>
          </div>
          
          <div class="stat-card success">
            <div class="stat-icon">💼</div>
            <div class="stat-content">
              <h3>Candidatures envoyées</h3>
              <p class="stat-number">{{ stats.proposalsSent }}</p>
            </div>
          </div>
          
          <div class="stat-card warning">
            <div class="stat-icon">⭐</div>
            <div class="stat-content">
              <h3>Note moyenne</h3>
              <p class="stat-number">{{ stats.averageRating }}/5</p>
            </div>
          </div>
          
          <div class="stat-card info">
            <div class="stat-icon">💰</div>
            <div class="stat-content">
              <h3>Revenus estimés</h3>
              <p class="stat-number">{{ stats.estimatedEarnings }}€</p>
            </div>
          </div>
        </div>

        <!-- Missions récentes -->
        <div class="content-section">
          <div class="section-header">
            <h3>📈 Mes missions récentes</h3>
            <router-link to="/missions" class="see-all">Voir toutes</router-link>
          </div>
          <div class="missions-list">
            <div v-for="mission in recentMissions" :key="mission.id" class="mission-card">
              <div class="mission-status" :class="mission.status"></div>
              <div class="mission-content">
                <h4>{{ mission.title }}</h4>
                <p class="mission-client">Client: {{ mission.client.name }}</p>
                <div class="mission-progress">
                  <div class="progress-bar">
                    <div :style="{ width: mission.progress + '%' }" class="progress-fill"></div>
                  </div>
                  <span class="progress-text">{{ mission.progress }}%</span>
                </div>
                <p class="mission-deadline">Échéance: {{ mission.deadline }}</p>
                <div class="mission-actions">
                  <button @click="viewMission(mission.id)" class="btn btn-primary btn-small">Voir détails</button>
                  <button @click="applyToMission(mission.id)" class="btn btn-secondary btn-small">Postuler</button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Offres récentes -->
        <div class="content-section">
          <div class="section-header">
            <h3>🎯 Offres récentes</h3>
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
                <button @click="viewMission(offer.id)" class="btn btn-secondary btn-small">Voir détails</button>
                <button @click="applyToMission(offer.id)" class="btn btn-primary btn-small">Postuler</button>
              </div>
            </div>
          </div>
        </div>

      </div>
    </div>
  </div>

  <div v-else class="loading-container">
    <p>Chargement...</p>
  </div>
</template>

<script>
import { getFreelanceMissions, getLatestOffers } from '@/services/api';

export default {
  name: 'DashboardViewFreelance',
  props: ['currentUser'],
  data() {
    return {
      stats: {
        activeMissions: 0,
        proposalsSent: 0,
        averageRating: 0,
        estimatedEarnings: 0
      },
      recentMissions: [],
      latestOffers: []
    };
  },
  async mounted() {
    if (!this.currentUser) {
      this.$router.push('/');
      return;
    }
    await this.loadDashboardData();
  },
  watch: {
    currentUser(newVal) {
      if (!newVal) this.$router.push('/');
    }
  },
  methods: {
    async loadDashboardData() {
      try {
        const missionsRes = await getFreelanceMissions(this.currentUser.id);
        this.recentMissions = missionsRes.data.missions_freelance || [];

        const offersRes = await getLatestOffers();
        this.latestOffers = offersRes.data.last_offers || [];

        // Calcul des stats
        this.stats.activeMissions = this.recentMissions.filter(m => m.status === 'IN_PROGRESS').length;
        this.stats.proposalsSent = this.recentMissions.length; // ou calcul selon API
        this.stats.averageRating = 4.7; // à remplacer par la valeur réelle depuis l'API
        this.stats.estimatedEarnings = 1500; // idem
      } catch (error) {
        console.error("Erreur lors du chargement du dashboard freelance :", error);
      }
    },
    viewMission(id) {
      this.$router.push(`/missions/${id}`);
    },
    applyToMission(id) {
      alert(`Candidature envoyée pour la mission #${id}`);
    }
  }
};
</script>


<style scoped>
.dashboard {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 3rem;
  padding-bottom: 2rem;
  border-bottom: 1px solid #e5e7eb;
}

.welcome-section h1 {
  font-size: 2.5rem;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 0.5rem;
}

.welcome-message {
  font-size: 1.125rem;
  color: #6b7280;
  margin-bottom: 0.5rem;
}

.welcome-subtitle {
  color: #9ca3af;
  font-size: 1rem;
}

.header-actions {
  display: flex;
  gap: 1rem;
}

/* Stats Grid */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 3rem;
}

.stat-card {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.08);
  display: flex;
  align-items: center;
  gap: 1rem;
  border-left: 4px solid;
  transition: transform 0.3s, box-shadow 0.3s;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0,0,0,0.12);
}

.stat-card.primary {
  border-left-color: #4f46e5;
}

.stat-card.success {
  border-left-color: #10b981;
}

.stat-card.warning {
  border-left-color: #f59e0b;
}

.stat-card.info {
  border-left-color: #06b6d4;
}

.stat-icon {
  font-size: 2rem;
  width: 60px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f8fafc;
  border-radius: 10px;
}

.stat-content h3 {
  font-size: 0.875rem;
  font-weight: 600;
  color: #6b7280;
  margin-bottom: 0.5rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.stat-number {
  font-size: 2rem;
  font-weight: 700;
  color: #1f2937;
  margin: 0;
  line-height: 1;
}

.stat-trend {
  font-size: 0.75rem;
  color: #9ca3af;
  margin: 0;
}

/* Content Grid */
.content-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
}

.content-section {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.08);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #f3f4f6;
}

.section-header h3 {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1f2937;
  margin: 0;
}

.see-all {
  color: #4f46e5;
  text-decoration: none;
  font-weight: 500;
  font-size: 0.875rem;
}

.see-all:hover {
  text-decoration: underline;
}

.badge {
  background: #e0e7ff;
  color: #4f46e5;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 600;
}

/* Offers List */
.offers-list,
.missions-list,
.freelancers-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.offer-card,
.mission-card,
.freelancer-card {
  border: 1px solid #f3f4f6;
  border-radius: 8px;
  padding: 1.25rem;
  transition: border-color 0.3s, box-shadow 0.3s;
}

.offer-card:hover,
.mission-card:hover,
.freelancer-card:hover {
  border-color: #e5e7eb;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

.offer-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 0.75rem;
}

.offer-header h4 {
  font-size: 1.125rem;
  font-weight: 600;
  color: #1f2937;
  margin: 0;
  flex: 1;
  margin-right: 1rem;
}

.budget {
  background: #10b981;
  color: white;
  padding: 0.375rem 0.75rem;
  border-radius: 20px;
  font-size: 0.875rem;
  font-weight: 600;
  white-space: nowrap;
}

.offer-description {
  color: #6b7280;
  font-size: 0.875rem;
  line-height: 1.5;
  margin-bottom: 1rem;
}

.offer-meta {
  display: flex;
  justify-content: space-between;
  font-size: 0.75rem;
  color: #9ca3af;
  margin-bottom: 1rem;
}

.offer-actions {
  display: flex;
  gap: 0.5rem;
}

.btn-small {
  padding: 0.5rem 1rem;
  font-size: 0.75rem;
}

/* Mission Cards */
.mission-card {
  display: flex;
  gap: 1rem;
}

.mission-status {
  width: 4px;
  border-radius: 2px;
  flex-shrink: 0;
}

.mission-status.in-progress {
  background: #f59e0b;
}

.mission-status.completed {
  background: #10b981;
}

.mission-status.review {
  background: #8b5cf6;
}

.mission-content {
  flex: 1;
}

.mission-content h4 {
  font-size: 1rem;
  font-weight: 600;
  color: #1f2937;
  margin: 0 0 0.5rem 0;
}

.mission-client,
.mission-meta,
.mission-deadline {
  font-size: 0.875rem;
  color: #6b7280;
  margin: 0.25rem 0;
}

.mission-progress {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin: 0.75rem 0;
}

.progress-bar {
  flex: 1;
  background: #f3f4f6;
  border-radius: 10px;
  height: 6px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: #10b981;
  border-radius: 10px;
  transition: width 0.3s;
}

.progress-text {
  font-size: 0.75rem;
  font-weight: 600;
  color: #374151;
  min-width: 40px;
}

/* Freelancer Cards */
.freelancer-card {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.freelancer-avatar {
  width: 50px;
  height: 50px;
  background: #4f46e5;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 1.125rem;
  flex-shrink: 0;
}

.freelancer-info {
  flex: 1;
}

.freelancer-info h4 {
  font-size: 1rem;
  font-weight: 600;
  color: #1f2937;
  margin: 0 0 0.25rem 0;
}

.freelancer-title {
  font-size: 0.875rem;
  color: #6b7280;
  margin: 0 0 0.5rem 0;
}

.freelancer-rating {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
}

.stars {
  font-size: 0.75rem;
}

.rating {
  font-size: 0.75rem;
  font-weight: 600;
  color: #f59e0b;
}

.freelancer-skills {
  font-size: 0.75rem;
  color: #9ca3af;
  margin: 0;
}

/* Responsive */
@media (max-width: 1024px) {
  .content-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .dashboard {
    padding: 1rem;
  }
  
  .dashboard-header {
    flex-direction: column;
    gap: 1rem;
  }
  
  .header-actions {
    width: 100%;
    justify-content: stretch;
  }
  
  .header-actions .btn {
    flex: 1;
    text-align: center;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .offer-header {
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .budget {
    align-self: flex-start;
  }
  
  .offer-actions {
    flex-direction: column;
  }
  
  .freelancer-card {
    flex-direction: column;
    text-align: center;
  }
}

@media (max-width: 480px) {
  .welcome-section h1 {
    font-size: 2rem;
  }
  
  .stat-card {
    flex-direction: column;
    text-align: center;
  }
  
  .mission-card {
    flex-direction: column;
  }
  
  .mission-status {
    width: 100%;
    height: 4px;
  }
}
</style>