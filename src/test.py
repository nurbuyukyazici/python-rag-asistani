from foundry_local_sdk import Configuration, FoundryLocalManager

config = Configuration(app_name="rag_projesi")
FoundryLocalManager.initialize(config)
manager = FoundryLocalManager.instance

model = manager.catalog.get_model("qwen3-0.6b")
model.download()
model.load()

client = model.get_chat_client()
response = client.complete_chat([
    {"role": "user", "content": "Merhaba, sen kimsin?"}
])

print("Model cevabı:", response.choices[0].message.content)

model.unload()