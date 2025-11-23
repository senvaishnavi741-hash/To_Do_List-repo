# Import necessary libraries
import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

# Simple function to generate a skill roadmap
def generate_roadmap(goal):
    # Example of skills related to the goal
    skills = {
        'Python': ['Data Analysis', 'Machine Learning'],
        'Data Analysis': ['Pandas', 'NumPy'],
        'Machine Learning': ['Scikit-learn', 'TensorFlow'],
    }

    G = nx.DiGraph()

    # Add nodes (skills) and edges (dependencies)
    for skill, dependencies in skills.items():
        for dependency in dependencies:
            G.add_edge(skill, dependency)

    return G

# Streamlit UI
st.title("PathPilot: Learning Roadmap Generator")

# Input box for user goal
goal = st.text_input("Enter your goal", "Become a Data Scientist")

# When goal is provided, generate and show roadmap
if goal:
    st.write(f"Goal: {goal}")
    roadmap = generate_roadmap(goal)

    # Draw the roadmap using matplotlib
    pos = nx.spring_layout(roadmap)
    plt.figure(figsize=(8, 6))
    nx.draw(roadmap, pos, with_labels=True, node_size=3000, node_color="skyblue", font_size=12, font_weight="bold")
    st.pyplot(plt)