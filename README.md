# ⚠️ Important Notice

This repository is deprecated and no longer maintained.

For the latest python examples, please refer to the `llama-cloud-services` repository examples: 
https://github.com/run-llama/llama_cloud_services/tree/main/examples

---

# LlamaCloud Demo

This repository contains a collection of cookbooks to show you how to build LLM applications using LlamaCloud to help manage your data pipelines, and LlamaIndex as the core orchestration framework.

## Getting Started

1. Follow the instructions in the section below for setting up the Jupyter Environment.
1. Go to [https://cloud.llamaindex.ai/](https://cloud.llamaindex.ai/) and create an account using one of the authentication providers.
1. Once logged in, go to [the API Key page](https://cloud.llamaindex.ai/api-key) and create an API key. Copy that generated API key to your clipboard.
1. Go back to LlamaCloud. Create a project and initialize a new index by specifying the data source, data sink, embedding, and optionally transformation parameters. 
1. Open one of the Jupyter notebooks in this repo (e.g. `examples/getting_started.ipynb`) and paste the API key into the first cell block that reads `os.environ["PLATFORM_API_KEY"] = "..."`
1. Copy the `index_name` and `project_name` from the deployed index into the `LlamaCloudIndex` initialization in the notebook.

That should get you started! You should now be able to create an e2e pipeline with a LlamaCloud pipeline as the backend.

## Setting up the Jupyter Environment
Here's some commands for installing the Python dependencies & running Jupyter.
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
jupyter lab
```

Notebooks are in `examples`.

Note: if you encounter package issues when running notebook examples, please `rm -rf .venv` and repeat the above steps again.
