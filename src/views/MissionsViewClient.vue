<template>
  <div class="create-mission">
    <h1>📝 Créer une nouvelle mission</h1>

    <form @submit.prevent="submitMission" class="mission-form">
      <!-- Titre -->
      <div class="form-group">
        <label for="title">Titre de la mission *</label>
        <input
          id="title"
          v-model="mission.title"
          type="text"
          placeholder="Ex: Développement d'une application mobile"
          required
        />
      </div>

      <!-- Description -->
      <div class="form-group">
        <label for="description">Description *</label>
        <textarea
          id="description"
          v-model="mission.description"
          rows="5"
          placeholder="Décrivez en détail les tâches, les attentes, les livrables..."
          required
        ></textarea>
      </div>

      <!-- Budget -->
      <div class="form-group">
        <label for="budget">Budget (€) *</label>
        <input
          id="budget"
          v-model.number="mission.budget"
          type="number"
          min="0"
          placeholder="Ex: 1200"
          required
        />
      </div>

      <!-- Type de budget -->
      <div class="form-group">
        <label for="budget_type">Type de budget *</label>
        <select v-model="mission.budget_type" id="budget_type" required>
          <option value="FIXED">💰 Forfait (montant fixe)</option>
          <option value="HOURLY">⏱ Taux horaire</option>
        </select>
      </div>

      <!-- Deadline -->
      <div class="form-group">
        <label for="deadline">Date limite *</label>
        <input id="deadline" v-model="mission.deadline" type="date" required />
      </div>

      <!-- Compétences requises -->
      <div class="form-group">
        <label>Compétences requises *</label>
        <div class="skills-input-container">
          <input
            v-model="newSkill"
            @keydown.enter.prevent="addSkill"
            type="text"
            placeholder="Ex: React, Python, Figma..."
          />
          <button
            type="button"
            @click="addSkill"
            class="btn-add-skill"
            :disabled="!newSkill.trim()"
          >
            +
          </button>
        </div>
        <div class="skills-list" v-if="mission.required_skills.length > 0">
          <div
            v-for="(skill, index) in mission.required_skills"
            :key="index"
            class="skill-tag"
          >
            {{ skill }}
            <button type="button" @click="removeSkill(index)">×</button>
          </div>
        </div>
      </div>

      <!-- Boutons -->
      <div class="form-actions">
        <button type="button" @click="resetForm" class="btn btn-secondary">
          Annuler
        </button>
        <button
          type="submit"
          class="btn btn-primary"
          :disabled="loading || !isFormValid"
        >
          <span v-if="loading">⏳ Création...</span>
          <span v-else>✅ Créer la mission</span>
        </button>
      </div>
    </form>
  </div>
</template>

<script>
import { createMission } from "@/services/api";

export default {
  name: "CreateMissionView",
  props: {
    currentUser: {
      type: Object,
      default: () => null,
    },
  },
  data() {
    return {
      mission: {
        title: "",
        description: "",
        budget: null,
        budget_type: "FIXED",
        deadline: "",
        required_skills: [],
      },
      newSkill: "",
      loading: false,
    };
  },
  computed: {
    isFormValid() {
      return (
        this.mission.title &&
        this.mission.description &&
        this.mission.budget &&
        this.mission.deadline &&
        this.mission.required_skills.length > 0
      );
    },
  },
  methods: {
    addSkill() {
      const skill = this.newSkill.trim();
      if (skill && !this.mission.required_skills.includes(skill)) {
        this.mission.required_skills.push(skill);
        this.newSkill = "";
      }
    },
    removeSkill(index) {
      this.mission.required_skills.splice(index, 1);
    },
    resetForm() {
      if (
        confirm("Voulez-vous vraiment annuler ? Les données non sauvegardées seront perdues.")
      ) {
        this.mission = {
          title: "",
          description: "",
          budget: null,
          budget_type: "FIXED",
          deadline: "",
          required_skills: [],
        };
      }
    },
    async submitMission() {
      if (!this.isFormValid) {
        alert("⚠️ Veuillez remplir tous les champs obligatoires !");
        return;
      }

      if (!this.currentUser || !this.currentUser.id) {
        alert("❌ Vous devez être connecté pour créer une mission !");
        return;
      }

      this.loading = true;
      try {
        const payload = {
          ...this.mission,
          client_id: this.currentUser.id,
        };

        const response = await createMission(payload);

        if (response.status === 201 || response.status === 200) {
          alert("✅ Mission créée avec succès !");
          this.$router.push("/dashboard-client");
        } else {
          alert("❌ Erreur lors de la création de la mission !");
        }
      } catch (err) {
        console.error("Erreur création mission :", err);
        alert("❌ Une erreur est survenue.");
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style scoped>
.create-mission {
  max-width: 700px;
  margin: 0 auto;
  padding: 2rem;
}
h1 {
  margin-bottom: 1.5rem;
  text-align: center;
}
.form-group {
  margin-bottom: 1rem;
}
input,
textarea,
select {
  width: 100%;
  padding: 0.6rem;
  border-radius: 6px;
  border: 1px solid #ccc;
}
.skills-input-container {
  display: flex;
  gap: 0.5rem;
}
.btn-add-skill {
  background-color: #2563eb;
  color: white;
  border: none;
  padding: 0.5rem 0.8rem;
  border-radius: 5px;
}
.skills-list {
  margin-top: 0.5rem;
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem;
}
.skill-tag {
  background: #e0e7ff;
  color: #1e3a8a;
  padding: 0.4rem 0.6rem;
  border-radius: 4px;
  font-size: 0.9rem;
}
.skill-tag button {
  margin-left: 6px;
  background: none;
  border: none;
  color: red;
  cursor: pointer;
}
.form-actions {
  margin-top: 1.5rem;
  display: flex;
  justify-content: space-between;
}
.btn {
  padding: 0.6rem 1.2rem;
  border-radius: 6px;
  cursor: pointer;
}
.btn-primary {
  background: #16a34a;
  color: white;
  border: none;
}
.btn-secondary {
  background: #f3f4f6;
  color: #374151;
  border: 1px solid #d1d5db;
}
</style>
