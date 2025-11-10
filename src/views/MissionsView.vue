<template>
  <div class="missions-page">
    <!-- Header avec recherche et filtres -->
    <div class="missions-header">
      <div class="header-main">
        <h1>🎯 Missions Disponibles</h1>
        <p>Trouvez la mission parfaite qui correspond à vos compétences</p>
      </div>
      
      <div class="header-actions">
        <div class="search-box">
          <input 
            v-model="searchQuery" 
            placeholder="Rechercher une mission, une compétence..." 
            type="text"
            class="search-input"
          />
          <span class="search-icon">🔍</span>
        </div>
        
        <div class="filter-buttons">
          <button 
            v-for="filter in quickFilters" 
            :key="filter.id"
            :class="['filter-btn', { active: activeQuickFilter === filter.id }]"
            @click="toggleQuickFilter(filter.id)"
          >
            {{ filter.label }}
          </button>
        </div>
      </div>
    </div>

    <!-- Contenu principal -->
    <div class="missions-content">
      <!-- Sidebar des filtres -->
      <div class="filters-sidebar">
        <div class="filter-section">
          <h3>Filtres</h3>
          
          <div class="filter-group">
            <label>Budget</label>
            <div class="budget-range">
              <input 
                v-model.number="filters.minBudget" 
                type="number" 
                placeholder="Min" 
                class="budget-input"
              />
              <span>-</span>
              <input 
                v-model.number="filters.maxBudget" 
                type="number" 
                placeholder="Max" 
                class="budget-input"
              />
            </div>
          </div>

          <div class="filter-group">
            <label>Compétences</label>
            <div class="skills-filter">
              <input 
                v-model="skillFilter" 
                placeholder="Filtrer par compétence..." 
                class="skill-input"
              />
              <div class="skills-list">
                <label 
                  v-for="skill in filteredSkills" 
                  :key="skill"
                  class="skill-checkbox"
                >
                  <input 
                    type="checkbox" 
                    :value="skill" 
                    v-model="filters.skills"
                  />
                  <span class="checkmark"></span>
                  {{ skill }}
                </label>
              </div>
            </div>
          </div>

          <div class="filter-group">
            <label>Type de mission</label>
            <div class="type-filters">
              <label class="type-checkbox">
                <input type="checkbox" value="FULL_TIME" v-model="filters.types">
                <span class="checkmark"></span>
                Temps plein
              </label>
              <label class="type-checkbox">
                <input type="checkbox" value="PART_TIME" v-model="filters.types">
                <span class="checkmark"></span>
                Temps partiel
              </label>
              <label class="type-checkbox">
                <input type="checkbox" value="FREELANCE" v-model="filters.types">
                <span class="checkmark"></span>
                Freelance
              </label>
            </div>
          </div>

          <button @click="resetFilters" class="btn-reset-filters">
            🔄 Réinitialiser
          </button>
        </div>

        <!-- Statistiques -->
        <div class="stats-sidebar">
          <h4>Votre activité</h4>
          <div class="stat-item">
            <span class="stat-number">{{ userStats.applicationsSent }}</span>
            <span class="stat-label">Candidatures envoyées</span>
          </div>
          <div class="stat-item">
            <span class="stat-number">{{ userStats.interviews }}</span>
            <span class="stat-label">Entretiens</span>
          </div>
          <div class="stat-item">
            <span class="stat-number">{{ userStats.successRate }}%</span>
            <span class="stat-label">Taux de réussite</span>
          </div>
        </div>
      </div>

      <!-- Liste des missions -->
      <div class="missions-list">
        <div class="list-header">
          <h2>{{ filteredMissions.length }} missions trouvées</h2>
          <div class="sort-options">
            <label>Trier par:</label>
            <select v-model="sortBy" class="sort-select">
              <option value="newest">Plus récentes</option>
              <option value="budget_high">Budget (élevé)</option>
              <option value="budget_low">Budget (faible)</option>
              <option value="deadline">Échéance proche</option>
            </select>
          </div>
        </div>

        <!-- Missions -->
        <div class="missions-grid">
          <div 
            v-for="mission in sortedMissions" 
            :key="mission.id" 
            class="mission-card"
            :class="{ featured: mission.featured }"
          >
            <div class="mission-badge" v-if="mission.featured">
              ⭐ Mission recommandée
            </div>
            
            <div class="mission-header">
              <div class="mission-title-section">
                <h3>{{ mission.title }}</h3>
                <div class="mission-meta">
                  <span class="mission-type" :class="mission.type">
                    {{ getTypeLabel(mission.type) }}
                  </span>
                  <span class="mission-duration">📅 {{ mission.duration }}</span>
                </div>
              </div>
              <div class="mission-budget">
                <span class="budget-amount">{{ mission.budget }}€</span>
                <span class="budget-type">{{ mission.budgetType }}</span>
              </div>
            </div>

            <p class="mission-description">{{ mission.description }}</p>

            <div class="mission-skills">
              <span 
                v-for="skill in mission.skills.slice(0, 4)" 
                :key="skill" 
                class="skill-tag"
              >
                {{ skill }}
              </span>
              <span v-if="mission.skills.length > 4" class="more-skills">
                +{{ mission.skills.length - 4 }}
              </span>
            </div>

            <div class="mission-footer">
              <div class="mission-client">
                <div class="client-avatar">
                  {{ mission.client.name.charAt(0) }}
                </div>
                <div class="client-info">
                  <span class="client-name">{{ mission.client.name }}</span>
                  <span class="client-rating">
                    ⭐ {{ mission.client.rating }} ({{ mission.client.reviews }} avis)
                  </span>
                </div>
              </div>
              
              <div class="mission-actions">
                <button 
                  @click="viewMission(mission.id)" 
                  class="btn btn-secondary btn-small"
                >
                  👀 Voir
                </button>
                <button 
                  @click="applyToMission(mission)" 
                  class="btn btn-primary btn-small"
                  :disabled="mission.hasApplied"
                >
                  {{ mission.hasApplied ? '✅ Postulé' : '📨 Postuler' }}
                </button>
              </div>
            </div>

            <div class="mission-timeline">
              <span class="post-date">📅 Publiée {{ mission.postedDate }}</span>
              <span class="deadline">⏱️ Échéance: {{ mission.deadline }}</span>
              <span class="proposals">📨 {{ mission.proposalsCount }} propositions</span>
            </div>
          </div>
        </div>

        <!-- Pagination -->
        <div class="pagination" v-if="totalPages > 1">
          <button 
            @click="prevPage" 
            :disabled="currentPage === 1" 
            class="pagination-btn"
          >
            ‹ Précédent
          </button>
          
          <div class="page-numbers">
            <button 
              v-for="page in visiblePages" 
              :key="page"
              :class="['page-btn', { active: page === currentPage }]"
              @click="goToPage(page)"
            >
              {{ page }}
            </button>
          </div>
          
          <button 
            @click="nextPage" 
            :disabled="currentPage === totalPages" 
            class="pagination-btn"
          >
            Suivant ›
          </button>
        </div>

        <!-- État vide -->
        <div v-if="filteredMissions.length === 0" class="empty-state">
          <div class="empty-icon">🔍</div>
          <h3>Aucune mission trouvée</h3>
          <p>Essayez de modifier vos filtres ou votre recherche</p>
          <button @click="resetFilters" class="btn btn-primary">
            Réinitialiser les filtres
          </button>
        </div>
      </div>
    </div>

    <!-- Modal de candidature -->
    <div v-if="showApplicationModal" class="modal-overlay">
      <div class="modal-content">
        <div class="modal-header">
          <h3>Postuler à la mission</h3>
          <button @click="closeModal" class="btn-close">×</button>
        </div>
        
        <div class="modal-body">
          <div class="mission-preview" v-if="selectedMission">
            <h4>{{ selectedMission.title }}</h4>
            <p class="budget">Budget: {{ selectedMission.budget }}€</p>
          </div>
          
          <form @submit.prevent="submitApplication">
            <div class="form-group">
              <label>Votre proposition *</label>
              <textarea 
                v-model="application.proposal" 
                placeholder="Présentez-vous et expliquez pourquoi vous êtes le bon candidat pour cette mission..."
                rows="6"
                required
              ></textarea>
            </div>
            
            <div class="form-group">
              <label>Votre tarif proposé (€) *</label>
              <input 
                v-model.number="application.proposedBudget" 
                type="number" 
                :placeholder="selectedMission?.budget"
                required
              />
            </div>
            
            <div class="form-group">
              <label>Délai de livraison *</label>
              <input 
                v-model="application.deliveryTime" 
                placeholder="Ex: 2 semaines, 1 mois..." 
                required
              />
            </div>
            
            <div class="form-actions">
              <button type="button" @click="closeModal" class="btn btn-secondary">
                Annuler
              </button>
              <button type="submit" class="btn btn-primary" :disabled="!isApplicationValid">
                📨 Envoyer la candidature
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'MissionsView',
  props: ['currentUser'],
  data() {
    return {
      searchQuery: '',
      activeQuickFilter: null,
      sortBy: 'newest',
      currentPage: 1,
      itemsPerPage: 6,
      
      filters: {
        minBudget: null,
        maxBudget: null,
        skills: [],
        types: []
      },
      
      skillFilter: '',
      showApplicationModal: false,
      selectedMission: null,
      
      application: {
        proposal: '',
        proposedBudget: null,
        deliveryTime: ''
      },
      
      quickFilters: [
        { id: 'urgent', label: '🔴 Urgent' },
        { id: 'featured', label: '⭐ Recommandé' },
        { id: 'budget_high', label: '💰 Budget élevé' },
        { id: 'new', label: '🆕 Nouveau' }
      ],
      
      allSkills: [
        'React', 'Vue.js', 'Node.js', 'Python', 'JavaScript', 'TypeScript',
        'UI/UX Design', 'Figma', 'Adobe XD', 'PHP', 'Laravel', 'Symfony',
        'WordPress', 'MongoDB', 'PostgreSQL', 'AWS', 'Docker', 'React Native',
        'Flutter', 'Swift', 'Kotlin', 'Java', 'C#', '.NET'
      ],
      
      missions: [
        {
          id: 1,
          title: "Développement Application React Native",
          description: "Création d'une application mobile de gestion de tâches avec backend Node.js et base de données MongoDB. L'application doit inclure une authentification utilisateur, un système de notifications push et une interface responsive.",
          budget: 3000,
          budgetType: "Forfait",
          type: "FREELANCE",
          duration: "3-4 semaines",
          skills: ["React Native", "Node.js", "MongoDB", "API REST", "JavaScript"],
          client: {
            name: "TechStart Inc.",
            rating: 4.8,
            reviews: 24
          },
          postedDate: "il y a 2 jours",
          deadline: "15 décembre 2024",
          proposalsCount: 8,
          featured: true,
          hasApplied: false
        },
        {
          id: 2,
          title: "Design Site E-commerce Modern",
          description: "Refonte complète de l'interface utilisateur et expérience client pour une boutique en ligne. Création d'un design system cohérent et responsive.",
          budget: 1500,
          budgetType: "Forfait",
          type: "FREELANCE",
          duration: "2 semaines",
          skills: ["UI/UX Design", "Figma", "Adobe XD", "Web Design", "Responsive"],
          client: {
            name: "FashionStore",
            rating: 4.5,
            reviews: 12
          },
          postedDate: "il y a 5 jours",
          deadline: "10 décembre 2024",
          proposalsCount: 15,
          featured: false,
          hasApplied: true
        },
        {
          id: 3,
          title: "API REST avec Python Flask",
          description: "Développement d'une API REST sécurisée avec authentification JWT, documentation Swagger et tests unitaires. Intégration avec base de données PostgreSQL.",
          budget: 45,
          budgetType: "Heure",
          type: "PART_TIME",
          duration: "1 mois",
          skills: ["Python", "Flask", "JWT", "Swagger", "PostgreSQL", "Docker"],
          client: {
            name: "DataCorp",
            rating: 4.9,
            reviews: 36
          },
          postedDate: "il y a 1 jour",
          deadline: "20 décembre 2024",
          proposalsCount: 5,
          featured: true,
          hasApplied: false
        },
        {
          id: 4,
          title: "Application de Gestion de Projet",
          description: "Développement d'une application web de gestion de projet avec Vue.js et Laravel. Fonctionnalités : tableaux Kanban, gestion des tâches, time tracking.",
          budget: 5000,
          budgetType: "Forfait",
          type: "FULL_TIME",
          duration: "2 mois",
          skills: ["Vue.js", "Laravel", "MySQL", "Tailwind CSS", "API REST"],
          client: {
            name: "ProjectSoft",
            rating: 4.7,
            reviews: 18
          },
          postedDate: "il y a 3 jours",
          deadline: "15 janvier 2025",
          proposalsCount: 12,
          featured: false,
          hasApplied: false
        }
      ],
      
      userStats: {
        applicationsSent: 8,
        interviews: 3,
        successRate: 75
      }
    };
  },
  computed: {
    filteredSkills() {
      return this.allSkills.filter(skill =>
        skill.toLowerCase().includes(this.skillFilter.toLowerCase())
      );
    },
    
    filteredMissions() {
      return this.missions.filter(mission => {
        // Filtre de recherche
        if (this.searchQuery && !mission.title.toLowerCase().includes(this.searchQuery.toLowerCase()) &&
            !mission.description.toLowerCase().includes(this.searchQuery.toLowerCase()) &&
            !mission.skills.some(skill => skill.toLowerCase().includes(this.searchQuery.toLowerCase()))) {
          return false;
        }
        
        // Filtre par budget
        if (this.filters.minBudget && mission.budget < this.filters.minBudget) return false;
        if (this.filters.maxBudget && mission.budget > this.filters.maxBudget) return false;
        
        // Filtre par compétences
        if (this.filters.skills.length > 0 && 
            !this.filters.skills.some(skill => mission.skills.includes(skill))) {
          return false;
        }
        
        // Filtre par type
        if (this.filters.types.length > 0 && !this.filters.types.includes(mission.type)) {
          return false;
        }
        
        // Filtres rapides
        if (this.activeQuickFilter === 'featured' && !mission.featured) return false;
        if (this.activeQuickFilter === 'urgent') {
          const daysLeft = this.getDaysLeft(mission.deadline);
          if (daysLeft > 7) return false;
        }
        if (this.activeQuickFilter === 'budget_high' && mission.budget < 2000) return false;
        if (this.activeQuickFilter === 'new') {
          const isNew = mission.postedDate.includes('jour') && 
                       parseInt(mission.postedDate) <= 2;
          if (!isNew) return false;
        }
        
        return true;
      });
    },
    
    sortedMissions() {
      const missions = [...this.filteredMissions];
      
      switch (this.sortBy) {
        case 'budget_high':
          return missions.sort((a, b) => b.budget - a.budget);
        case 'budget_low':
          return missions.sort((a, b) => a.budget - b.budget);
        case 'deadline':
          return missions.sort((a, b) => this.getDaysLeft(a.deadline) - this.getDaysLeft(b.deadline));
        case 'newest':
        default:
          return missions.sort((a, b) => b.id - a.id);
      }
    },
    
    paginatedMissions() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return this.sortedMissions.slice(start, end);
    },
    
    totalPages() {
      return Math.ceil(this.filteredMissions.length / this.itemsPerPage);
    },
    
    visiblePages() {
      const pages = [];
      const start = Math.max(1, this.currentPage - 2);
      const end = Math.min(this.totalPages, start + 4);
      
      for (let i = start; i <= end; i++) {
        pages.push(i);
      }
      return pages;
    },
    
    isApplicationValid() {
      return this.application.proposal.trim() && 
             this.application.proposedBudget > 0 && 
             this.application.deliveryTime.trim();
    }
  },
  methods: {
    toggleQuickFilter(filterId) {
      this.activeQuickFilter = this.activeQuickFilter === filterId ? null : filterId;
      this.currentPage = 1;
    },
    
    resetFilters() {
      this.searchQuery = '';
      this.activeQuickFilter = null;
      this.filters = {
        minBudget: null,
        maxBudget: null,
        skills: [],
        types: []
      };
      this.currentPage = 1;
    },
    
    getTypeLabel(type) {
      const labels = {
        FULL_TIME: 'Temps plein',
        PART_TIME: 'Temps partiel',
        FREELANCE: 'Freelance'
      };
      return labels[type] || type;
    },
    
    getDaysLeft(deadline) {
      // Simulation simple - en réalité, il faudrait parser la date
      return Math.floor(Math.random() * 30) + 1;
    },
    
    viewMission(missionId) {
      console.log('Voir mission:', missionId);
      // Navigation vers les détails de la mission
    },
    
    applyToMission(mission) {
      this.selectedMission = mission;
      this.application.proposedBudget = mission.budget;
      this.showApplicationModal = true;
    },
    
    closeModal() {
      this.showApplicationModal = false;
      this.selectedMission = null;
      this.application = {
        proposal: '',
        proposedBudget: null,
        deliveryTime: ''
      };
    },
    
    submitApplication() {
      if (!this.isApplicationValid) return;
      
      console.log('Candidature envoyée:', {
        mission: this.selectedMission,
        application: this.application
      });
      
      // Marquer la mission comme postulée
      const missionIndex = this.missions.findIndex(m => m.id === this.selectedMission.id);
      if (missionIndex !== -1) {
        this.missions[missionIndex].hasApplied = true;
      }
      
      this.userStats.applicationsSent++;
      alert('✅ Candidature envoyée avec succès !');
      this.closeModal();
    },
    
    prevPage() {
      if (this.currentPage > 1) this.currentPage--;
    },
    
    nextPage() {
      if (this.currentPage < this.totalPages) this.currentPage++;
    },
    
    goToPage(page) {
      this.currentPage = page;
    }
  },
  watch: {
    filters: {
      handler() {
        this.currentPage = 1;
      },
      deep: true
    },
    
    searchQuery() {
      this.currentPage = 1;
    },
    
    sortBy() {
      this.currentPage = 1;
    }
  }
};
</script>

<style scoped>
.missions-page {
  max-width: 1400px;
  margin: 0 auto;
  padding: 2rem;
}

.missions-header {
  margin-bottom: 2rem;
}

.header-main h1 {
  font-size: 2.5rem;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 0.5rem;
}

.header-main p {
  color: #6b7280;
  font-size: 1.125rem;
}

.header-actions {
  display: flex;
  gap: 2rem;
  margin-top: 1.5rem;
  flex-wrap: wrap;
}

.search-box {
  position: relative;
  flex: 1;
  min-width: 300px;
}

.search-input {
  width: 100%;
  padding: 1rem 3rem 1rem 1rem;
  border: 2px solid #e5e7eb;
  border-radius: 12px;
  font-size: 1rem;
  transition: all 0.3s;
  background: white;
}

.search-input:focus {
  outline: none;
  border-color: #4f46e5;
  box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
}

.search-icon {
  position: absolute;
  right: 1rem;
  top: 50%;
  transform: translateY(-50%);
  color: #6b7280;
}

.filter-buttons {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.filter-btn {
  padding: 0.75rem 1.5rem;
  border: 2px solid #e5e7eb;
  background: white;
  border-radius: 25px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.3s;
  white-space: nowrap;
}

.filter-btn.active,
.filter-btn:hover {
  border-color: #4f46e5;
  background: #4f46e5;
  color: white;
}

.missions-content {
  display: grid;
  grid-template-columns: 300px 1fr;
  gap: 2rem;
}

.filters-sidebar {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.filter-section {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.08);
  border: 1px solid #f3f4f6;
}

.filter-section h3 {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 1.5rem;
  padding-bottom: 0.75rem;
  border-bottom: 2px solid #f8fafc;
}

.filter-group {
  margin-bottom: 1.5rem;
}

.filter-group label {
  display: block;
  margin-bottom: 0.75rem;
  font-weight: 600;
  color: #374151;
  font-size: 0.875rem;
}

.budget-range {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.budget-input {
  flex: 1;
  padding: 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 0.875rem;
}

.budget-input:focus {
  outline: none;
  border-color: #4f46e5;
}

.skill-input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 0.875rem;
  margin-bottom: 0.75rem;
}

.skills-list {
  max-height: 200px;
  overflow-y: auto;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  padding: 0.5rem;
}

.skill-checkbox,
.type-checkbox {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem;
  cursor: pointer;
  font-size: 0.875rem;
  border-radius: 4px;
  transition: background 0.3s;
}

.skill-checkbox:hover,
.type-checkbox:hover {
  background: #f8fafc;
}

.skill-checkbox input,
.type-checkbox input {
  display: none;
}

.checkmark {
  width: 16px;
  height: 16px;
  border: 2px solid #d1d5db;
  border-radius: 3px;
  position: relative;
  transition: all 0.3s;
}

.skill-checkbox input:checked + .checkmark,
.type-checkbox input:checked + .checkmark {
  background: #4f46e5;
  border-color: #4f46e5;
}

.checkmark::after {
  content: '✓';
  position: absolute;
  color: white;
  font-size: 12px;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  opacity: 0;
  transition: opacity 0.3s;
}

.skill-checkbox input:checked + .checkmark::after,
.type-checkbox input:checked + .checkmark::after {
  opacity: 1;
}

.btn-reset-filters {
  width: 100%;
  padding: 0.75rem;
  background: #f3f4f6;
  color: #374151;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.3s;
}

.btn-reset-filters:hover {
  background: #e5e7eb;
}

.stats-sidebar {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.08);
  border: 1px solid #f3f4f6;
}

.stats-sidebar h4 {
  font-size: 1.125rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 1rem;
}

.stat-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 0;
  border-bottom: 1px solid #f3f4f6;
}

.stat-item:last-child {
  border-bottom: none;
}

.stat-number {
  font-weight: 700;
  color: #4f46e5;
  font-size: 1.125rem;
}

.stat-label {
  color: #6b7280;
  font-size: 0.875rem;
}

.missions-list {
  flex: 1;
}

.list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.list-header h2 {
  font-size: 1.5rem;
  font-weight: 600;
  color: #1f2937;
  margin: 0;
}

.sort-options {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.sort-options label {
  color: #6b7280;
  font-size: 0.875rem;
}

.sort-select {
  padding: 0.5rem;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  background: white;
  font-size: 0.875rem;
}

.missions-grid {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.mission-card {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.08);
  border: 1px solid #f3f4f6;
  position: relative;
  transition: transform 0.3s, box-shadow 0.3s;
}

.mission-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0,0,0,0.12);
}

.mission-card.featured {
  border-left: 4px solid #f59e0b;
}

.mission-badge {
  position: absolute;
  top: -10px;
  right: 1rem;
  background: #f59e0b;
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 600;
}

.mission-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
  gap: 1rem;
}

.mission-title-section h3 {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1f2937;
  margin: 0 0 0.5rem 0;
  line-height: 1.3;
}

.mission-meta {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.mission-type {
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
}

.mission-type.FULL_TIME { background: #dbeafe; color: #1e40af; }
.mission-type.PART_TIME { background: #fef3c7; color: #92400e; }
.mission-type.FREELANCE { background: #d1fae5; color: #065f46; }

.mission-duration {
  color: #6b7280;
  font-size: 0.875rem;
}

.mission-budget {
  text-align: right;
  flex-shrink: 0;
}

.budget-amount {
  display: block;
  font-size: 1.5rem;
  font-weight: 700;
  color: #10b981;
  line-height: 1;
}

.budget-type {
  font-size: 0.75rem;
  color: #6b7280;
}

.mission-description {
  color: #6b7280;
  line-height: 1.5;
  margin-bottom: 1rem;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.mission-skills {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.skill-tag {
  background: #e0e7ff;
  color: #4f46e5;
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 500;
}

.more-skills {
  color: #9ca3af;
  font-size: 0.75rem;
  font-style: italic;
}

.mission-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  gap: 1rem;
}

.mission-client {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex: 1;
}

.client-avatar {
  width: 40px;
  height: 40px;
  background: #4f46e5;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  flex-shrink: 0;
}

.client-info {
  display: flex;
  flex-direction: column;
}

.client-name {
  font-weight: 600;
  color: #374151;
  font-size: 0.875rem;
}

.client-rating {
  color: #6b7280;
  font-size: 0.75rem;
}

.mission-actions {
  display: flex;
  gap: 0.5rem;
  flex-shrink: 0;
}

.mission-timeline {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 1rem;
  border-top: 1px solid #f3f4f6;
  font-size: 0.75rem;
  color: #9ca3af;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.pagination {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 2rem 0;
}

.pagination-btn {
  padding: 0.75rem 1.5rem;
  border: 1px solid #d1d5db;
  background: white;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s;
}

.pagination-btn:hover:not(:disabled) {
  background: #f3f4f6;
  border-color: #9ca3af;
}

.pagination-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.page-numbers {
  display: flex;
  gap: 0.5rem;
}

.page-btn {
  width: 40px;
  height: 40px;
  border: 1px solid #d1d5db;
  background: white;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s;
}

.page-btn.active,
.page-btn:hover {
  background: #4f46e5;
  color: white;
  border-color: #4f46e5;
}

.empty-state {
  text-align: center;
  padding: 4rem 2rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.08);
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.empty-state h3 {
  font-size: 1.5rem;
  color: #1f2937;
  margin-bottom: 0.5rem;
}

.empty-state p {
  color: #6b7280;
  margin-bottom: 2rem;
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 1rem;
}

.modal-content {
  background: white;
  border-radius: 12px;
  max-width: 600px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 20px 25px rgba(0, 0, 0, 0.1);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #e5e7eb;
}

.modal-header h3 {
  margin: 0;
  color: #1f2937;
}

.btn-close {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #6b7280;
  padding: 0;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: background 0.3s;
}

.btn-close:hover {
  background: #f3f4f6;
}

.modal-body {
  padding: 1.5rem;
}

.mission-preview {
  background: #f8fafc;
  padding: 1rem;
  border-radius: 8px;
  margin-bottom: 1.5rem;
}

.mission-preview h4 {
  margin: 0 0 0.5rem 0;
  color: #1f2937;
}

.mission-preview .budget {
  color: #10b981;
  font-weight: 600;
  margin: 0;
}

.modal-body .form-group {
  margin-bottom: 1.5rem;
}

.modal-body .form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: #374151;
}

.modal-body .form-group input,
.modal-body .form-group textarea {
  width: 100%;
  padding: 0.875rem;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.3s;
  font-family: inherit;
}

.modal-body .form-group textarea {
  resize: vertical;
  min-height: 120px;
}

.modal-body .form-group input:focus,
.modal-body .form-group textarea:focus {
  outline: none;
  border-color: #4f46e5;
}

.form-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  margin-top: 2rem;
}

/* Responsive */
@media (max-width: 1024px) {
  .missions-content {
    grid-template-columns: 1fr;
  }
  
  .filters-sidebar {
    order: 2;
  }
}

@media (max-width: 768px) {
  .missions-page {
    padding: 1rem;
  }
  
  .header-actions {
    flex-direction: column;
  }
  
  .search-box {
    min-width: auto;
  }
  
  .mission-header {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .mission-budget {
    text-align: left;
  }
  
  .mission-footer {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .mission-actions {
    width: 100%;
    justify-content: stretch;
  }
  
  .mission-actions .btn {
    flex: 1;
  }
  
  .mission-timeline {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.25rem;
  }
  
  .pagination {
    flex-direction: column;
    gap: 1rem;
  }
  
  .form-actions {
    flex-direction: column;
  }
}

@media (max-width: 480px) {
  .header-main h1 {
    font-size: 2rem;
  }
  
  .filter-buttons {
    justify-content: center;
  }
  
  .filter-btn {
    flex: 1;
    min-width: 120px;
    text-align: center;
  }
  
  .list-header {
    flex-direction: column;
    gap: 1rem;
    align-items: flex-start;
  }
}
</style>