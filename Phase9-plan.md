# Phase 9 — AI Integration (tutorial)

Phases 7–8 are skipped. You execute the **current** `Prompt.content` row. No users, no prompt versions.

Work **one slice at a time**. Do not start 9.3 until 9.2 returns a reply. Same rules as Phase 6: `Router → Service → Repository`. The model is **not** SQL — add a small LLM client, not a method on `prompt_repository`.

---

## Map

| # | Slice | In plain terms | Wait on |
|---|---|---|---|
| 9.1 | Ollama | Model on your laptop; prove it talks | — |
| 9.2 | Execute | Saved prompt → model → reply JSON | history, stream |
| 9.3 | History | Save each run | — |
| 9.4 | Model | Pick which model without editing code | — |
| 9.5 | Tokens | Count in/out units | $ cost (Ollama ≈ 0) |
| 9.6 | Stream | Reply appears word by word | don’t block 9.2 |
| 9.7 | Embeddings | Text → list of numbers | **Phase 10** if unsure |

---

## Ground rules (whole phase)

**WHAT**  
Talk to a chat model through HTTP. Ollama speaks the **OpenAI-compatible** shape (`POST /v1/chat/completions`). One client. Later you only change `base_url` + key to hit hosted OpenAI.

**HOW**

```
prompt_id
  → load Prompt (404 if missing)
  → POST Ollama: messages=[{ role: user, content: Prompt.content }]
  → JSON: output text (+ usage)
  → (9.3+) INSERT executions
```

- `.env`: `OLLAMA_BASE_URL=http://localhost:11434/v1` · `OLLAMA_MODEL=llama3.2`
- Missing prompt → 404 `PROMPT_NOT_FOUND` (you already have this).
- Ollama down → 503 `SERVICE_UNAVAILABLE` + `error_body` (same idea as `/health`).
- Do **not** write the model reply onto `prompts.content`.

**Out of scope:** auth, per-user history, versions, RAG, billing, Dockerizing Ollama.

---

## 9.1 Ollama

**WHAT**  
Install a local model runner. Pull **one** small model. Confirm *something* answers before you write FastAPI code.

**HOW**

1. Install Ollama (app or brew). Start it.
2. `ollama pull llama3.2` (or another small tag).
3. Smoke test outside the API, e.g. `ollama run llama3.2 "Say hi in one sentence."`
4. Optional: `curl http://localhost:11434/v1/models` — OpenAI-compat list.

**Check:** the CLI prints a reply. If this fails, 9.2 will only produce 503s.

---

## 9.2 Execute

**WHAT**  
A client picks a prompt **id**. Your API loads that row, sends `content` to Ollama, returns the assistant text. Pagination/filter/sort stay untouched.

**HOW**

1. Settings: `ollama_base_url`, `ollama_model` (and later `ollama_api_key` default empty).
2. New module e.g. `app/llm/ollama_client.py` — HTTP POST chat completions. **Not** in the repository.
3. Service: `get_prompt` (reuse 404) → client → map response.
4. Router: `POST /api/v1/prompts/{prompt_id}/execute` on the **existing** prompts router (path must be registered **before** `/{prompt_id}` only if FastAPI could confuse them — `execute` is a suffix, so `/{prompt_id}/execute` is fine).

```
IN:  path prompt_id · body? { temperature? }
OUT: 200 {
       prompt_id, model,
       output,
       usage: { prompt_tokens, completion_tokens }
     }
```

If Ollama’s `usage` is missing, send `null`s — don’t fake numbers. Don’t persist yet.

**Check:** `POST /api/v1/prompts/{id}/execute` → 200 + `output` string. Bad id → 404. Stop Ollama → 503.

---

## 9.3 History

**WHAT**  
Each run becomes a row. The prompt can change tomorrow; the row still shows **what was sent that day**.

**HOW**

1. Model `Execution` + Alembic migration. Table `executions`:
   `id · prompt_id FK · model · input_snapshot · output · prompt_tokens · completion_tokens · created_at`
2. `input_snapshot` = `Prompt.content` at execute time.
3. Repository for executions only (create + list by `prompt_id`). Service calls it **after** a successful LLM response.
4. `GET /api/v1/prompts/{id}/executions` — same envelope as prompt list: `{ items, total, limit, offset }`.

Failed LLM calls: **no row** (or a later `status=error` column — skip for v1).

**Check:** execute twice → two rows; `GET .../executions` lists them; edit the prompt, old rows still have the old snapshot.

---

## 9.4 Model

**WHAT**  
Caller can choose a model name. Default stays in Settings so local curl still works with no body.

**HOW**

```
IN:  body.model  OR  Settings.ollama_model
OUT: echo `model` on execute JSON + on the history row
```

Pass the string through to Ollama. Unknown model → Ollama errors → you map to 502/503 + `error_body`. Allowlist only if you actually need it.

**Check:** omit `model` → default. Send `model: "..."` → that name appears in the response and in `executions`.

---

## 9.5 Tokens

**WHAT**  
Tokens ≈ how much text went in and came out. You store the provider’s counts. You do **not** invent a dollar amount on Ollama.

**HOW**

Read `usage` from the chat-completions JSON. Write the two ints onto:

- execute `OUT.usage`
- `executions.prompt_tokens` / `completion_tokens`

`cost_usd`: skip, or always `null`.

**Check:** after execute, usage ints are present (or explicit nulls). History row matches the response.

---

## 9.6 Stream

**WHAT**  
Non-stream 9.2 stays. Streaming is a **second** way to watch the same job: tokens arrive as they are generated.

**HOW**

```
POST /api/v1/prompts/{id}/execute/stream
IN:  same as 9.2
OUT: SSE (or chunked) text deltas → last event = usage
```

Do not insert history until the stream **finishes** successfully. Don’t replace 9.2 with stream-only.

**Check:** 9.2 still JSON. Stream prints increasing text. Kill Ollama mid-stream → error, no partial history row (or document if you choose otherwise).

---

## 9.7 Embeddings

**WHAT**  
Turn a string into a vector (list of floats). Useful later for “find similar prompts.” A vector **database** is Phase 10.

**HOW** (only if you still want it here)

```
POST /api/v1/embeddings
IN:  { text }  OR  { prompt_id }
OUT: { model, embedding: number[] }
```

Ollama embeddings endpoint (or `/v1/embeddings` if enabled). No pgvector, no search.

**Prefer:** skip this slice and do it with RAG in Phase 10.

---

## Phase done when

`POST /api/v1/prompts/{id}/execute` returns Ollama text, 404/503 as above, and (after 9.3) a matching `executions` row.

Start at **9.1**. When Ollama replies in the CLI, ask for the 9.2 implementation steps (same WHY/HOW style as Phase 6).
