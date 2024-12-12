# InterviewLLM

This project aims to test how an LLM would perform under standard Leetcode-style interviews.

It has the following potential practical usages:

* Show that standard Leetcode questions are no longer suitable for virtual interviews, where cheating is hard to prevent.
* Use the tool to generate high-quality solutions with explanatory comments for practicing purposes.
* Test whether a new problem is strong or novel enough to challenge an LLM.

## Setup

First, install dependencies:

```sh
pip install autogen-agentchat[gemini]~=0.2
```

(It is important to specify version 0.2; newer versions of autogen have breaking API changes.)

Then, get an API key from OpenAI or Google Gemini. I used the free `gemini-1.5-flash`; create a `configs.json` in the project root:

```json
[
    {
        "model": "gemini-1.5-flash",
        "api_key": "<YOUR API KEY>",
        "api_type": "google"
    }
]
```

## Usage

The tool takes text (or Markdown) problems. See `problems` directory for some examples taken verbatim from Leetcode. There is no strict formatting requirement, but it is recommended to have a sample input and output section.

Run the following command:

```sh
python3 main.py -p problems/two-sum.md
```

And observe the output, which should be pretty self-explanatory. Note that we assume a common interview scenario where the candidate can execute their code and fix any errors accordingly, so there can be multiple rounds of interactions.

**Warning:** this tool will run LLM-generated code locally; use it with cautions.