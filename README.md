# Book Discoverer Bot

Book Discoverer Bot is a Streamlit-powered assistant that uncovers compelling book recommendations tailored to your literary preferences. Powered by [Agno](https://github.com/agno-agi/agno), OpenAI's GPT-4o, and SerpAPI, the bot explores curated book lists across the web and delivers a personalized, well-formatted reading report — based on your taste, mood, and favorite genres.

## Folder Structure

```
Book-Discoverer-Bot/
├── book-discoverer-bot.py
├── README.md
└── requirements.txt
```

- **book-discoverer-bot.py**: The main Streamlit application.
- **requirements.txt**: Required Python packages.
- **README.md**: This documentation file.

## Features

- **Book Preference Input**  
  Fill in your age group, reading frequency, favorite genres, story styles, mood, and authors you love.

- **AI-Powered Book Research**  
  The Book Researcher agent uses SerpAPI to search the web using a targeted query based on your profile, collecting 10 highly relevant book recommendation sources.

- **Curated Book Report**  
  The Book Reporter agent reads these resources and crafts a structured book report with verified book titles, summaries, and reasons each one fits your taste.

- **Structured Markdown Output**  
  Your recommendations are beautifully formatted in markdown with sections, hyperlinks, and concise book summaries.

- **Download Option**  
  Download your personalized book recommendation report as a `.txt` file.

- **Clean Streamlit UI**  
  Designed with a simple, focused interface so you can explore books without distractions.

## Prerequisites

- Python 3.11 or higher  
- An OpenAI API key ([Get one here](https://platform.openai.com/account/api-keys))  
- A SerpAPI key ([Get one here](https://serpapi.com/manage-api-key))

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/akash301191/Book-Discoverer-Bot.git
   cd Book-Discoverer-Bot
   ```

2. **(Optional) Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate        # On macOS/Linux
   # or
   venv\Scripts\activate           # On Windows
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the app**:
   ```bash
   streamlit run book-discoverer-bot.py
   ```

2. **In your browser**:
   - Add your OpenAI and SerpAPI keys via the sidebar.
   - Fill in your reading profile and preferences.
   - Click **🔍 Generate Book Recommendations**.
   - View your AI-generated recommendation report with titles, summaries, and source links.

3. **Download Option**  
   Use the **📥 Download Book Recommendations** button to save your reading list as a `.txt` file.

---

## Code Overview

- **`render_book_preferences()`**: Captures reader preferences, including genres, mood, style, and past favorites.
- **`render_sidebar()`**: Manages API key inputs and stores them in Streamlit’s session state.
- **`generate_book_recommendations()`**:  
  - Runs the **Book Researcher** agent to search for curated book lists using SerpAPI.  
  - Passes those links to the **Book Reporter** agent to generate a personalized, structured reading report.
- **`main()`**: Configures the app layout, renders input components, and ties everything together.

## Contributions

Contributions are welcome! Feel free to fork the repo, suggest features, report bugs, or open a pull request. Please ensure your updates are clean, well-commented, and aligned with the bot’s mission.