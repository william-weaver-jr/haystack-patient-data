# Haystack Patient Data Agent

An AI agent that helps healthcare professionals query dermatology patient records and look up general medical knowledge using natural language.

Built with [Haystack AI](https://haystack.deepset.ai/), the agent translates plain English questions into SQL queries against a local patient database, and supplements answers with live web search when general medical knowledge is needed.

## Quick Start

**Prerequisites:** Python 3.12+, an OpenAI API key, and a Serper API key.

```bash
# 1. Clone and enter the project
git clone https://github.com/william-weaver-jr/haystack-patient-data.git
cd haystack-patient-data

# 2. Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment variables
cp .env.example .env   # then fill in your keys

# 5. Run the agent
python main.py
```

Expected output: the agent prints a streaming response answering the query defined in `main.py`.

## Installation

### Prerequisites

| Tool | Version |
|------|---------|
| Python | 3.12+ |
| pip | latest |

### Setup

```bash
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the project root with the following variables:

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENAI_API_KEY` | Yes | OpenAI API key — used to power GPT-4o-mini for SQL generation and agent reasoning |
| `SERPERDEV_API_KEY` | Yes | Serper API key — used for real-time web search |

```bash
OPENAI_API_KEY=sk-...
SERPERDEV_API_KEY=...
```

## Usage

### Running the agent

Edit the `user_query` variable in `main.py` to ask any dermatology-related question, then run:

```bash
python main.py
```

### Example queries

```python
# Patient-specific (queries the local database)
user_query = "What is the most common condition among smoker patients?"
user_query = "Which patients are over 60 and have Psoriasis?"

# General medical knowledge (triggers web search)
user_query = "What are the side effects of isotretinoin?"

# Combined (database + web search)
user_query = "Can all our patients above 40 safely take oral antifungals?"
```

## Project Structure

```
haystack-patient-data/
├── main.py                      # Entry point — set your query here and run
├── agent.py                     # Assembles the Haystack Agent with tools and prompt
├── tools.py                     # Defines the SQL query tool and web search tool
├── prompts.py                   # Prompt templates for the SQL generator and agent
├── database.py                  # Loads CSV data into SQLite; SQLConnector component
├── dermatology_patient_data.csv # Source patient dataset (synthetic)
├── requirements.txt             # Python dependencies
└── .env                         # API keys (not committed)
```

## Architecture

The agent follows a two-tool design:

1. **`get_patient_information`** — accepts a natural language query, uses GPT-4o-mini to generate SQL, runs it against a local SQLite database, and returns the result.
2. **`web_search_tool`** — performs a real-time web search via Serper for general medical knowledge not tied to specific patients.

At runtime, the agent decides which tool (or combination of tools) to use based on the question, then synthesizes a final response.

```
User query
    └── Agent (GPT-4o-mini)
            ├── get_patient_information
            │       └── SQL Pipeline (GPT-4o-mini → SQLConnector → patient_data.db)
            └── web_search_tool
                    └── SerperDev Web Search
```

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| `KeyError` on `OPENAI_API_KEY` | `.env` not loaded or missing | Ensure `.env` exists at project root and `load_dotenv()` runs before imports |
| `No SQL code found.` in results | LLM returned SQL without code fences | Check the `query_to_sql_prompt` in `prompts.py` |
| `OperationalError: no such table: patients` | `setup_database()` not called before agent run | Ensure `setup_database()` runs in `main.py` before `agent.run()` |
| Empty web search results | Invalid or exhausted Serper API key | Verify `SERPERDEV_API_KEY` in `.env` |

## License

<!-- TODO: Add a LICENSE file and reference it here -->
