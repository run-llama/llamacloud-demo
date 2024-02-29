# LlamaCloud Demo

## Getting Started

1. Grab an [OpenAI API key](https://platform.openai.com/api-keys) and set it as an environment variable e.g. `export OPENAI_API_KEY=sk-xxx`
1. Follow the instructions in the section below for setting up the Jupyter Environment.
1. Go to [https://cloud.llamaindex.ai/](https://cloud.llamaindex.ai/) and create an account using one of the authentication providers.
1. Once logged in, go to [the API Key page](https://cloud.llamaindex.ai/api-key) and create an API key. Copy that generated API key to your clipboard.
1. Open one of the Jupyter notebooks in this repo (`demo.ipynb` or `demo_sec.ipynb`) and paste the API key into the first cell block that reads `os.environ["PLATFORM_API_KEY"] = "..."`
1. Execute the cells in the notebook until you get to the cell that registers the pipeline with LlamaCloud
    * e.g. `pg_pipeline_id = pg_pipeline.register()`

That should get you started! From there you can go to the playground section of [the LlamaCloud website](https://cloud.llamaindex.ai/) and start experimenting with your pipeline.

### Setting up the Jupyter Environment
Here's some commands for installing the Python dependencies & running Jupyter.
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
jupyter lab
```
