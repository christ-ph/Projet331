
<template>
  <div class="missions-client-page">
    <div class="missions-header">
      <div class="header-main">
        <h1>🎯 Mes Missions</h1>
        <p>Gérez vos missions publiées et créez de nouvelles opportunités</p>
      </div>
      
      <div class="header-actions">
        <button @click="showCreateModal" class="btn btn-primary">
          ➕ Créer une mission
        </button>
      </div>
    </div>

    <div class="client-stats">
      <div class="stat-card">
        <div class="stat-icon">📋</div>
        <div class="stat-content">
          <h3>Missions totales</h3>
          <p class="stat-number">{{ stats.totalMissions }}</p>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">📨</div>
        <div class="stat-content">
          <h3>Candidatures</h3>
          <p class="stat-number">{{ stats.totalApplications }}</p>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">⚡</div>
        <div class="stat-content">
          <h3>En cours</h3>
          <p class="stat-number">{{ stats.activeMissions }}</p>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">✅</div>
        <div class="stat-content">
          <h3>Terminées</h3>
          <p class="stat-number">{{ stats.completedMissions }}</p>
        </div>
      </div>
    </div>

    <div class="filters-bar">
      <div class="search-box">
        <input 
          v-model="searchQuery" 
          placeholder="Rechercher dans mes missions..." 
          type="text"
          class="search-input"
        />
        <span class="search-icon">🔍</span>
      </div>
      
      <div class="filter-buttons">
        <button 
          v-for="filter in statusFilters" 
          :key="filter.id"
          :class="['filter-btn', { active: activeStatusFilter === filter.id }]"
          @click="toggleStatusFilter(filter.id)"
        >
          {{ filter.label }}
        </button>
      </div>
    </div>

    <div class="missions-list">
      <div class="list-header">
        <h2>{{ filteredMissions.length }} mission(s)</h2>
        <div class="sort-options">
          <label>Trier par:</label>
          <select v-model="sortBy" class="sort-select">
            <option value="newest">Plus récentes</option>
            <option value="oldest">Plus anciennes</option>
            <option value="budget_high">Budget (élevé)</option>
            <option value="budget_low">Budget (faible)</option>
            <option value="applications">Candidatures (nombre)</option>
          </select>
        </div>
      </div>

      <div class="missions-grid">
        <div 
          v-for="mission in sortedMissions" 
          :key="mission.id" 
          class="mission-card"
          :class="mission.status"
        >
          <div class="mission-status-badge" :class="mission.status">
            {{ getStatusLabel(mission.status) }}
          </div>
          
          <div class="mission-header">
            <div class="mission-title-section">
              <h3>{{ mission.title }}</h3>
              <div class="mission-meta">
                <span class="mission-type" :class="mission.type">
                  {{ getTypeLabel(mission.type) }}
                </span>
                <span class="mission-budget-display">{{ mission.budget }}€</span>
              </div>
            </div>
            <div class="mission-actions">
              <button 
                @click="viewMission(mission.id)" 
                class="btn btn-small btn-outline"
                title="Voir détails"
              >
                👀
              </button>
              <button 
                @click="editMission(mission.id)" 
                class="btn btn-small btn-outline"
                title="Modifier"
                :disabled="mission.status !== 'DRAFT' && mission.status !== 'PUBLISHED'"
              >
                ✏️
              </button>
              <button 
                @click="deleteMission(mission.id)" 
                class="btn btn-small btn-danger"
                title="Supprimer"
                :disabled="mission.status === 'IN_PROGRESS'"
              >
                🗑️
              </button>
            </div>
          </div>

          <p class="mission-description">{{ truncateDescription(mission.description) }}</p>

          <div class="mission-skills">
            <span 
              v-for="skill in mission.skills.slice(0, 3)" 
              :key="skill" 
              class="skill-tag"
            >
              {{ skill }}
            </span>
            <span v-if="mission.skills.length > 3" class="more-skills">
              +{{ mission.skills.length - 3 }}
            </span>
          </div>

          <div class="mission-stats">
            <div class="stat">
              <span class="stat-icon">📨</span>
              <span class="stat-value">{{ mission.applications_count || 0 }}</span>
              <span class="stat-label">candidatures</span>
            </div>
            <div class="stat">
              <span class="stat-icon">👁️</span>
              <span class="stat-value">{{ mission.views || 0 }}</span>
              <span class="stat-label">vues</span>
            </div>
            <div class="stat">
              <span class="stat-icon">⏱️</span>
              <span class="stat-value">{{ getDaysLeft(mission.deadline) }}</span>
              <span class="stat-label">jours</span>
            </div>
          </div>

          <div class="mission-footer">
            <div class="mission-dates">
              <span class="post-date">Publiée: {{ mission.postedDate }}</span>
              <span class="deadline">Échéance: {{ formatDate(mission.deadline) }}</span>
            </div>
            
            <div class="mission-primary-actions">
              <button 
                v-if="mission.status === 'PUBLISHED'"
                @click="viewApplications(mission.id)" 
                class="btn btn-primary btn-small"
              >
                📋 Voir candidatures
              </button>
              <button 
                v-else-if="mission.status === 'DRAFT'"
                @click="publishMission(mission.id)" 
                class="btn btn-success btn-small"
              >
                🚀 Publier
              </button>
              <button 
                v-else-if="mission.status === 'IN_PROGRESS'"
                @click="showCompleteOrCancelModal(mission.id)" 
                class="btn btn-info btn-small"
              >
                📊 Suivre / Terminer
              </button>
            </div>
          </div>
        </div>
      </div>

      <div v-if="filteredMissions.length === 0 && !loading" class="empty-state">
        <div class="empty-icon">📋</div>
        <h3>Aucune mission trouvée</h3>
        <p v-if="searchQuery || activeStatusFilter">
          Aucune mission ne correspond à vos critères de recherche
        </p>
        <p v-else>
          Vous n'avez pas encore créé de mission
        </p>
        <button @click="showCreateModal" class="btn btn-primary">
          ➕ Créer votre première mission
        </button>
      </div>

      <div v-if="loading" class="loading-state">
        <div class="spinner"></div>
        <p>Chargement de vos missions...</p>
      </div>
    </div>

    <div v-if="showCreateMissionModal" class="modal-overlay">
      <div class="modal-content large">
        <div class="modal-header">
          <h3>➕ Créer une nouvelle mission</h3>
          <button @click="closeCreateModal" class="btn-close">×</button>
        </div>
        
        <div class="modal-body">
          <form @submit.prevent="submitMission" class="create-mission-form">
            <div class="form-section">
              <h4>📝 Informations de base</h4>
              
              <div class="form-group">
                <label for="mission-title">Titre de la mission *</label>
                <input 
                  id="mission-title"
                  v-model="newMission.title" 
                  type="text" 
                  placeholder="Ex: Développement d'application mobile React Native"
                  required
                  maxlength="200"
                  class="form-input"
                >
                <div class="char-count">{{ newMission.title.length }}/200</div>
              </div>

              <div class="form-group">
                <label for="mission-description">Description détaillée *</label>
                <textarea 
                  id="mission-description"
                  v-model="newMission.description" 
                  rows="4"
                  placeholder="Décrivez votre projet en détail : objectifs, fonctionnalités attendues, contraintes techniques..."
                  required
                  class="form-textarea"
                ></textarea>
              </div>

              <div class="form-row">
                <div class="form-group">
                  <label for="mission-budget">Budget (€) *</label>
                  <input 
                    id="mission-budget"
                    v-model.number="newMission.budget" 
                    type="number" 
                    min="1"
                    step="0.01"
                    placeholder="Ex: 3000"
                    required
                    class="form-input"
                  >
                </div>

                <div class="form-group">
                  <label for="budget-type">Type de budget</label>
                  <select 
                    id="budget-type"
                    v-model="newMission.budget_type" 
                    class="form-select"
                  >
                    <option value="FIXED">Forfait</option>
                    <option value="HOURLY">À l'heure</option>
                  </select>
                </div>
              </div>
            </div>

            <div class="form-section">
              <h4>🛠️ Compétences requises</h4>
              <div class="skills-selector">
                <div class="skills-input">
                  <input 
                    v-model="skillInput" 
                    @keyup.enter="addSkill"
                    placeholder="Ajouter une compétence (React, Python, Design...)"
                    class="skill-input"
                  >
                  <button type="button" @click="addSkill" class="btn btn-small btn-primary">+ Ajouter</button>
                </div>
                <div class="selected-skills">
                  <span 
                    v-for="skill in newMission.required_skills" 
                    :key="skill"
                    class="skill-tag"
                  >
                    {{ skill }}
                    <button type="button" @click="removeSkill(skill)" class="remove-skill">×</button>
                  </span>
                  <div v-if="newMission.required_skills.length === 0" class="no-skills">
                    <p>Aucune compétence sélectionnée. Ajoutez les compétences requises pour votre projet.</p>
                  </div>
                </div>
              </div>
            </div>

            <div class="form-section">
              <h4>📅 Délais et type</h4>
              
              <div class="form-row">
                <div class="form-group">
                  <label for="mission-deadline">Date limite *</label>
                  <input 
                    id="mission-deadline"
                    v-model="newMission.deadline" 
                    type="date"
                    :min="minDate"
                    required
                    class="form-input"
                  >
                  <div class="help-text">La mission sera automatiquement fermée après cette date</div>
                </div>

                <div class="form-group">
                  <label for="mission-type">Type de mission</label>
                  <select 
                    id="mission-type"
                    v-model="newMission.mission_type" 
                    class="form-select"
                  >
                    <option value="FREELANCE">Freelance</option>
                    <option value="PART_TIME">Temps partiel</option>
                    <option value="FULL_TIME">Temps plein</option>
                  </select>
                </div>
              </div>

              <div class="form-group">
                <label for="mission-duration">Durée estimée</label>
                <input 
                  id="mission-duration"
                  v-model="newMission.duration" 
                  type="text" 
                  placeholder="Ex: 3-4 semaines, 2 mois, 6 mois..."
                  class="form-input"
                >
                <div class="help-text">Donnez une estimation de la durée du projet</div>
              </div>
            </div>

            <div class="form-section">
              <h4>⚙️ Options avancées</h4>
              
              <div class="form-group checkbox-group">
                <label class="checkbox">
                  <input type="checkbox" v-model="newMission.featured">
                  <span class="checkmark"></span>
                  Mettre en avant cette mission (recommandée)
                </label>
                <div class="help-text">Cette mission sera mise en évidence dans les résultats de recherche</div>
              </div>
            </div>

            <div class="form-actions">
              <button type="button" @click="closeCreateModal" class="btn btn-secondary">
                Annuler
              </button>
              <button 
                type="submit" 
                class="btn btn-primary" 
                :disabled="!isFormValid || creatingMission"
              >
                <span v-if="creatingMission" class="loading-spinner"></span>
                {{ creatingMission ? 'Publication...' : '🚀 Publier la mission' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
    
    <div v-if="showStatusUpdateModal && missionToUpdate" class="modal-overlay">
        <div class="modal-content small">
            <div class="modal-header">
                <h3>Mettre à jour: {{ missionToUpdate.title }}</h3>
                <button @click="closeStatusUpdateModal" class="btn-close">×</button>
            </div>
            
            <div class="modal-body">
                <p class="mission-status-info">
                    La mission est actuellement : 
                    <span :class="missionToUpdate.status">
                        {{ getStatusLabel(missionToUpdate.status) }}
                    </span>
                </p>

                <div class="alert alert-warning" v-if="missionToUpdate.status === 'IN_PROGRESS'">
                    Veuillez choisir le statut final pour cette mission.
                </div>

                <div class="form-actions-status">
                    
                    <button 
                    @click="confirmMissionStatusUpdate('COMPLETED')" 
                    :disabled="statusUpdateLoading"
                    class="btn btn-success btn-large"
                    >
                    <span v-if="statusUpdateLoading" class="loading-spinner"></span>
                    ✅ Marquer comme Terminé
                    </button>
                    
                    <button 
                    @click="confirmMissionStatusUpdate('CANCELLED')" 
                    :disabled="statusUpdateLoading"
                    class="btn btn-danger btn-large"
                    >
                    <span v-if="statusUpdateLoading" class="loading-spinner"></span>
                    ❌ Annuler la mission
                    </button>
                </div>

                <div class="help-text">
                    *Marquer comme **Terminé** change le statut à **COMPLETED**.
                    L'**Annulation** la passe à **CANCELLED**.
                </div>
                
            </div>
        </div>
    </div>
  </div>
</template>

<script>
// Assurez-vous que l'importation de completeOrCancelMission est correcte dans votre fichier d'API
import {createMission, deleteMission, updateMission, getUserMissions, completeOrCancelMission } from '@/services/api';

export default {
  name: 'MissionsViewClient',
  props: ['currentUser'],
  data() {
    return {
      missions: [],
      loading: false,
      searchQuery: '',
      activeStatusFilter: null,
      sortBy: 'newest',
      showCreateMissionModal: false,
      creatingMission: false,
      
      // NOUVEAU: Modal de complétion/annulation
      showStatusUpdateModal: false,
      missionToUpdate: null, 
      statusUpdateLoading: false,

      skillInput: '',
      isNewClient: false,
      
      newMission: {
        title: '',
        description: '',
        budget: null,
        budget_type: 'FIXED',
        mission_type: 'FREELANCE',
        duration: '',
        deadline: '',
        required_skills: [],
        featured: false
      },
      
      suggestedSkills: [
        'React', 'Vue.js', 'Node.js', 'Python', 'JavaScript', 'TypeScript',
        'UI/UX Design', 'Figma', 'Adobe XD', 'PHP', 'Laravel', 'Symfony',
        'WordPress', 'MongoDB', 'PostgreSQL', 'AWS', 'Docker', 'React Native',
        'Flutter', 'Swift', 'Kotlin', 'Java', 'C#', '.NET', 'HTML/CSS',
        'Tailwind CSS', 'Bootstrap', 'SASS', 'GraphQL', 'REST API', 'MySQL',
        'Firebase', 'Git', 'GitHub', 'CI/CD', 'Testing', 'Agile', 'Scrum'
      ],
      
      statusFilters: [
        { id: null, label: 'Toutes' },
        { id: 'DRAFT', label: 'Brouillons' },
        { id: 'PUBLISHED', label: 'Publiées' },
        { id: 'IN_PROGRESS', label: 'En cours' },
        { id: 'COMPLETED', label: 'Terminées' }
      ],
      
      stats: {
        totalMissions: 0,
        totalApplications: 0,
        activeMissions: 0,
        completedMissions: 0
      }
    };
  },

  computed: {
    filteredMissions() {
      let filtered = this.missions;

      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase();
        filtered = filtered.filter(mission => 
          mission.title.toLowerCase().includes(query) ||
          mission.description.toLowerCase().includes(query) ||
          (mission.skills && mission.skills.some(skill => skill.toLowerCase().includes(query)))
        );
      }

      if (this.activeStatusFilter) {
        filtered = filtered.filter(mission => mission.status === this.activeStatusFilter);
      }

      return filtered;
    },
    
    sortedMissions() {
      const missions = [...this.filteredMissions];
      
      switch (this.sortBy) {
        case 'oldest':
          return missions.sort((a, b) => new Date(a.created_at) - new Date(b.created_at));
        case 'budget_high':
          return missions.sort((a, b) => b.budget - a.budget);
        case 'budget_low':
          return missions.sort((a, b) => a.budget - b.budget);
        case 'applications':
          return missions.sort((a, b) => (b.applications_count || 0) - (a.applications_count || 0));
        case 'newest':
        default:
          return missions.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
      }
    },
    
    isFormValid() {
      return this.newMission.title.trim() && 
             this.newMission.description.trim() && 
             this.newMission.budget > 0 && 
             this.newMission.deadline &&
             this.newMission.required_skills.length > 0;
    },
    
    minDate() {
      return new Date().toISOString().split('T')[0];
    }
  },

  async mounted() {
    if (!this.currentUser) {
      this.$router.push('/login');
      return;
    }
    await this.loadClientMissions();
  },

  methods: {
    async loadClientMissions() {
      this.loading = true;
      try {
        // NOTE: L'API doit retourner applications_count et views, ou les laisser à 0
        const response = await getUserMissions(this.currentUser.id);
        
        if (response.data && response.data.missions) {
          this.missions = response.data.missions.map(mission => ({
            id: mission.id,
            title: mission.title,
            description: mission.description,
            budget: mission.budget,
            budgetType: mission.budget_type === 'FIXED' ? 'Forfait' : 'Horaire',
            budget_type: mission.budget_type,
            type: mission.mission_type || 'FREELANCE',
            mission_type: mission.mission_type,
            duration: mission.duration || 'Non définie',
            skills: mission.required_skills || [],
            required_skills: mission.required_skills || [],
            status: mission.status || 'DRAFT',
            applications_count: mission.applications_count || 0,
            views: mission.views || 0,
            created_at: mission.created_at,
            deadline: mission.deadline,
            postedDate: this.getRelativeTime(mission.created_at),
            featured: mission.featured || false
          }));
          
          this.calculateStats();

          if (this.missions.length === 0) {
            this.isNewClient = true;
            this.showCreateMissionModal = true;
          }

        } else {
          this.missions = [];
          this.isNewClient = true;
          this.showCreateMissionModal = true;
        }

      } catch (error) {
        console.error('Erreur chargement missions client:', error);
        alert('❌ Erreur lors du chargement de vos missions');
      } finally {
        this.loading = false;
      }
    },
    
    calculateStats() {
      this.stats.totalMissions = this.missions.length;
      this.stats.totalApplications = this.missions.reduce((total, mission) => 
        total + (mission.applications_count || 0), 0
      );
      this.stats.activeMissions = this.missions.filter(m => 
        m.status === 'PUBLISHED' || m.status === 'IN_PROGRESS'
      ).length;
      this.stats.completedMissions = this.missions.filter(m => 
        m.status === 'COMPLETED'
      ).length;
    },
    
    showCreateModal() {
      this.showCreateMissionModal = true;
    },
    
    closeCreateModal() {
      this.showCreateMissionModal = false;
      this.resetNewMission();
    },
    
    resetNewMission() {
      this.newMission = {
        title: '',
        description: '',
        budget: null,
        budget_type: 'FIXED',
        mission_type: 'FREELANCE',
        duration: '',
        deadline: '',
        required_skills: [],
        featured: false
      };
      this.skillInput = '';
    },
    
    addSkill() {
      const skill = this.skillInput.trim();
      if (skill && !this.newMission.required_skills.includes(skill)) {
        this.newMission.required_skills.push(skill);
        this.skillInput = '';
      }
    },
    
    removeSkill(skill) {
      this.newMission.required_skills = this.newMission.required_skills.filter(s => s !== skill);
    },
    
    async submitMission() {
      if (!this.isFormValid || this.creatingMission) return;
      
      this.creatingMission = true;
      try {
        const missionData = {
          title: this.newMission.title,
          description: this.newMission.description,
          budget: this.newMission.budget,
          budget_type: this.newMission.budget_type,
          mission_type: this.newMission.mission_type,
          duration: this.newMission.duration,
          deadline: this.newMission.deadline,
          required_skills: this.newMission.required_skills,
          client_id: this.currentUser.id,
          status: 'DRAFT',
          featured: this.newMission.featured
        };
        
        const response = await createMission(missionData);
        
        if (response.data && response.data.mission) {
          const createdMission = response.data.mission;
          
          const newMission = {
            id: createdMission.id,
            title: createdMission.title,
            description: createdMission.description,
            budget: createdMission.budget,
            budgetType: createdMission.budget_type === 'FIXED' ? 'Forfait' : 'Horaire',
            budget_type: createdMission.budget_type,
            type: createdMission.mission_type || 'FREELANCE',
            mission_type: createdMission.mission_type,
            duration: createdMission.duration || 'Non définie',
            skills: createdMission.required_skills || [],
            required_skills: createdMission.required_skills || [],
            status: createdMission.status || 'DRAFT',
            applications_count: 0,
            views: 0,
            created_at: createdMission.created_at || new Date().toISOString(),
            deadline: createdMission.deadline,
            postedDate: 'À l\'instant',
            featured: createdMission.featured || false
          };
          
          this.missions.unshift(newMission);
          this.calculateStats();
          this.closeCreateModal();

          this.isNewClient = false;

          alert('✅ Mission créée avec succès !');
        }
      } catch (error) {
        console.error('Erreur création mission:', error);
        alert('❌ Erreur lors de la création de la mission');
      } finally {
        this.creatingMission = false;
      }
    },
    
    viewMission(missionId) {
      this.$router.push(`/missions/${missionId}`);
    },
    
    editMission(missionId) {
      this.$router.push(`/missions/${missionId}/edit`);
    },
    
    async deleteMission(missionId) {
      if (!confirm('Êtes-vous sûr de vouloir supprimer cette mission ?')) return;
      
      try {
        await deleteMission(missionId);
        this.missions = this.missions.filter(m => m.id !== missionId);
        this.calculateStats();
        alert('✅ Mission supprimée avec succès');
      } catch (error) {
        console.error('Erreur suppression mission:', error);
        alert('❌ Erreur lors de la suppression de la mission');
      }
    },
    
    viewApplications(missionId) {
      this.$router.push(`/missions/${missionId}/applications`);
    },
    
    async publishMission(missionId) {
      try {
        const missionToUpdate = this.missions.find(m => m.id === missionId);
        if (!missionToUpdate) return;
        
        const updateData = { ...missionToUpdate, status: 'PUBLISHED' };
        
        await updateMission(missionId, updateData);
        
        const mission = this.missions.find(m => m.id === missionId);
        if (mission) mission.status = 'PUBLISHED';

        alert('✅ Mission publiée avec succès !');
      } catch (error) {
        console.error('Erreur publication mission:', error);
        alert('❌ Erreur lors de la publication de la mission');
      }
    },
    
    toggleStatusFilter(filterId) {
      this.activeStatusFilter = this.activeStatusFilter === filterId ? null : filterId;
    },
    
    // NOUVELLES MÉTHODES POUR LA MISE À JOUR DE STATUT
    showCompleteOrCancelModal(missionId) {
      this.missionToUpdate = this.missions.find(m => m.id === missionId);
      if (this.missionToUpdate) {
        this.showStatusUpdateModal = true;
      }
    },
    
    closeStatusUpdateModal() {
      this.showStatusUpdateModal = false;
      this.missionToUpdate = null;
    },


async confirmMissionStatusUpdate(newStatus) {
  if (!this.missionToUpdate || this.statusUpdateLoading) return;
  
  this.statusUpdateLoading = true;
  const missionId = this.missionToUpdate.id;
  
  // 🔧 CORRECTION: Utiliser 'COMPLETE' au lieu de 'COMPLETED'
  const data = { status_cible: newStatus === 'COMPLETED' ? 'COMPLETE' : newStatus };
  
  console.log('📤 Données envoyées:', data);
  
  try {
    const response = await completeOrCancelMission(missionId, data);
    
    if (response.data && response.data.mission) {
      // Mettre à jour la mission dans la liste locale 
      const index = this.missions.findIndex(m => m.id === missionId);
      if (index !== -1) {
        this.missions[index].status = response.data.mission.status;
        this.calculateStats();
      }

      // 🔧 CORRECTION: Ajuster les labels si nécessaire
      const statusLabel = newStatus === 'COMPLETED' ? 'COMPLETE' : newStatus;
      const displayLabel = this.getStatusLabel(statusLabel) || statusLabel;
      
      alert(`✅ Mission ${missionId} marquée comme "${displayLabel}" avec succès !`);
      
      this.closeStatusUpdateModal();
    }
  } catch (error) {
    console.error('Erreur mise à jour statut mission:', error);
    
    const errorMessage = error.response && error.response.data && error.response.data.message 
                         ? error.response.data.message 
                         : '❌ Erreur lors de la mise à jour du statut de la mission.';
                         
    alert(errorMessage);
    
  } finally {
    this.statusUpdateLoading = false;
  }
},    // FIN NOUVELLES MÉTHODES
    
    getStatusLabel(status) {
      const labels = {
        DRAFT: 'Brouillon',
        PUBLISHED: 'Publiée',
        IN_PROGRESS: 'En cours',
        COMPLETED: 'Terminée',
        CANCELLED: 'Annulée'
      };
      return labels[status] || status;
    },
    
    getTypeLabel(type) {
      const labels = {
        FULL_TIME: 'Temps plein',
        PART_TIME: 'Temps partiel',
        FREELANCE: 'Freelance'
      };
      return labels[type] || type;
    },
    
    truncateDescription(description) {
      if (!description) return '';
      return description.length > 150 
        ? description.substring(0, 150) + '...' 
        : description;
    },
    
    formatDate(dateString) {
      if (!dateString) return 'Non définie';
      return new Date(dateString).toLocaleDateString('fr-FR');
    },
    
    getDaysLeft(deadline) {
      if (!deadline) return '?';
      const today = new Date();
      const deadlineDate = new Date(deadline);
      const diffTime = deadlineDate - today;
      const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
      return diffDays > 0 ? diffDays : 0;
    },
    
    getRelativeTime(dateString) {
      if (!dateString) return 'Date inconnue';
      
      const date = new Date(dateString);
      const now = new Date();
      const diffMs = now - date;
      const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));
      const diffHours = Math.floor(diffMs / (1000 * 60 * 60));
      const diffMinutes = Math.floor(diffMs / (1000 * 60));
      
      if (diffMinutes < 1) return 'À l\'instant';
      if (diffMinutes < 60) return `il y a ${diffMinutes} minute${diffMinutes > 1 ? 's' : ''}`;
      if (diffHours < 24) return `il y a ${diffHours} heure${diffHours > 1 ? 's' : ''}`;
      if (diffDays < 7) return `il y a ${diffDays} jour${diffDays > 1 ? 's' : ''}`;
      if (diffDays < 30) return `il y a ${Math.floor(diffDays / 7)} semaine${Math.floor(diffDays / 7) > 1 ? 's' : ''}`;
      return `il y a ${Math.floor(diffDays / 30)} mois`;
    }
  }
};
</script>
<style scoped>
.missions-client-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.missions-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 2rem;
  padding-bottom: 2rem;
  border-bottom: 1px solid #e5e7eb;
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
  gap: 1rem;
}

/* Bouton principal */
.btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.3s ease;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.btn-primary {
  background: #4f46e5;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: #4338ca;
  transform: translateY(-1px);
}

.btn-primary:disabled {
  background: #9ca3af;
  cursor: not-allowed;
  transform: none;
}

.btn-secondary {
  background: #6b7280;
  color: white;
}

.btn-secondary:hover {
  background: #4b5563;
}

.btn-success {
  background: #10b981;
  color: white;
}

.btn-success:hover {
  background: #059669;
}

.btn-info {
  background: #06b6d4;
  color: white;
}

.btn-info:hover {
  background: #0891b2;
}

.btn-danger {
  background: #ef4444;
  color: white;
}

.btn-danger:hover:not(:disabled) {
  background: #dc2626;
}

.btn-danger:disabled {
  background: #fca5a5;
  cursor: not-allowed;
}

.btn-outline {
  background: white;
  border: 1px solid #d1d5db;
  color: #374151;
}

.btn-outline:hover {
  background: #f8fafc;
}

.btn-small {
  padding: 0.5rem 1rem;
  font-size: 0.75rem;
}

/* Statistiques */
.client-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.08);
  display: flex;
  align-items: center;
  gap: 1rem;
  border-left: 4px solid #4f46e5;
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

/* Barre de filtres */
.filters-bar {
  display: flex;
  gap: 2rem;
  margin-bottom: 2rem;
  align-items: center;
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

/* Liste des missions */
.missions-list {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.08);
  overflow: hidden;
}

.list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #f3f4f6;
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
  padding: 1.5rem;
  display: grid;
  gap: 1.5rem;
}

/* Carte de mission */
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

.mission-status-badge {
  position: absolute;
  top: -10px;
  right: 1rem;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
}

.mission-status-badge.DRAFT {
  background: #f3f4f6;
  color: #6b7280;
}

.mission-status-badge.PUBLISHED {
  background: #dbeafe;
  color: #1e40af;
}

.mission-status-badge.IN_PROGRESS {
  background: #fef3c7;
  color: #92400e;
}

.mission-status-badge.COMPLETED {
  background: #d1fae5;
  color: #065f46;
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
  align-items: center;
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

.mission-budget-display {
  background: #10b981;
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.875rem;
  font-weight: 600;
}

.mission-actions {
  display: flex;
  gap: 0.25rem;
  flex-shrink: 0;
}

.mission-description {
  color: #6b7280;
  line-height: 1.5;
  margin-bottom: 1rem;
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

.mission-stats {
  display: flex;
  gap: 2rem;
  margin-bottom: 1rem;
  padding: 1rem;
  background: #f8fafc;
  border-radius: 8px;
}

.stat {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.stat-icon {
  font-size: 1rem;
  width: auto;
  height: auto;
  background: none;
}

.stat-value {
  font-weight: 700;
  color: #1f2937;
}

.stat-label {
  color: #6b7280;
  font-size: 0.875rem;
}

.mission-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #f3f4f6;
}

.mission-dates {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  font-size: 0.875rem;
  color: #6b7280;
}

.mission-primary-actions {
  flex-shrink: 0;
}

/* États */
.empty-state,
.loading-state {
  text-align: center;
  padding: 4rem 2rem;
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

.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f4f6;
  border-left: 4px solid #4f46e5;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Modal */
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

.modal-content.large {
  max-width: 800px;
  width: 95%;
  max-height: 90vh;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #e5e7eb;
  background: white;
  border-radius: 12px 12px 0 0;
}

.modal-header h3 {
  margin: 0;
  color: #1f2937;
  font-size: 1.5rem;
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
  padding: 0;
  flex: 1;
  display: flex;
  flex-direction: column;
  background: white;
  border-radius: 0 0 12px 12px;
}

/* FORMULAIRE DE CRÉATION CORRIGÉ */
.create-mission-form {
  max-height: 70vh;
  overflow-y: auto;
  padding-right: 0.5rem;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.create-mission-form::-webkit-scrollbar {
  width: 6px;
}

.create-mission-form::-webkit-scrollbar-track {
  background: #f1f5f9;
  border-radius: 3px;
}

.create-mission-form::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 3px;
}

.form-section {
  margin-bottom: 0;
  padding: 1.5rem;
  background: #f8fafc;
  border-bottom: 1px solid #e5e7eb;
}

.form-section:last-child {
  border-bottom: none;
}

.form-section h4 {
  font-size: 1.125rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 1.5rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding-bottom: 0.75rem;
  border-bottom: 2px solid #e5e7eb;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group:last-child {
  margin-bottom: 0;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: #374151;
  font-size: 0.875rem;
}

.form-input,
.form-textarea,
.form-select {
  width: 100%;
  padding: 0.75rem;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  font-size: 0.875rem;
  font-family: inherit;
  transition: all 0.3s ease;
  background: white;
}

.form-input:focus,
.form-textarea:focus,
.form-select:focus {
  outline: none;
  border-color: #4f46e5;
  box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
}

.form-textarea {
  resize: vertical;
  min-height: 100px;
  line-height: 1.5;
}

.char-count {
  text-align: right;
  font-size: 0.75rem;
  color: #6b7280;
  margin-top: 0.25rem;
}

.help-text {
  font-size: 0.75rem;
  color: #6b7280;
  margin-top: 0.5rem;
  font-style: italic;
}

/* Skills Selector */
.skills-selector {
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  overflow: hidden;
  background: white;
}

.skills-input {
  display: flex;
  padding: 1rem;
  border-bottom: 1px solid #f3f4f6;
  background: #f8fafc;
  gap: 0.75rem;
  align-items: center;
}

.skill-input {
  flex: 1;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  padding: 0.75rem;
  font-size: 0.875rem;
  background: white;
}

.skill-input:focus {
  outline: none;
  border-color: #4f46e5;
}

.selected-skills {
  padding: 1rem;
  min-height: 60px;
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  align-items: flex-start;
  background: white;
}

.skill-tag {
  background: #e0e7ff;
  color: #4f46e5;
  padding: 0.5rem 0.75rem;
  border-radius: 20px;
  font-size: 0.875rem;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.3s ease;
}

.skill-tag:hover {
  background: #d1d5fd;
}

.remove-skill {
  background: none;
  border: none;
  color: #4f46e5;
  cursor: pointer;
  font-size: 1.125rem;
  font-weight: bold;
  padding: 0;
  width: 18px;
  height: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: all 0.3s ease;
}

.remove-skill:hover {
  background: #4f46e5;
  color: white;
}

.no-skills {
  color: #9ca3af;
  font-style: italic;
  text-align: center;
  width: 100%;
  padding: 1rem;
}

.no-skills p {
  margin: 0;
  font-size: 0.875rem;
}

/* Checkbox */
.checkbox-group {
  margin-top: 1rem;
}

.checkbox {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  cursor: pointer;
  font-weight: 500;
  font-size: 0.875rem;
  line-height: 1.4;
  padding: 0.5rem 0;
}

.checkbox input {
  display: none;
}

.checkmark {
  width: 20px;
  height: 20px;
  border: 2px solid #d1d5db;
  border-radius: 4px;
  position: relative;
  transition: all 0.3s ease;
  flex-shrink: 0;
  margin-top: 0.1rem;
  background: white;
}

.checkbox input:checked + .checkmark {
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
  transition: opacity 0.3s ease;
}

.checkbox input:checked + .checkmark::after {
  opacity: 1;
}

/* Form Actions */
.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 0;
  padding: 1.5rem;
  border-top: 1px solid #e5e7eb;
  background: white;
  border-radius: 0 0 12px 12px;
}

.loading-spinner {
  width: 16px;
  height: 16px;
  border: 2px solid transparent;
  border-top: 2px solid white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  display: inline-block;
  margin-right: 0.5rem;
}

/* Responsive */
@media (max-width: 768px) {
  .missions-client-page {
    padding: 1rem;
  }
  
  .missions-header {
    flex-direction: column;
    gap: 1rem;
  }
  
  .header-actions {
    width: 100%;
  }
  
  .header-actions .btn {
    width: 100%;
  }
  
  .client-stats {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .filters-bar {
    flex-direction: column;
    align-items: stretch;
  }
  
  .search-box {
    min-width: auto;
  }
  
  .list-header {
    flex-direction: column;
    gap: 1rem;
    align-items: flex-start;
  }
  
  .mission-header {
    flex-direction: column;
  }
  
  .mission-footer {
    flex-direction: column;
    align-items: stretch;
  }
  
  .mission-primary-actions {
    width: 100%;
  }
  
  .mission-primary-actions .btn {
    width: 100%;
  }
  
  /* Responsive formulaire */
  .modal-content.large {
    width: 98%;
    margin: 1rem;
  }
  
  .form-section {
    padding: 1rem;
  }
  
  .form-row {
    grid-template-columns: 1fr;
    gap: 0.75rem;
  }
  
  .skills-input {
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .skills-input .btn {
    width: 100%;
  }
  
  .form-actions {
    flex-direction: column-reverse;
    gap: 0.75rem;
  }
  
  .form-actions .btn {
    width: 100%;
  }
}

@media (max-width: 480px) {
  .header-main h1 {
    font-size: 2rem;
  }
  
  .client-stats {
    grid-template-columns: 1fr;
  }
  
  .filter-buttons {
    justify-content: center;
  }
  
  .filter-btn {
    flex: 1;
    min-width: 120px;
    text-align: center;
  }
  
  .form-section h4 {
    font-size: 1rem;
  }
  
  .form-input,
  .form-textarea,
  .form-select {
    padding: 0.875rem;
  }
  
  .selected-skills {
    padding: 0.75rem;
  }
  
  .skill-tag {
    font-size: 0.8rem;
    padding: 0.4rem 0.6rem;
  }
}

/* Améliorations visuelles */
.form-input::placeholder,
.form-textarea::placeholder,
.skill-input::placeholder {
  color: #9ca3af;
}

.form-select {
  cursor: pointer;
  background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 20 20'%3e%3cpath stroke='%236b7280' stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='m6 8 4 4 4-4'/%3e%3c/svg%3e");
  background-position: right 0.5rem center;
  background-repeat: no-repeat;
  background-size: 1.5em 1.5em;
  padding-right: 2.5rem;
  -webkit-appearance: none;
  -moz-appearance: none;
  appearance: none;
}

/* Animation pour l'ajout de compétences */
.skill-tag {
  animation: slideIn 0.3s ease;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>