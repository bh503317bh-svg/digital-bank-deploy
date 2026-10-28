# Local demo and AI assistant

Start Docker Desktop, copy `.env.example` to `.env`, and set `DEEPSEEK_API_KEY` to your DeepSeek API key. The `.env` file is ignored by Git and should stay private. Then run:

```sh
./scripts/run-local.sh
```

Open http://127.0.0.1:18088/. The script builds from a temporary copy under `/tmp/digital-bank-local` so Docker can handle source paths with non-ASCII characters. It binds the demo to localhost, without the deployment's external network. Run the script again after changing source code. The database is stored in the Docker volume `digital-bank_mysql_data`.

The assistant streams DeepSeek responses through the authenticated backend, using `deepseek-v4-pro` by default. It offers relevant app and product links after the response, but cannot read account information or execute transactions. Users must review any transaction in the existing app flow. Interrupted responses display an error and can be retried.

The microphone button is a scripted demo: it shows a waveform for about 1.7 seconds and inserts a fixed English portfolio request into the input. It does not record audio or send the message automatically. Conversation is held in browser memory until the page reloads.
