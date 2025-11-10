<template>
  <div class="user-profile">
    <!-- Header du profil -->
    <div class="profile-header">
      <div class="header-content">
        <div class="avatar-section">
          <div class="avatar-large">
            {{ userInitials }}
          </div>
          <div class="user-info">
            <h1>{{ currentUser.email }}</h1>
            <div class="user-meta">
              <span class="role-badge" :class="currentUser.role.toLowerCase()">
                {{ getRoleLabel(currentUser.role) }}
              </span>
              <span class="member-since">Membre depuis décembre 2024</span>
            </div>
          </div>
        </div>
        
        <div class="header-stats">
          <div class="stat-item">
            <div class="stat-number">{{ userStats.completedProjects }}</div>
            <div class="stat-label">Projets terminés</div>
          </div>
          <div class="stat-item">
            <div class="stat-number">{{ userStats.responseRate }}%</div>
            <div class="stat-label">Taux de réponse</div>
          </div>
          <div class="stat-item">
            <div class="stat-number">{{ userStats.avgResponseTime }}h</div>
            <div class="stat-label">Réponse moyenne</div>
          </div>
        </div>
      </div>
    </div>

    <div class="profile-content">
      <!-- Navigation par onglets -->
      <div class="profile-tabs">
        <button 
          v-for="tab in tabs" 
          :key="tab.id"
          :class="['tab-button', { active: activeTab === tab.id }]"
          @click="activeTab = tab.id"
        >
          {{ tab.label }}
        </button>
      </div>

      <!-- Contenu des onglets -->
      <div class="tab-content">
        <!-- Onglet Aperçu -->
        <div v-if="activeTab === 'overview'" class="overview-tab">
          <div class="overview-grid">
            <!-- Statistiques principales -->
            <div class="stats-section">
              <h3>📊 Statistiques de performance</h3>
              <div class="performance-stats">
                <div class="performance-card success">
                  <div class="performance-icon">✅</div>
                  <div class="performance-content">
                    <div class="performance-value">{{ performanceStats.successRate }}%</div>
                    <div class="performance-label">Taux de réussite</div>
                  </div>
                </div>
                <div class="performance-card warning">
                  <div class="performance-icon">⏱️</div>
                  <div class="performance-content">
                    <div class="performance-value">{{ performanceStats.avgCompletionTime }}j</div>
                    <div class="performance-label">Délai moyen</div>
                  </div>
                </div>
                <div class="performance-card info">
                  <div class="performance-icon">💬</div>
                  <div class="performance-content">
                    <div class="performance-value">{{ performanceStats.clientSatisfaction }}%</div>
                    <div class="performance-label">Satisfaction client</div>
                  </div>
                </div>
                <div class="performance-card primary">
                  <div class="performance-icon">🔄</div>
                  <div class="performance-content">
                    <div class="performance-value">{{ performanceStats.repeatClients }}</div>
                    <div class="performance-label">Clients fidèles</div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Badges et réalisations -->
            <div class="badges-section">
              <h3>🏆 Badges et réalisations</h3>
              <div class="badges-grid">
                <div class="badge-card verified" v-if="isVerified">
                  <div class="badge-icon">✅</div>
                  <div class="badge-content">
                    <h4>Profil Vérifié</h4>
                    <p>Identité et compétences confirmées</p>
                  </div>
                </div>
                <div class="badge-card top-rated">
                  <div class="badge-icon">⭐</div>
                  <div class="badge-content">
                    <h4>Top Rated</h4>
                    <p>Parmi les meilleurs freelances</p>
                  </div>
                </div>
                <div class="badge-card fast-delivery">
                  <div class="badge-icon">⚡</div>
                  <div class="badge-content">
                    <h4>Livraison Rapide</h4>
                    <p>Délais respectés à 95%</p>
                  </div>
                </div>
                <div class="badge-card communicator">
                  <div class="badge-icon">💬</div>
                  <div class="badge-content">
                    <h4>Excellent Communicant</h4>
                    <p>Très réactif aux messages</p>
                  </div>
                </div>
              </div>
            </div>

            <!-- Dernières activités -->
            <div class="activity-section">
              <h3>📈 Activité récente</h3>
              <div class="activity-timeline">
                <div v-for="activity in recentActivities" :key="activity.id" class="activity-item">
                  <div class="activity-icon" :class="activity.type">
                    {{ getActivityIcon(activity.type) }}
                  </div>
                  <div class="activity-content">
                    <p class="activity-text">{{ activity.description }}</p>
                    <span class="activity-time">{{ activity.time }}</span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Recommandations -->
            <div class="recommendations-section">
              <h3>💡 Recommandations</h3>
              <div class="recommendations-list">
                <div class="recommendation-card">
                  <div class="recommendation-icon">📈</div>
                  <div class="recommendation-content">
                    <h4>Améliorez votre profil</h4>
                    <p>Ajoutez plus de projets à votre portfolio pour augmenter vos chances de 40%</p>
                    <button class="btn btn-primary btn-small">
                      Compléter le profil
                    </button>
                  </div>
                </div>
                <div class="recommendation-card">
                  <div class="recommendation-icon">🎯</div>
                  <div class="recommendation-content">
                    <h4>Compétences demandées</h4>
                    <p>Les clients recherchent activement des experts en React et Node.js</p>
                    <button class="btn btn-secondary btn-small">
                      Voir les missions
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Onglet Évaluations -->
        <div v-if="activeTab === 'reviews'" class="reviews-tab">
          <div class="reviews-header">
            <div class="rating-overview">
              <div class="average-rating">
                <div class="rating-stars">⭐⭐⭐⭐⭐</div>
                <div class="rating-value">{{ averageRating }}/5</div>
                <div class="rating-count">{{ reviews.length }} avis</div>
              </div>
              <div class="rating-breakdown">
                <div v-for="n in 5" :key="n" class="rating-bar">
                  <span class="star-count">{{ 6 - n }} ⭐</span>
                  <div class="bar-container">
                    <div 
                      class="bar-fill" 
                      :style="{ width: getRatingPercentage(6 - n) + '%' }"
                    ></div>
                  </div>
                  <span class="percentage">{{ getRatingPercentage(6 - n) }}%</span>
                </div>
              </div>
            </div>
          </div>

          <div class="reviews-list">
            <div v-for="review in reviews" :key="review.id" class="review-card">
              <div class="review-header">
                <div class="reviewer-info">
                  <div class="reviewer-avatar">
                    {{ review.reviewerName.charAt(0) }}
                  </div>
                  <div class="reviewer-details">
                    <h4>{{ review.reviewerName }}</h4>
                    <div class="review-meta">
                      <span class="review-date">{{ review.date }}</span>
                      <span class="project-name">{{ review.project }}</span>
                    </div>
                  </div>
                </div>
                <div class="review-rating">
                  <span class="stars">
                    <span v-for="n in 5" :key="n" :class="{ filled: n <= review.rating }">
                      ⭐
                    </span>
                  </span>
                  <span class="rating-value">{{ review.rating }}/5</span>
                </div>
              </div>
              <p class="review-comment">{{ review.comment }}</p>
              <div class="review-skills" v-if="review.skills.length > 0">
                <span 
                  v-for="skill in review.skills" 
                  :key="skill" 
                  class="skill-tag"
                >
                  {{ skill }}
                </span>
              </div>
            </div>
          </div>
        </div>

        <!-- Onglet Portfolio (pour les freelances) -->
        <div v-if="activeTab === 'portfolio' && currentUser.role === 'FREELANCE'" class="portfolio-tab">
          <div class="portfolio-header">
            <h3>Mes projets</h3>
            <button class="btn btn-primary" @click="addProject">
              + Ajouter un projet
            </button>
          </div>
          
          <div class="portfolio-grid">
            <div v-for="project in portfolioProjects" :key="project.id" class="project-card">
              <div class="project-image">
                <div class="image-placeholder">
                  {{ project.title.charAt(0) }}
                </div>
              </div>
              <div class="project-content">
                <h4>{{ project.title }}</h4>
                <p class="project-description">{{ project.description }}</p>
                <div class="project-skills">
                  <span 
                    v-for="skill in project.skills" 
                    :key="skill" 
                    class="skill-tag"
                  >
                    {{ skill }}
                  </span>
                </div>
                <div class="project-meta">
                  <span class="project-date">{{ project.date }}</span>
                  <span class="project-budget">{{ project.budget }}€</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Onglet Paramètres -->
        <div v-if="activeTab === 'settings'" class="settings-tab">
          <div class="settings-section">
            <h3>Paramètres du compte</h3>
            <div class="settings-form">
              <div class="form-group">
                <label>Email</label>
                <input :value="currentUser.email" type="email" disabled />
                <small>L'email ne peut pas être modifié</small>
              </div>
              
              <div class="form-group">
                <label>Notifications</label>
                <div class="checkbox-group">
                  <label class="checkbox-label">
                    <input type="checkbox" v-model="settings.emailNotifications" />
                    <span class="checkmark"></span>
                    Notifications par email
                  </label>
                  <label class="checkbox-label">
                    <input type="checkbox" v-model="settings.projectAlerts" />
                    <span class="checkmark"></span>
                    Alertes de nouveaux projets
                  </label>
                  <label class="checkbox-label">
                    <input type="checkbox" v-model="settings.messageNotifications" />
                    <span class="checkmark"></span>
                    Notifications de messages
                  </label>
                </div>
              </div>

              <div class="form-group">
                <label>Visibilité du profil</label>
                <select v-model="settings.profileVisibility">
                  <option value="public">Public</option>
                  <option value="private">Privé</option>
                  <option value="limited">Limité</option>
                </select>
              </div>

              <button class="btn btn-primary" @click="saveSettings">
                Sauvegarder les paramètres
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'UserProfileView',
  props: ['currentUser'],
  data() {
    return {
      activeTab: 'overview',
      tabs: [
        { id: 'overview', label: '📊 Aperçu' },
        { id: 'reviews', label: '⭐ Évaluations' },
        { id: 'portfolio', label: '📁 Portfolio' },
        { id: 'settings', label: '⚙️ Paramètres' }
      ],
      isVerified: true,
      userStats: {
        completedProjects: 24,
        responseRate: 95,
        avgResponseTime: 2
      },
      performanceStats: {
        successRate: 98,
        avgCompletionTime: 14,
        clientSatisfaction: 96,
        repeatClients: 8
      },
      recentActivities: [
        {
          id: 1,
          type: 'application',
          description: 'Vous avez postulé à la mission "Développement Application React"',
          time: 'Il y a 2 heures'
        },
        {
          id: 2,
          type: 'message',
          description: 'Nouveau message de Sarah Martin',
          time: 'Il y a 1 jour'
        },
        {
          id: 3,
          type: 'review',
          description: 'Nouvel avis reçu pour le projet "Site E-commerce"',
          time: 'Il y a 2 jours'
        },
        {
          id: 4,
          type: 'completion',
          description: 'Projet "Application Mobile" marqué comme terminé',
          time: 'Il y a 3 jours'
        }
      ],
      reviews: [
        {
          id: 1,
          reviewerName: 'Sarah Martin',
          rating: 5,
          date: '15 novembre 2024',
          project: 'Application de Réservation',
          comment: 'Excellent travail ! Marie a su comprendre nos besoins rapidement et a livré un produit de qualité supérieure. Très professionnelle et réactive. Je recommande vivement !',
          skills: ['React Native', 'Node.js', 'Communication']
        },
        {
          id: 2,
          reviewerName: 'Pierre Dubois',
          rating: 4,
          date: '10 novembre 2024',
          project: 'Site Vitrine WordPress',
          comment: 'Très bon développeur, compétent et sérieux. Quelques retards mineurs mais la qualité du travail est au rendez-vous.',
          skills: ['WordPress', 'PHP', 'Design']
        }
      ],
      portfolioProjects: [
        {
          id: 1,
          title: 'Application Mobile de Livraison',
          description: 'Développement d\'une application React Native complète avec système de géolocalisation en temps réel.',
          skills: ['React Native', 'Node.js', 'MongoDB', 'Google Maps API'],
          date: 'Nov 2024',
          budget: 3500
        },
        {
          id: 2,
          title: 'Plateforme E-learning',
          description: 'Création d\'une plateforme de cours en ligne avec système de paiement et vidéos streaming.',
          skills: ['Vue.js', 'Laravel', 'MySQL', 'Stripe API'],
          date: 'Oct 2024',
          budget: 5000
        }
      ],
      settings: {
        emailNotifications: true,
        projectAlerts: true,
        messageNotifications: true,
        profileVisibility: 'public'
      }
    };
  },
  computed: {
    userInitials() {
      const email = this.currentUser.email || '';
      return email.charAt(0).toUpperCase();
    },
    averageRating() {
      if (this.reviews.length === 0) return 0;
      const sum = this.reviews.reduce((acc, review) => acc + review.rating, 0);
      return (sum / this.reviews.length).toFixed(1);
    }
  },
  methods: {
    getRoleLabel(role) {
      const labels = {
        FREELANCE: 'Freelance',
        CLIENT: 'Client',
        ADMIN: 'Administrateur'
      };
      return labels[role] || role;
    },
    getActivityIcon(type) {
      const icons = {
        application: '📨',
        message: '💬',
        review: '⭐',
        completion: '✅'
      };
      return icons[type] || '🔔';
    },
    getRatingPercentage(rating) {
      const count = this.reviews.filter(r => r.rating === rating).length;
      return Math.round((count / this.reviews.length) * 100) || 0;
    },
    addProject() {
      console.log('Ajouter un nouveau projet');
      // Implémenter la logique d'ajout de projet
    },
    saveSettings() {
      console.log('Sauvegarde des paramètres:', this.settings);
      alert('Paramètres sauvegardés avec succès !');
    }
  }
};
</script>

<style scoped>
.user-profile {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.profile-header {
  background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
  color: white;
  padding: 3rem 2rem;
  border-radius: 16px;
  margin-bottom: 2rem;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 2rem;
}

.avatar-section {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.avatar-large {
  width: 100px;
  height: 100px;
  background: rgba(255, 255, 255, 0.2);
  border: 4px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2.5rem;
  font-weight: 700;
}

.user-info h1 {
  font-size: 2.5rem;
  font-weight: 700;
  margin: 0 0 0.5rem 0;
}

.user-meta {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex-wrap: wrap;
}

.role-badge {
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-weight: 600;
  font-size: 0.875rem;
}

.role-badge.freelance {
  background: rgba(34, 197, 94, 0.2);
  border: 1px solid rgba(34, 197, 94, 0.5);
}

.role-badge.client {
  background: rgba(59, 130, 246, 0.2);
  border: 1px solid rgba(59, 130, 246, 0.5);
}

.role-badge.admin {
  background: rgba(239, 68, 68, 0.2);
  border: 1px solid rgba(239, 68, 68, 0.5);
}

.member-since {
  opacity: 0.8;
  font-size: 0.875rem;
}

.header-stats {
  display: flex;
  gap: 2rem;
}

.stat-item {
  text-align: center;
}

.stat-number {
  font-size: 2rem;
  font-weight: 700;
  display: block;
  line-height: 1;
}

.stat-label {
  font-size: 0.875rem;
  opacity: 0.8;
  margin-top: 0.5rem;
}

.profile-tabs {
  display: flex;
  background: white;
  border-radius: 12px;
  padding: 0.5rem;
  margin-bottom: 2rem;
  box-shadow: 0 2px 10px rgba(0,0,0,0.08);
  border: 1px solid #f3f4f6;
}

.tab-button {
  flex: 1;
  padding: 1rem 1.5rem;
  border: none;
  background: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.3s;
  text-align: center;
}

.tab-button.active {
  background: #4f46e5;
  color: white;
}

.tab-button:hover:not(.active) {
  background: #f8fafc;
}

.tab-content {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 2px 10px rgba(0,0,0,0.08);
  border: 1px solid #f3f4f6;
}

/* Styles pour l'onglet Aperçu */
.overview-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 2rem;
}

.stats-section h3,
.badges-section h3,
.activity-section h3,
.recommendations-section h3 {
  font-size: 1.5rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 1.5rem;
}

.performance-stats {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.performance-card {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1.5rem;
  border-radius: 12px;
  border-left: 4px solid;
}

.performance-card.success {
  background: #f0fdf4;
  border-left-color: #10b981;
}

.performance-card.warning {
  background: #fffbeb;
  border-left-color: #f59e0b;
}

.performance-card.info {
  background: #f0f9ff;
  border-left-color: #0ea5e9;
}

.performance-card.primary {
  background: #eef2ff;
  border-left-color: #4f46e5;
}

.performance-icon {
  font-size: 2rem;
}

.performance-value {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1f2937;
  line-height: 1;
}

.performance-label {
  color: #6b7280;
  font-size: 0.875rem;
  margin-top: 0.25rem;
}

.badges-grid {
  display: grid;
  gap: 1rem;
}

.badge-card {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1.5rem;
  border-radius: 12px;
  border: 1px solid;
}

.badge-card.verified {
  background: #f0fdf4;
  border-color: #10b981;
}

.badge-card.top-rated {
  background: #fffbeb;
  border-color: #f59e0b;
}

.badge-card.fast-delivery {
  background: #fef3c7;
  border-color: #d97706;
}

.badge-card.communicator {
  background: #e0e7ff;
  border-color: #4f46e5;
}

.badge-icon {
  font-size: 2rem;
}

.badge-content h4 {
  margin: 0 0 0.25rem 0;
  color: #1f2937;
  font-size: 1.125rem;
}

.badge-content p {
  margin: 0;
  color: #6b7280;
  font-size: 0.875rem;
}

.activity-timeline {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.activity-item {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  padding: 1rem;
  border-radius: 8px;
  transition: background 0.3s;
}

.activity-item:hover {
  background: #f8fafc;
}

.activity-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.125rem;
  flex-shrink: 0;
}

.activity-icon.application { background: #dbeafe; }
.activity-icon.message { background: #e0e7ff; }
.activity-icon.review { background: #fef3c7; }
.activity-icon.completion { background: #d1fae5; }

.activity-text {
  margin: 0 0 0.25rem 0;
  color: #374151;
  font-weight: 500;
}

.activity-time {
  color: #9ca3af;
  font-size: 0.875rem;
}

.recommendations-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.recommendation-card {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  padding: 1.5rem;
  background: #f8fafc;
  border-radius: 12px;
  border-left: 4px solid #4f46e5;
}

.recommendation-icon {
  font-size: 1.5rem;
  flex-shrink: 0;
}

.recommendation-content h4 {
  margin: 0 0 0.5rem 0;
  color: #1f2937;
}

.recommendation-content p {
  margin: 0 0 1rem 0;
  color: #6b7280;
  font-size: 0.875rem;
}

/* Styles pour l'onglet Évaluations */
.reviews-header {
  margin-bottom: 2rem;
  padding-bottom: 2rem;
  border-bottom: 1px solid #e5e7eb;
}

.rating-overview {
  display: flex;
  gap: 3rem;
  align-items: center;
  flex-wrap: wrap;
}

.average-rating {
  text-align: center;
}

.rating-stars {
  font-size: 2rem;
  margin-bottom: 0.5rem;
}

.rating-value {
  font-size: 3rem;
  font-weight: 700;
  color: #1f2937;
  line-height: 1;
  margin-bottom: 0.5rem;
}

.rating-count {
  color: #6b7280;
}

.rating-breakdown {
  flex: 1;
  min-width: 300px;
}

.rating-bar {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 0.5rem;
}

.star-count {
  width: 60px;
  font-size: 0.875rem;
  color: #6b7280;
}

.bar-container {
  flex: 1;
  background: #f3f4f6;
  height: 8px;
  border-radius: 4px;
  overflow: hidden;
}

.bar-fill {
  height: 100%;
  background: #f59e0b;
  border-radius: 4px;
  transition: width 0.3s;
}

.percentage {
  width: 40px;
  text-align: right;
  font-size: 0.875rem;
  color: #6b7280;
}

.reviews-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.review-card {
  padding: 1.5rem;
  border: 1px solid #f3f4f6;
  border-radius: 12px;
  transition: border-color 0.3s;
}

.review-card:hover {
  border-color: #e5e7eb;
}

.review-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
  gap: 1rem;
}

.reviewer-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.reviewer-avatar {
  width: 50px;
  height: 50px;
  background: #4f46e5;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  flex-shrink: 0;
}

.reviewer-details h4 {
  margin: 0 0 0.25rem 0;
  color: #1f2937;
}

.review-meta {
  display: flex;
  gap: 1rem;
  font-size: 0.875rem;
  color: #6b7280;
}

.review-rating {
  text-align: right;
  flex-shrink: 0;
}

.review-rating .stars {
  display: block;
  margin-bottom: 0.25rem;
}

.review-rating .rating-value {
  font-size: 1rem;
  color: #f59e0b;
  font-weight: 600;
}

.review-comment {
  color: #374151;
  line-height: 1.6;
  margin-bottom: 1rem;
}

.review-skills {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.skill-tag {
  background: #e0e7ff;
  color: #4f46e5;
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 500;
}

/* Styles pour l'onglet Portfolio */
.portfolio-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.portfolio-header h3 {
  margin: 0;
  color: #1f2937;
}

.portfolio-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

.project-card {
  border: 1px solid #f3f4f6;
  border-radius: 12px;
  overflow: hidden;
  transition: transform 0.3s, box-shadow 0.3s;
}

.project-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0,0,0,0.1);
}

.project-image {
  height: 120px;
  background: linear-gradient(135deg, #4f46e5, #7c3aed);
  display: flex;
  align-items: center;
  justify-content: center;
}

.image-placeholder {
  color: white;
  font-size: 3rem;
  font-weight: 700;
}

.project-content {
  padding: 1.5rem;
}

.project-content h4 {
  margin: 0 0 0.75rem 0;
  color: #1f2937;
  font-size: 1.125rem;
}

.project-description {
  color: #6b7280;
  font-size: 0.875rem;
  line-height: 1.5;
  margin-bottom: 1rem;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.project-skills {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.project-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.875rem;
  color: #9ca3af;
}

.project-budget {
  font-weight: 600;
  color: #10b981;
}

/* Styles pour l'onglet Paramètres */
.settings-section h3 {
  font-size: 1.5rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 1.5rem;
}

.settings-form {
  max-width: 500px;
}

.settings-form .form-group {
  margin-bottom: 1.5rem;
}

.settings-form label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: #374151;
}

.settings-form input,
.settings-form select {
  width: 100%;
  padding: 0.875rem;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.3s;
}

.settings-form input:focus,
.settings-form select:focus {
  outline: none;
  border-color: #4f46e5;
}

.settings-form input:disabled {
  background: #f9fafb;
  color: #6b7280;
}

.settings-form small {
  display: block;
  margin-top: 0.5rem;
  color: #6b7280;
  font-size: 0.75rem;
}

.checkbox-group {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  cursor: pointer;
  font-weight: 500;
}

.checkbox-label input {
  width: auto;
}

/* Responsive */
@media (max-width: 1024px) {
  .overview-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .user-profile {
    padding: 1rem;
  }
  
  .profile-header {
    padding: 2rem 1rem;
  }
  
  .header-content {
    flex-direction: column;
    text-align: center;
  }
  
  .avatar-section {
    flex-direction: column;
    text-align: center;
  }
  
  .header-stats {
    justify-content: center;
  }
  
  .profile-tabs {
    flex-direction: column;
  }
  
  .rating-overview {
    flex-direction: column;
    text-align: center;
  }
  
  .review-header {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .review-rating {
    text-align: left;
  }
  
  .portfolio-header {
    flex-direction: column;
    gap: 1rem;
    align-items: flex-start;
  }
}

@media (max-width: 480px) {
  .user-info h1 {
    font-size: 2rem;
  }
  
  .performance-stats {
    grid-template-columns: 1fr;
  }
  
  .header-stats {
    flex-direction: column;
    gap: 1rem;
  }
  
  .portfolio-grid {
    grid-template-columns: 1fr;
  }
}
</style>