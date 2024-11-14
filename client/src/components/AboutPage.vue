<template>
    <div class="about">
      <h1>About News Analyzer</h1>
      <p>
        The <strong>News Analyzer</strong> application provides users with insightful analysis of news articles by performing sentiment analysis. It allows you to quickly understand the general mood of news content and categorizes articles based on their sentiment and impact.
      </p>
      <h2>Project Flow</h2>
      <ol>
        <li><strong>News URL Extraction:</strong> The application starts by extracting URLs of news articles from a specified news source. This process gathers the links for articles, which are then used as inputs for the sentiment analysis phase.</li>
        <li><strong>Content Retrieval:</strong> Once URLs are collected, the app retrieves the article contents. This is where the core text of the news article is obtained for further analysis.</li>
        <li><strong>Sentiment Analysis:</strong> Using natural language processing techniques, the application analyzes the extracted content to determine its sentiment—positive, negative, or neutral.</li>
        <li><strong>Sentiment Categorization:</strong> Based on the analysis, each article is categorized. This allows users to filter articles by sentiment and assess the general mood of recent news.</li>
        <li><strong>Impact Assessment:</strong> Additionally, articles are assessed for their potential impact. High-impact articles are highlighted, allowing users to prioritize news based on importance.</li>
      </ol>
  
      <h2>Importance of News Analyzer</h2>
      <p>
        In today’s fast-paced world, keeping up with news can be overwhelming, and it’s challenging to quickly understand the sentiment behind the flood of information. <strong>News Analyzer</strong> helps users by providing:
      </p>
      <ul>
        <li><strong>Quick Insights:</strong> Sentiment categorization helps users gauge the mood of the news without having to read each article in detail.</li>
        <li><strong>Improved Decision-Making:</strong> By understanding both sentiment and impact, users can make more informed decisions about which news topics to prioritize.</li>
        <li><strong>Content Filtering:</strong> Users can filter out articles based on sentiment (positive, negative, or neutral), allowing for a more customized news-reading experience.</li>
        <li><strong>Efficiency:</strong> The application simplifies the news-consumption process, enabling users to grasp complex information at a glance.</li>
      </ul>
    </div>
  </template>
  
  <script>
  export default {
    name: "AboutPage",
  };
  </script>
  
  <style scoped>
  .about {
    max-width: 800px;
    margin: 20px auto;
    padding: 20px;
    background-color: #fff;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    font-family: Arial, sans-serif;
  }
  
  .about h2 {
    margin-top: 20px;
    font-size: 1.5em;
  }
  
  .about p, .about ol, .about ul {
    font-size: 1em;
    line-height: 1.6;
    color: #333;
  }
  
  .about ol, .about ul {
    margin: 10px 0 10px 20px;
  }
  
  .about li {
    margin-bottom: 10px;
  }
  </style>
  