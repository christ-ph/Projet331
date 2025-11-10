<template>
  <div class="freelance-profile">
    <div class="profile-header">
      <div class="header-content">
        <h1>Mon Profil Freelance</h1>
        <p>Complétez votre profil pour attirer plus de clients et augmenter vos chances de décrocher des missions.</p>
      </div>
      <div class="completion-badge" v-if="completionPercentage < 100">
        <div class="completion-progress">
          <div class="progress-circle">
            <span class="percentage">{{ completionPercentage }}%</span>
          </div>
        </div>
        <p>Profil complété à {{ completionPercentage }}%</p>
      </div>
    </div>

    <div class="profile-container">
      <form @submit.prevent="saveProfile" class="profile-form">
        <!-- Informations Personnelles -->
        <div class="form-section">
          <div class="section-header">
            <h2>👤 Informations personnelles</h2>
            <span class="section-badge" v-if="isPersonalInfoComplete">✅</span>
          </div>
          <div class="form-grid">
            <div class="form-group">
              <label for="first_name">Prénom *</label>
              <input 
                v-model="profile.first_name" 
                id="first_name"
                placeholder="Votre prénom" 
                required
              />
            </div>
            <div class="form-group">
              <label for="last_name">Nom *</label>
              <input 
                v-model="profile.last_name" 
                id="last_name"
                placeholder="Votre nom" 
                required
              />
            </div>
          </div>
          <div class="form-group">
            <label for="title">Titre professionnel *</label>
            <input 
              v-model="profile.title" 
              id="title"
              placeholder="Ex: Développeur Full Stack, Designer UX/UI..." 
              required
            />
            <small>Ce titre sera visible par les clients</small>
          </div>
          <div class="form-group">
            <label for="description">Description *</label>
            <textarea 
              v-model="profile.description" 
              id="description"
              placeholder="Décrivez votre expertise, votre expérience et ce que vous pouvez apporter aux clients..."
              rows="4"
              required
            ></textarea>
            <small>{{ profile.description.length }}/500 caractères</small>
          </div>
        </div>

        <!-- Compétences -->
        <div class="form-section">
          <div class="section-header">
            <h2>🛠️ Compétences</h2>
            <span class="section-badge" v-if="profile.skills.length > 0">✅</span>
          </div>
          <div class="form-group">
            <label>Ajouter des compétences *</label>
            <div class="skills-input-container">
              <input 
                v-model="newSkill" 
                @keydown.enter.prevent="addSkill"
                placeholder="Ex: React, Node.js, UX Design..." 
                class="skills-input"
              />
              <button type="button" @click="addSkill" class="btn-add-skill" :disabled="!newSkill.trim()">
                <span>+</span>
              </button>
            </div>
            <small>Appuyez sur Entrée ou cliquez sur + pour ajouter</small>
          </div>
          <div class="skills-list" v-if="profile.skills.length > 0">
            <div v-for="(skill, index) in profile.skills" :key="index" class="skill-tag">
              <span>{{ skill }}</span>
              <button type="button" @click="removeSkill(index)" class="btn-remove-skill">
                <span>×</span>
              </button>
            </div>
          </div>
          <div v-else class="empty-state">
            <p>🚫 Aucune compétence ajoutée. Ajoutez au moins 3 compétences.</p>
          </div>
        </div>

        <!-- Tarifs et Disponibilité -->
        <div class="form-section">
          <div class="section-header">
            <h2>💰 Tarifs et disponibilité</h2>
            <span class="section-badge" v-if="profile.hourly_rate">✅</span>
          </div>
          <div class="form-grid">
            <div class="form-group">
              <label for="hourly_rate">Taux horaire (€) *</label>
              <div class="input-with-icon">
                <span class="input-icon">€</span>
                <input 
                  v-model.number="profile.hourly_rate" 
                  id="hourly_rate"
                  type="number" 
                  placeholder="50" 
                  min="0"
                  required
                />
              </div>
              <small>Votre taux horaire moyen</small>
            </div>
            <div class="form-group">
              <label for="availability">Disponibilité *</label>
              <select v-model="profile.availability" id="availability" required>
                <option value="">Sélectionnez...</option>
                <option value="AVAILABLE">🟢 Disponible immédiatement</option>
                <option value="PART_TIME">🟡 Temps partiel (20h/semaine)</option>
                <option value="BUSY">🟠 Occupé (10h/semaine)</option>
                <option value="UNAVAILABLE">🔴 Indisponible</option>
              </select>
              <small>Votre disponibilité actuelle</small>
            </div>
          </div>
        </div>

                  <!-- Portfolio -->
                  <div class="form-section">
                    <div class="section-header">
                      <h2>📁 Portfolio</h2>
                      <span class="section-badge" v-if="portfolio.length > 0">✅</span>
                    </div>
                    
                    <div class="portfolio-items">
                      <div v-for="(item, index) in portfolio" :key="index" class="portfolio-item">
                        <div class="portfolio-item-header">
                          <h4>Projet {{ index + 1 }}</h4>
                          <button type="button" @click="removePortfolioItem(index)" class="btn-remove-item">
                            Supprimer
                          </button>
                        </div>
                        <div class="form-grid">
                          <div class="form-group">
                            <label>Titre du projet</label>
                            <input v-model="item.title" placeholder="Nom de votre projet" />
                          </div>
                          <div class="form-group">
                            <label>URL du projet</label>
                            <input v-model="item.project_url" placeholder="https://..." type="url" />
                          </div>
                        </div>
                        <div class="form-group">
                          <label>Description</label>
                          <textarea v-model="item.description" placeholder="Décrivez le projet, vos responsabilités, les technologies utilisées..." rows="3"></textarea>
                        </div>
                      </div>
                    </div>
                            <!-- <button type="button" @click="addPortfolioItem" class="btn-add-portfolio">
                      <span>+</span>
                      Ajouter un projet
                    </button> -->

                   <button type="button" @click="addPortfolioItem" class="btn-add-portfolio">
                    <span>+</span>
                    Ajouter un projet
                  </button>

                  </div>

                  <!-- Actions -->
                  <div class="form-actions">
                    <button type="button" @click="resetForm" class="btn btn-secondary" :disabled="loading">
                      Annuler
                    </button>
                    <button type="submit" class="btn btn-primary" :disabled="loading || !isFormValid">
                      <span v-if="loading">
                        <div class="spinner"></div>
                        Sauvegarde...
                      </span>
                      <span v-else>
                        💾 Sauvegarder le profil
                      </span>
                    </button>
                  </div>
                </form>

  
      <!-- Aperçu du profil -->
      <div class="profile-preview">
        <div class="preview-card">
          <h3>Aperçu de votre profil</h3>
          <div class="preview-content">
            <div class="preview-header">
              <div class="preview-avatar">
                {{ profile.first_name?.charAt(0) || 'F' }}{{ profile.last_name?.charAt(0) || 'L' }}
              </div>
              <div class="preview-info">
                <h4>{{ profile.title || 'Titre professionnel' }}</h4>
                <p>{{ profile.first_name || 'Prénom' }} {{ profile.last_name || 'Nom' }}</p>
              </div>
            </div>
            
            <div class="preview-section" v-if="profile.description">
              <h5>À propos</h5>
              <p class="preview-description">{{ profile.description }}</p>
            </div>

            <div class="preview-section" v-if="profile.skills.length > 0">
              <h5>Compétences</h5>
              <div class="preview-skills">
                <span v-for="skill in profile.skills.slice(0, 5)" :key="skill" class="preview-skill">
                  {{ skill }}
                </span>
                <span v-if="profile.skills.length > 5" class="preview-more">
                  +{{ profile.skills.length - 5 }} plus
                </span>
              </div>
            </div>

            <div class="preview-section" v-if="profile.hourly_rate">
              <h5>Tarif</h5>
              <p class="preview-rate">{{ profile.hourly_rate }}€/heure</p>
            </div>

            <div class="preview-section" v-if="portfolio.length > 0">
              <h5>Projets récents</h5>
              <div class="preview-projects">
                <div v-for="item in portfolio.slice(0, 2)" :key="item.title" class="preview-project">
                  <strong>{{ item.title || 'Titre du projet' }}</strong>
                  <p>{{ item.description ? item.description.substring(0, 60) + '...' : 'Description du projet' }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import {
  updateProfile,
  getProfile,
  getPortfolioItems,
  addPortfolioItem,
  updatePortfolioItem,
  deletePortfolioItem,
} from '@/services/api';

const STORAGE_KEY = 'freelance_profile_data';

export default {
  name: 'FreelanceProfileView',
  props: ['currentUser'],
  data() {
    return {
      profile: {
        first_name: '',
        last_name: '',
        title: '',
        description: '',
        skills: [],
        hourly_rate: null,
        availability: 'AVAILABLE',
      },
      portfolio: [],
      newSkill: '',
      loading: false,
      existingProfileId: null,
    };
  },
  computed: {
    isPersonalInfoComplete() {
      return this.profile.first_name && this.profile.last_name && this.profile.title && this.profile.description;
    },
    completionPercentage() {
      let completed = 0;
      const totalFields = 6;
      if (this.profile.first_name) completed++;
      if (this.profile.last_name) completed++;
      if (this.profile.title) completed++;
      if (this.profile.description) completed++;
      if (this.profile.skills.length >= 3) completed++;
      if (this.profile.hourly_rate) completed++;
      return Math.round((completed / totalFields) * 100);
    },
    isFormValid() {
      return (
        this.profile.first_name &&
        this.profile.last_name &&
        this.profile.title &&
        this.profile.description &&
        this.profile.skills.length >= 3 &&
        this.profile.hourly_rate &&
        this.profile.availability
      );
    },
  },
  watch: {
    profile: {
      deep: true,
      handler(newProfile) {
        const data = { profile: newProfile, portfolio: this.portfolio };
        localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
      },
    currentUser(newVal) {
      if (!newVal) {
        this.$router.push('/');
      }
    },
    },
    portfolio: {
      deep: true,
      handler(newPortfolio) {
        const data = { profile: this.profile, portfolio: newPortfolio };
        localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
      }
    }
  },
  methods: {
    addSkill() {
      const skill = this.newSkill.trim();
      if (skill && !this.profile.skills.includes(skill)) {
        this.profile.skills.push(skill);
        this.newSkill = '';
      }
    },
    removeSkill(index) {
      this.profile.skills.splice(index, 1);
    },
    addPortfolioItem() {
      this.portfolio.push({ 
        title: '', 
        description: '', 
        project_url: '', 
        id: null 
      });
    },
    async removePortfolioItem(index) {
      const item = this.portfolio[index];
      
      // Si l'item a un ID, on le supprime de la base de données
      if (item.id && this.existingProfileId) {
        if (!confirm('Supprimer ce projet ?')) return;
        
        try {
          await deletePortfolioItem(this.existingProfileId, item.id);
          this.portfolio.splice(index, 1);
        } catch (err) {
          console.error('Erreur suppression portfolio:', err);
          alert('❌ Erreur lors de la suppression du projet');
        }
      } else {
        // Sinon, on le supprime simplement du tableau local
        this.portfolio.splice(index, 1);
      }
    },
    async savePortfolioItems() {
      if (!this.existingProfileId) return;
      
      for (const item of this.portfolio) {
        try {
          if (item.id) {
            // Mise à jour d'un item existant
            await updatePortfolioItem(this.existingProfileId, item.id, item);
          } else if (item.title.trim()) {
            // Création d'un nouvel item
            const response = await addPortfolioItem(this.existingProfileId, item);
            item.id = response.data.id;
          }
        } catch (err) {
          console.error('Erreur sauvegarde portfolio:', err);
        }
      }
    },
    async saveProfile() {
      if (!this.isFormValid) {
        alert('Veuillez compléter tous les champs obligatoires');
        return;
      }
      
      this.loading = true;
      try {
        // Sauvegarde du profil principal
        const response = await updateProfile(this.currentUser.id, this.profile);
        
        if (response.data) {
          this.existingProfileId = response.data.id;
          
          // Sauvegarde des items du portfolio
          await this.savePortfolioItems();
        }
        
        alert('✅ Profil sauvegardé avec succès !');
      } catch (err) {
        console.error('Erreur sauvegarde profil:', err);
        alert('❌ Erreur lors de la sauvegarde du profil');
      } finally {
        this.loading = false;
      }
    },
    loadProfileData() {
      // Essayer de charger depuis le localStorage d'abord
      const savedData = localStorage.getItem(STORAGE_KEY);
      if (savedData) {
        try {
          const { profile, portfolio } = JSON.parse(savedData);
          this.profile = { ...this.profile, ...profile };
          this.portfolio = portfolio || [];
        } catch (e) {
          console.error('Erreur parsing localStorage:', e);
        }
      }
      
      // Ensuite charger depuis l'API si l'utilisateur a un profil existant
      if (this.currentUser && this.currentUser.freelance_profile) {
        const profile = this.currentUser.freelance_profile;
        this.existingProfileId = profile.id;
        
        // Fusionner avec les données existantes (ne pas écraser les modifications locales)
        this.profile = {
          first_name: profile.first_name || this.profile.first_name,
          last_name: profile.last_name || this.profile.last_name,
          title: profile.title || this.profile.title,
          description: profile.description || this.profile.description,
          skills: profile.skills || this.profile.skills,
          hourly_rate: profile.hourly_rate || this.profile.hourly_rate,
          availability: profile.availability || this.profile.availability,
        };
        
        // Charger le portfolio depuis l'API
        this.loadPortfolioFromAPI(profile.id);
      }
    },
    async loadPortfolioFromAPI(profileId) {
      try {
        const { data } = await getPortfolioItems(profileId);
        if (data && data.length > 0) {
          this.portfolio = data;
        }
      } catch (err) {
        console.error('Erreur chargement portfolio:', err);
      }
    },
    resetForm() {
      if (confirm('Voulez-vous vraiment annuler toutes les modifications ? Les données non sauvegardées seront perdues.')) {
        // Réinitialiser avec les données originales
        this.profile = {
          first_name: '',
          last_name: '',
          title: '',
          description: '',
          skills: [],
          hourly_rate: null,
          availability: 'AVAILABLE',
        };
        this.portfolio = [];
        this.newSkill = '';
        
        // Recharger les données depuis le localStorage ou l'API
        this.loadProfileData();
      }
    },
  },
  mounted() {
    this.loadProfileData();
  },
};
</script>


<style scoped>
.freelance-profile {
  max-width: 1400px;
  margin: 0 auto;
  padding: 2rem;
}

.profile-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 3rem;
  padding-bottom: 2rem;
  border-bottom: 1px solid #e5e7eb;
}

.header-content h1 {
  font-size: 2.5rem;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 0.5rem;
}

.header-content p {
  color: #6b7280;
  font-size: 1.125rem;
  max-width: 600px;
}

.completion-badge {
  text-align: center;
}

.progress-circle {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: conic-gradient(#10b981 0% v-bind('completionPercentage')0%, #e5e7eb 0% 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 0.5rem;
  position: relative;
}

.progress-circle::before {
  content: '';
  position: absolute;
  width: 60px;
  height: 60px;
  background: white;
  border-radius: 50%;
}

.percentage {
  position: relative;
  font-weight: 700;
  color: #1f2937;
  font-size: 1.125rem;
}

.completion-badge p {
  color: #6b7280;
  font-size: 0.875rem;
  margin: 0;
}

.profile-container {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 3rem;
}

.profile-form {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.form-section {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.08);
  border: 1px solid #f3f4f6;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid #f8fafc;
}

.section-header h2 {
  font-size: 1.5rem;
  font-weight: 600;
  color: #1f2937;
  margin: 0;
}

.section-badge {
  background: #10b981;
  color: white;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.75rem;
}

.form-grid {
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
  font-weight: 600;
  color: #374151;
}

.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 0.875rem 1rem;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.3s;
  background: #fafafa;
  font-family: inherit;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #4f46e5;
  background: white;
  box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
}

.form-group textarea {
  resize: vertical;
  min-height: 100px;
}

.form-group small {
  display: block;
  margin-top: 0.5rem;
  color: #9ca3af;
  font-size: 0.75rem;
}

.input-with-icon {
  position: relative;
}

.input-icon {
  position: absolute;
  left: 1rem;
  top: 50%;
  transform: translateY(-50%);
  color: #6b7280;
  font-weight: 600;
}

.input-with-icon input {
  padding-left: 2.5rem;
}

/* Skills Styles */
.skills-input-container {
  display: flex;
  gap: 0.5rem;
}

.skills-input {
  flex: 1;
  margin-bottom: 0;
}

.btn-add-skill {
  background: #10b981;
  color: white;
  border: none;
  border-radius: 8px;
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background 0.3s;
  flex-shrink: 0;
}

.btn-add-skill:hover:not(:disabled) {
  background: #059669;
}

.btn-add-skill:disabled {
  background: #9ca3af;
  cursor: not-allowed;
}

.skills-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-top: 1rem;
}

.skill-tag {
  background: #e0e7ff;
  color: #4f46e5;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  font-weight: 500;
}

.btn-remove-skill {
  background: none;
  border: none;
  color: #4f46e5;
  cursor: pointer;
  font-size: 1.125rem;
  padding: 0;
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: background 0.3s;
}

.btn-remove-skill:hover {
  background: rgba(79, 70, 229, 0.1);
}

.empty-state {
  background: #f8fafc;
  padding: 1.5rem;
  border-radius: 8px;
  text-align: center;
  color: #6b7280;
  margin-top: 1rem;
}

/* Portfolio Styles */
.portfolio-items {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

.portfolio-item {
  background: #f8fafc;
  padding: 1.5rem;
  border-radius: 8px;
  border-left: 4px solid #4f46e5;
}

.portfolio-item-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.portfolio-item-header h4 {
  margin: 0;
  color: #374151;
  font-size: 1.125rem;
}

.btn-remove-item {
  background: #ef4444;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.875rem;
  transition: background 0.3s;
}

.btn-remove-item:hover {
  background: #dc2626;
}

.btn-add-portfolio {
  background: transparent;
  color: #4f46e5;
  border: 2px dashed #4f46e5;
  padding: 1rem 1.5rem;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.3s;
  width: 100%;
  justify-content: center;
}

.btn-add-portfolio:hover {
  background: #4f46e5;
  color: white;
}

/* Form Actions */
.form-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  padding-top: 2rem;
  border-top: 1px solid #e5e7eb;
}

.form-actions .btn {
  min-width: 140px;
  justify-content: center;
}

.spinner {
  width: 16px;
  height: 16px;
  border: 2px solid transparent;
  border-top: 2px solid currentColor;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-right: 0.5rem;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Preview Styles */
.profile-preview {
  position: sticky;
  top: 2rem;
  height: fit-content;
}

.preview-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.1);
  padding: 2rem;
  border: 1px solid #e5e7eb;
}

.preview-card h3 {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 1.5rem;
  text-align: center;
}

.preview-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid #f3f4f6;
}

.preview-avatar {
  width: 60px;
  height: 60px;
  background: linear-gradient(135deg, #4f46e5, #7c3aed);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 1.25rem;
  flex-shrink: 0;
}

.preview-info h4 {
  margin: 0 0 0.25rem 0;
  color: #1f2937;
  font-size: 1.125rem;
}

.preview-info p {
  margin: 0;
  color: #6b7280;
  font-size: 0.875rem;
}

.preview-section {
  margin-bottom: 1.5rem;
}

.preview-section h5 {
  font-size: 0.875rem;
  font-weight: 600;
  color: #374151;
  margin: 0 0 0.75rem 0;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.preview-description {
  color: #6b7280;
  font-size: 0.875rem;
  line-height: 1.5;
  margin: 0;
}

.preview-skills {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.preview-skill {
  background: #e0e7ff;
  color: #4f46e5;
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 500;
}

.preview-more {
  color: #9ca3af;
  font-size: 0.75rem;
  font-style: italic;
}

.preview-rate {
  color: #10b981;
  font-weight: 600;
  font-size: 1.125rem;
  margin: 0;
}

.preview-projects {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.preview-project {
  background: #f8fafc;
  padding: 1rem;
  border-radius: 6px;
}

.preview-project strong {
  display: block;
  color: #374151;
  font-size: 0.875rem;
  margin-bottom: 0.25rem;
}

.preview-project p {
  color: #6b7280;
  font-size: 0.75rem;
  margin: 0;
  line-height: 1.4;
}

/* Responsive */
@media (max-width: 1024px) {
  .profile-container {
    grid-template-columns: 1fr;
    gap: 2rem;
  }
  
  .profile-preview {
    position: static;
    order: -1;
  }
}

@media (max-width: 768px) {
  .freelance-profile {
    padding: 1rem;
  }
  
  .profile-header {
    flex-direction: column;
    gap: 1.5rem;
    text-align: center;
  }
  
  .form-grid {
    grid-template-columns: 1fr;
  }
  
  .form-section {
    padding: 1.5rem;
  }
  
  .form-actions {
    flex-direction: column;
  }
  
  .form-actions .btn {
    min-width: auto;
  }
}

@media (max-width: 480px) {
  .header-content h1 {
    font-size: 2rem;
  }
  
  .skills-input-container {
    flex-direction: column;
  }
  
  .btn-add-skill {
    width: 100%;
    height: 48px;
  }
  
  .portfolio-item-header {
    flex-direction: column;
    gap: 1rem;
    align-items: flex-start;
  }
}
</style>