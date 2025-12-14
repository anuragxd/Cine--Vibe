# 🎬 Cine-Vibe Curator

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-red)
![LangGraph](https://img.shields.io/badge/LangGraph-Agent-orange)
![Gemini](https://img.shields.io/badge/AI-Gemini%201.5%20Flash-green)
![TMDB](https://img.shields.io/badge/Data-TMDB%20API-blueviolet)

**Cine-Vibe Curator** is an intelligent, agentic movie recommendation engine. Unlike traditional search bars that rely on keywords, this agent understands **mood, context, and abstract descriptions** (e.g., *"I want a psychological thriller that feels like Shutter Island"*).

It uses a **LangGraph** pipeline to orchestrate decision-making and the **TMDB API** to fetch rich visual metadata (posters, ratings, and streaming availability).

## ✨ Features

* **🧠 "Vibe-Based" Search:** Uses Google Gemini to translate abstract user moods into concrete movie candidates.
* **🖼️ Rich Visual UI:** Displays high-quality movie posters, star ratings, and release dates in a clean "Netflix-style" card layout.
* **📺 Streaming Info:** Automatically detects where the movie is streaming in your region (e.g., Netflix, Prime Video).
* **🛡️ Robust Error Handling:** Includes regex-based parsing to ensure the AI's output is always correctly formatted, even if the model "chatters."
* **⚡ Speed:** Leverages parallel processing concepts to fetch metadata for multiple movies instantly.

## 🛠️ Architecture

The project follows a **Sequential Agentic Workflow**:

1.  **Curator Node (The Brain):**
    * Receives user input (Mood/Vibe).
    * Uses **Gemini 1.5 Flash** to brainstorm 3 culturally relevant movie recommendations.
    * Outputs a sanitized list of movie titles.

2.  **Fetcher Node (The Worker):**
    * Takes the titles from the Curator.
    * Queries the **TMDB API** for each title.
    * Retrieves metadata: Poster URL, Overview, Rating, and Watch Providers.

3.  **UI Layer (Streamlit):**
    * Renders the data into interactive columns with expanders for plot summaries.

## 🚀 Getting Started

### Prerequisites

* Python 3.9+
* **Google Gemini API Key** (Get it [here](https://aistudio.google.com/))
* **TMDB API Access Token** (Get it [here](https://www.themoviedb.org/settings/api))

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd movie_agent
