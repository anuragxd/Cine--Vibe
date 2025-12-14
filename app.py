import streamlit as st
from agent_graph import graph

st.set_page_config(page_title="Cine-Vibe", layout="wide")

st.title("🍿 Cine-Vibe Curator")
st.markdown("Describe your mood, and I'll build a visual watchlist for you.")

# Input
mood = st.text_input("How are you feeling?", placeholder="I want a visually stunning sci-fi movie with a plot twist...")

if st.button("Curate Watchlist"):
    if mood:
        with st.spinner("Analyzing vibes & fetching posters..."):
            result = graph.invoke({"user_mood": mood})
            movies = result.get("final_recommendations", [])
            
            if not movies:
                st.error("Couldn't find movies. Try a different mood!")
            else:
                # DISPLAY BEAUTIFULLY
                st.subheader("Your Personal Picks")
                
                # Create 3 columns for the 3 movies
                cols = st.columns(3)
                
                for idx, movie in enumerate(movies):
                    # ... (inside the for loop in app.py) ...

                    with cols[idx]:
                        # Poster Image
                        if movie['poster_url']:
                            st.image(movie['poster_url'], use_container_width=True)
                        
                        # Title & Rating
                        st.subheader(f"{movie['title']}")
                        st.caption(f"📅 {movie['release_date']} | ⭐ {movie['rating']}/10")
                        
                        # --- NEW SECTION: Streaming Info ---
                        if movie['streaming_on']:
                            st.write("📺 **Watch on:**")
                            # Display simple text badges
                            st.markdown(" ".join([f"`{p}`" for p in movie['streaming_on']]))
                        else:
                            st.caption("Not streaming on major platforms right now.")
                        # -----------------------------------
                        
                        # Description inside an expander
                        with st.expander("Read Plot"):
                            st.write(movie['overview'])
                        
                        st.button(f"Add {movie['title']}", key=idx)