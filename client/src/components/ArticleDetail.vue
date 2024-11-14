<template>
  <div class="article-detail">
    <div v-if="loading" class="loading">
      <span>Loading...</span>
    </div>
    <div v-else-if="error" class="error">
      <span>{{ error }}</span>
    </div>
    <div v-else class="content">
      <h1>{{ article.title }}</h1>
      <div class="metadata">
        <p><strong>Author:</strong> {{ article.author }}</p>
        <p><strong>Published Date:</strong> {{ formatDate(article.pub_date) }}</p>
        <p><strong>Source:</strong> {{ article.source }}</p>
        <p>
          <strong>Feedback: </strong>
          <span :class="['feedback-dot', feedbackClass(article.label)]"></span>
          {{ feedbackText(article.label) }}
        </p>
      </div>
      <div class="article-body">
        <p><strong>Headline:</strong> {{ article.headline }}</p>
        <p>{{ article.description }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "ArticleDetail",
  data() {
    return {
      article: {},
      loading: true,
      error: null,
    };
  },
  async created() {
    const id = this.$route.params.id;
    // Check if the article is stored in session storage
    const storedArticle = sessionStorage.getItem(`article_${id}`);

    if (storedArticle) {
      // Parse and set the article data if it exists in session storage
      this.article = JSON.parse(storedArticle);
      this.loading = false;
    } else {
      // Otherwise, fetch the article from the API
      try {
        const response = await axios.get(`http://localhost:5000/articles/${id}`);
        this.article = response.data;
        // Store the fetched article in session storage
        sessionStorage.setItem(`article_${id}`, JSON.stringify(this.article));
      } catch (err) {
        this.error = "Failed to load article details.";
        console.error(err);
      } finally {
        this.loading = false;
      }
    }
  },
  methods: {
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
    feedbackText(label) {
      return label === -1 ? "Negative" : label === 0 ? "Neutral" : "Positive";
    },
    feedbackClass(label) {
      return label === -1 ? "negative" : label === 1 ? "positive" : "neutral";
    },
  },
};
</script>


<style scoped>
.article-detail {
  max-width: 800px;
  margin: 20px auto;
  padding: 25px;
  background-color: #ffffff;
  border-radius: 10px;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
  font-family: Arial, sans-serif;
  transition: box-shadow 0.3s ease;
}

.article-detail:hover {
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
}

.loading,
.error {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 300px;
  font-size: 1.2em;
  color: #333;
}

.content h1 {
  font-size: 1.8em;
  color: #333;
  margin-bottom: 15px;
  font-weight: bold;
}

.metadata {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
  color: #555;
  margin-bottom: 20px;
}

.metadata p {
  font-size: 1em;
  color: #666;
  margin: 0;
}

.article-body p {
  font-size: 1.05em;
  line-height: 1.6;
  color: #333;
}

.feedback-dot {
  display: inline-block;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  margin-right: 6px;
  vertical-align: middle;
}

.feedback-dot.positive {
  background-color: #28a745;
}

.feedback-dot.negative {
  background-color: #dc3545;
}

.feedback-dot.neutral {
  background-color: #6c757d;
}
</style>
