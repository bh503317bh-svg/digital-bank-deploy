# Local demo and AI assistant

Start Docker Desktop, copy `.env.example` to `.env`, and set `DEEPSEEK_API_KEY` to your DeepSeek API key. The `.env` file is ignored by Git and should stay private. Then run:

```sh
./scripts/run-local.sh
```

Open http://127.0.0.1:18088/. The script builds from a temporary copy under `/tmp/digital-bank-local` so Docker can handle source paths with non-ASCII characters. It binds the demo to localhost, without the deployment's external network. Run the script again after changing source code. The database is stored in the Docker volume `digital-bank_mysql_data`.

The assistant sends the conversation to DeepSeek through the authenticated backend, using `deepseek-v4-pro` by default. It offers relevant app and product links, but cannot read account information or execute transactions. Users must review any transaction in the existing app flow. If DeepSeek returns an empty or invalid structured response, the backend retries using plain text and offers relevant links when it can identify them from the conversation.

For English voice input, tap the microphone, speak, and tap again to stop. Review or edit the recognized text before sending. This uses the browser's speech recognition service, not DeepSeek; availability, microphone permissions, and whether audio is sent to a recognition provider depend on the browser. Text works without speech support. Conversation is held in browser memory until the page reloads.
