from agent.smartstudy_agent import run_agent


question = "Give me study tips for DFS."

print("\n========== GROQ ==========")
print(run_agent(question, provider="groq"))

print("\n========== OLLAMA ==========")
print(run_agent(question, provider="ollama"))
