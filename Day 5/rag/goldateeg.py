import streamlit as st
from langchain.agents import initialize_agent, Tool
from langchain.agents.agent_types import AgentType
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools import DuckDuckGoSearchRun
import google.generativeai as genai

# 🌐 Hardcoded API key setup
GOOGLE_API_KEY = "AIzaSyDnH78k_Sj1y0fziRvS6VKkYe8u0lGsLyw"
genai.configure(api_key=GOOGLE_API_KEY)

# 🤖 Gemini model
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0)

# 🔍 DuckDuckGo search tool
search = DuckDuckGoSearchRun()
tools = [
    Tool(
        name="DuckDuckGo Search",
        func=search.run,
        description="Useful for answering questions about current events or factual queries"
    )
]

# 🧠 LangChain Agent setup
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=False  # 🔇 No verbose logs
)

# 🎨 Streamlit UI
st.set_page_config(page_title="Ask Me Anything 🤖", page_icon="💬")
st.title("💬 Real-Time Q&A Assistant")
st.markdown("Ask me anything about the world 🌍 — news, facts, or recent events!")

# User input
question = st.text_input("🔎 Type your question here:", placeholder="What's the latest news on AI?")

# Ask button
if st.button("Ask"):
    if question.strip() == "":
        st.warning("⚠️ Please enter a valid question.")
    else:
        try:
            with st.spinner("Thinking... 🤔"):
                answer = agent.run(question)
                st.success("✅ Answer:")
                st.write(answer)
        except Exception as e:
            st.error(f"❌ An error occurred: {str(e)}")
