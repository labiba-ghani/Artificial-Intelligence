from services.ai_provider import ask_ai


question = "What is Breadth-First Search? Explain in two sentences."

print("\nTesting Groq...")
groq_answer = ask_ai(question, provider="groq")
print(groq_answer)

print("\nTesting Ollama...")
ollama_answer = ask_ai(question, provider="ollama")
print(ollama_answer)
