import json
import re  # New import for robust parsing
from typing import TypedDict, List
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, END
from tools import search_movie_details

load_dotenv()

# 1. Define State
class AgentState(TypedDict):
    user_mood: str
    movie_names: List[str]
    final_recommendations: List[dict]

# 2. Setup Model
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)

# 3. Define Nodes

def curator_node(state: AgentState):
    """Gemini brainstorms 3 movies based on mood."""
    mood = state["user_mood"]
    print(f"\n🤖 CURATOR: Analyzing mood '{mood}'...")
    
    prompt = f"""
    Recommend exactly 3 movies for a user who says: "{mood}".
    Return ONLY a JSON list of strings, like this: ["The Matrix", "Inception", "Interstellar"].
    Do not add any other text or markdown.
    """
    response = llm.invoke(prompt)
    content = response.content
    print(f"🤖 RAW GEMINI OUTPUT: {content}") # Debug print

    # ROBUST PARSING LOGIC
    try:
        # Use Regex to find the list brackets [...] ignoring everything else
        match = re.search(r"\[.*\]", content, re.DOTALL)
        if match:
            json_str = match.group()
            movie_list = json.loads(json_str)
            print(f"✅ PARSED LIST: {movie_list}")
        else:
            print("❌ ERROR: No JSON list found in output.")
            movie_list = []
    except Exception as e:
        print(f"❌ JSON PARSING ERROR: {e}")
        movie_list = []
        
    return {"movie_names": movie_list}

def fetcher_node(state: AgentState):
    """Looks up details/posters for every movie in the list."""
    names = state["movie_names"]
    rich_data = []
    
    print(f"\n🔎 FETCHER: Searching TMDB for {len(names)} movies...")

    for name in names:
        details = search_movie_details(name)
        if details:
            print(f"   Found: {name}")
            rich_data.append(details)
        else:
            print(f"   ⚠️ Could not find details for: {name}")
            
    return {"final_recommendations": rich_data}

# 4. Build Graph
workflow = StateGraph(AgentState)
workflow.add_node("curator", curator_node)
workflow.add_node("fetcher", fetcher_node)

workflow.set_entry_point("curator")
workflow.add_edge("curator", "fetcher")
workflow.add_edge("fetcher", END)

graph = workflow.compile()