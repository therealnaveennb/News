<template>
  <div class="dashboard">
    <div v-if="error" class="error">
      {{ error }}
    </div>
    <div v-else-if="loading" class="loading">Loading...</div>
    <div v-else>
      <!-- Filter dropdown -->
      <div class="filter">
        <label for="feedbackFilter">Filter by Feedback:</label>
        <select
          id="feedbackFilter"
          v-model="selectedFeedback"
          @change="applyFilter"
        >
          <option value="all">All</option>
          <option value="positive">Positive</option>
          <option value="neutral">Neutral</option>
          <option value="negative">Negative</option>
        </select>
      </div>
      <table class="article-table">
        <thead>
          <tr>
            <th>S.No</th>
            <th>Title</th>
            <th>Author</th>
            <th>Source</th>
            <th>Published Date</th>
            <th>Feedback</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="(article, index) in filteredArticles"
            :key="article._id"
            @click="navigateToArticle(article._id)"
            style="cursor: pointer"
          >
            <td>{{ index + 1 + (currentPage - 1) * itemsPerPage }}</td>
            <td>{{ article.title }}</td>
            <td>{{ article.author }}</td>
            <td>{{ article.source }}</td>
            <td>{{ formatDate(article.pub_date) }}</td>
            <td>
              <span
                :class="['feedback-dot', feedbackClass(article.label)]"
              ></span>
              {{ feedbackText(article.label) }}
            </td>
          </tr>
        </tbody>
      </table>
      <div class="pagination">
        <button @click="prevPage" :disabled="currentPage === 1">
          Previous
        </button>
        <span>Page {{ currentPage }} of {{ totalPages }}</span>
        <button @click="nextPage" :disabled="currentPage === totalPages">
          Next
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "DashBoard",
  data() {
    return {
      articles: [],
      loading: true,
      error: null,
      currentPage: 1,
      itemsPerPage: 10,
      selectedFeedback: "all", // Default filter is "all"
    };
  },
  computed: {
    totalPages() {
      return Math.ceil(this.filteredArticles.length / this.itemsPerPage);
    },
    filteredArticles() {
      if (this.selectedFeedback === "all") return this.articles;

      const feedbackMapping = {
        positive: 1,
        neutral: 0,
        negative: -1,
      };
      return this.articles.filter(
        (article) => article.label === feedbackMapping[this.selectedFeedback]
      );
    },
    paginatedArticles() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return this.filteredArticles.slice(start, end);
    },
  },
  mounted() {
    this.loadArticles();
  },
  methods: {
    loadArticles() {
      const storedArticles = sessionStorage.getItem("articles");

      if (storedArticles) {
        // Load articles from session storage if available
        this.articles = JSON.parse(storedArticles);
        this.loading = false;
      } else {
        // Otherwise, fetch articles from the server
        this.fetchArticles();
      }
    },
    async fetchArticles() {
      try {
        const response = await axios.get("http://localhost:5000/articles");
        this.articles = response.data
          .map((article) => ({
            ...article,
            id: article._id,
          }))
          .sort((a, b) => new Date(b.pub_date) - new Date(a.pub_date)); // Sort by newest date first

        // Store fetched articles in session storage
        sessionStorage.setItem("articles", JSON.stringify(this.articles));
      } catch (err) {
        this.error = "Failed to load articles data.";
        console.log(err);
      } finally {
        this.loading = false;
      }
    },
    navigateToArticle(id) {
      this.$router.push({ name: "ArticleDetail", params: { id } });
    },
    nextPage() {
      if (this.currentPage < this.totalPages) {
        this.currentPage++;
      }
    },
    prevPage() {
      if (this.currentPage > 1) {
        this.currentPage--;
      }
    },
    feedbackText(label) {
      return label === -1 ? "Negative" : label === 0 ? "Neutral" : "Positive";
    },
    feedbackClass(label) {
      return label === -1 ? "negative" : label === 1 ? "positive" : "neutral";
    },
    formatDate(dateString) {
      const date = new Date(dateString);
      const options = {
        weekday: "short",
        day: "2-digit",
        month: "short",
        year: "numeric",
      };
      return date.toLocaleDateString("en-GB", options);
    },
    applyFilter() {
      this.currentPage = 1; // Reset to first page after filter change
    },
  },
};
</script>



<style scoped>
.dashboard {
  max-width: 1200px;
  margin: 40px auto 20px;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  font-family: Arial, sans-serif;
}

.filter {
  margin-bottom: 15px;
  display: flex;
  align-items: center;
}

.filter label {
  margin-right: 10px;
  font-weight: bold;
}

.filter select {
  padding: 5px;
  font-size: 16px;
}

.loading,
.error {
  text-align: center;
  color: #555;
  font-size: 18px;
}

.article-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

.article-table th,
.article-table td {
  border: 1px solid #ddd;
  padding: 12px 15px;
  text-align: left;
}

.article-table th {
  background-color: #4caf50;
  color: white;
  font-weight: bold;
  text-transform: uppercase;
}

.article-table tr:nth-child(even) {
  background-color: #f2f2f2;
}

.article-table tr:hover {
  background-color: #f1f1f1;
}

.feedback-dot {
  display: inline-block;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  margin-right: 5px;
  vertical-align: middle;
}

.feedback-dot.positive {
  background-color: green;
}

.feedback-dot.negative {
  background-color: red;
}

.feedback-dot.neutral {
  background-color: grey;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 20px;
}

.pagination button {
  padding: 8px 12px;
  margin: 0 10px;
  font-size: 16px;
  cursor: pointer;
  border: none;
  border-radius: 4px;
  background-color: #4caf50;
  color: white;
  transition: background-color 0.3s;
}

.pagination button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.pagination button:hover:not(:disabled) {
  background-color: #45a049;
}

.pagination span {
  font-size: 16px;
}
</style>
