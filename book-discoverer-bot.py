import streamlit as st
from agno.agent import Agent
from agno.tools.serpapi import SerpApiTools
from agno.models.openai import OpenAIChat

from textwrap import dedent

def render_book_preferences():
    st.markdown("---")
    col1, col2, col3 = st.columns(3)

    # Column 1: Reader Profile
    with col1:
        st.subheader("📖 Reader Profile")
        age_group = st.selectbox(
            "Your Age Group",
            ["Under 18", "18–24", "25–34", "35–49", "50+"]
        )
        reading_frequency = st.selectbox(
            "How often do you read?",
            ["Daily", "A few times a week", "Occasionally", "Rarely"]
        )
        books_per_month = st.selectbox(
            "Books per Month",
            ["0–1", "2–4", "5–7", "8+"]
        )
        book_format = st.selectbox(
            "Preferred Book Format",
            ["Physical", "eBooks", "Audiobooks", "Mixed"]
        )
        trend_preference = st.selectbox(
        "Do you follow reading trends or prefer niche/underrated books?",
        ["Trending books", "Hidden gems", "A mix of both"]
    )

    # Column 2: Reading Preferences
    with col2:
        st.subheader("📚 Genre & Style Preferences")
        favorite_genres = st.multiselect(
            "Favorite Genres",
            ["Fantasy", "Science Fiction", "Mystery / Thriller", "Romance", "Historical Fiction",
             "Contemporary / Drama", "Horror", "Biography / Memoir", "Self-help / Personal Development",
             "Non-fiction", "Young Adult", "Poetry", "Classics"]
        )
        story_style = st.multiselect(
            "Preferred Story Style",
            ["Uplifting and feel-good", "Dark and intense", "Slow and introspective",
             "Fast-paced and action-packed", "Deeply emotional", "Humorous and witty", "Philosophical"]
        )
        structure_pref = st.radio(
            "Do you prefer series or stand-alone books?",
            ["Series", "Stand-alone", "No preference"]
        )
        focus_preference = st.radio(
            "What do you prefer in a story?",
            ["Character-driven", "Plot-driven", "A balance of both"]
        )

    # Column 3: Mood & Goals
    with col3:
        st.subheader("🧠 Mood & Discovery Goals")
        current_mood = st.selectbox(
            "What are you in the mood to read?",
            ["Something light and fun", "Challenging or thought-provoking", "A page-turning thriller",
             "A deep, emotional story", "An inspiring read", "A romantic tale", "Surprise me!"]
        )
        reading_goal = st.selectbox(
            "What’s your reading goal right now?",
            ["To relax and unwind", "To learn or grow", "To escape into another world",
             "To be inspired", "Just exploring options"]
        )
        preferred_length = st.selectbox(
            "Preferred Book Length",
            ["Short (<250 pages)", "Medium (250–400 pages)", "Long (400+ pages)", "Doesn’t matter"]
        )
        favorite_authors = st.text_input("Any favorite authors? (optional)", placeholder="e.g., Neil Gaiman, Haruki Murakami")
        books_loved = st.text_input("Books you've loved recently (optional)", placeholder="e.g., The Night Circus, Sapiens, Atomic Habits")

    # Assemble book preference profile
    book_profile = f"""
    **Reader Profile:**
    - Age Group: {age_group}
    - Reading Frequency: {reading_frequency}
    - Books/Month: {books_per_month}
    - Format Preference: {book_format}
    - Trend Preference: {trend_preference}

    **Genre & Story Preferences:**
    - Genres: {', '.join(favorite_genres) if favorite_genres else 'Not specified'}
    - Story Style: {', '.join(story_style) if story_style else 'Not specified'}
    - Book Type Preference: {structure_pref}
    - Focus: {focus_preference}

    **Mood & Goals:**
    - Current Mood: {current_mood}
    - Reading Goal: {reading_goal}
    - Preferred Length: {preferred_length}
    - Favorite Authors: {favorite_authors.strip() if favorite_authors else 'Not specified'}
    - Recent Favorite Books: {books_loved.strip() if books_loved else 'Not specified'}
    """

    return book_profile

def render_sidebar():
    st.sidebar.title("🔐 API Configuration")
    st.sidebar.markdown("---")

    # OpenAI API Key input
    openai_api_key = st.sidebar.text_input(
        "OpenAI API Key",
        type="password",
        help="Don't have an API key? Get one [here](https://platform.openai.com/account/api-keys)."
    )
    if openai_api_key:
        st.session_state.openai_api_key = openai_api_key
        st.sidebar.success("✅ OpenAI API key updated!")

    # SerpAPI Key input
    serp_api_key = st.sidebar.text_input(
        "Serp API Key",
        type="password",
        help="Don't have an API key? Get one [here](https://serpapi.com/manage-api-key)."
    )
    if serp_api_key:
        st.session_state.serp_api_key = serp_api_key
        st.sidebar.success("✅ Serp API key updated!")

    st.sidebar.markdown("---")

def generate_book_recommendations(user_book_preferences: str) -> str:
    # Step 1: Run Book Researcher Agent 
    research_agent = Agent(
        name="Book Researcher",
        role="Finds curated and relevant book recommendations based on the user's literary profile, mood, and preferences.",
        model=OpenAIChat(id='gpt-4o', api_key=st.session_state.openai_api_key),
        description=dedent("""
            You are a book discovery specialist. Your role is to help users find curated, high-quality book recommendations by exploring reliable sources online.
            Based on the user's detailed preferences—such as genre, reading mood, favorite authors, and story style—you'll generate a focused book search query, perform a web search, and extract the most relevant links.
        """),
        instructions=[
            "Carefully read the user's book profile to understand their genre preferences, emotional tone, reading goal, and recent favorites.",
            "From this profile, generate ONE highly focused search term. Be descriptive and specific (e.g., 'emotional character-driven historical fiction like The Song of Achilles').",
            "Avoid vague queries like 'book recommendations' or 'popular books 2024'.",
            "Use the `search_google` tool with your query.",
            "From the search results, extract 10 of the most relevant links pointing to curated book recommendation lists, Goodreads lists, blogs, or review-based discovery platforms.",
            "Give priority to sources like Goodreads, Book Riot, NYT Books, NPR, Literary Hub, and trusted book blogs.",
            "Do not create or fabricate links. Only include real ones from the search results.",
            "You are not writing a summary or book report. Only return the links and any brief titles associated with them.",
        ],
        tools=[SerpApiTools(api_key=st.session_state.serp_api_key)],
        add_datetime_to_instructions=True,
    )

    research_response = research_agent.run(user_book_preferences)
    research_results = research_response.content

    # Step 2: Run Book Reporter Agent 
    reporter_agent = Agent(
        name="Book Reporter",
        role="Creates a personalized book recommendation report using the user's preferences and verified research links.",
        model=OpenAIChat(id='o3-mini', api_key=st.session_state.openai_api_key),
        description=dedent("""
            You are a literary assistant specializing in curated book recommendations.
            Your job is to generate a personalized recommendation report using:
            1. A structured summary of the user's reading preferences (genres, tone, favorite books/authors, mood).
            2. A list of URLs pointing to curated book recommendation lists, blog posts, or discovery platforms.

            You must read and analyze the linked sources to extract **real book titles** with summaries and justification.
        """),
        instructions=[
            "Start by reviewing the user's preferences and literary profile.",
            "Then explore the provided URLs.",
            "Extract books that match the user's preferences. You MUST find these in the URLs — do not invent titles or summaries.",
            "For each book, provide: title, author, 1–2 sentence summary, and a reason why it fits the user's taste.",
            "Also include the source site (e.g., Book Riot, Goodreads) and embed the link using markdown format.",
            "Use the following markdown structure EXACTLY for each book:\n"
            "### [Book Title]\n"
            "**Author**: \n"
            "**Summary**: \n"
            "**Why it aligns with your preference**: \n"
            "**Source**: [Site Name](link)\n",
            "The final output should be clean, useful, and tailored to the user’s taste.",
            "Do NOT add an intro or outro text — start directly with '## Book Recommendations'.",
            "Do NOT list more than 12-15 books. Keep it focused and relevant.",
            "Do NOT fabricate book summaries or reasons. Only use what's found in the URLs.",
        ],
        add_datetime_to_instructions=True,
    )

    reporter_input = f"""
    User's Book Preferences:
    {user_book_preferences}

    Research Results:
    {research_results}

    Use these details to generate a book recommendation report.
    """

    reporter_response = reporter_agent.run(reporter_input)
    discoverer_report = reporter_response.content 

    return discoverer_report

def main() -> None:
    # Page config
    st.set_page_config(page_title="Book Discoverer Bot", page_icon="📚", layout="wide")

    # Custom styling
    st.markdown(
        """
        <style>
        .block-container {
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }
        div[data-testid="stTextInput"] {
            max-width: 1200px;
            margin-left: auto;
            margin-right: auto;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Header and intro
    st.markdown("<h1 style='font-size: 2.5rem;'>📚 Book Discoverer Bot</h1>", unsafe_allow_html=True)
    st.markdown(
        "Welcome to Book Discoverer Bot — a Streamlit-powered guide that uncovers compelling reads tailored to your literary tastes, to help you discover stories that truly resonate.",
        unsafe_allow_html=True
    )

    render_sidebar()
    user_book_preferences = render_book_preferences()

    st.markdown("---")

    if st.button("🔍 Generate Book Recommendations"):
        if not hasattr(st.session_state, "openai_api_key"):
            st.error("Please provide your OpenAI API key in the sidebar.")
        elif not hasattr(st.session_state, "serp_api_key"):
            st.error("Please provide your SerpAPI key in the sidebar.")
        else:
            with st.spinner("Discovering books for you ..."):
                discoverer_report = generate_book_recommendations(user_book_preferences)
                st.session_state.discoverer_report = discoverer_report

    if "discoverer_report" in st.session_state:
        st.markdown(st.session_state.discoverer_report, unsafe_allow_html=True)
        st.markdown("---")

        st.download_button(
            label="📥 Download Book Recommendations",
            data=st.session_state.discoverer_report,
            file_name="book_recommendation_report.txt",
            mime="text/plain"
        )

if __name__ == "__main__":
    main()