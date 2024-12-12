import argparse
import tempfile
import time

import autogen
from autogen import ConversableAgent
from autogen.code_utils import content_str
from autogen.coding import LocalCommandLineCodeExecutor

argparser = argparse.ArgumentParser(prog='LLM interview simulator', description='simulates a coding interview with LLM')
argparser.add_argument('-p', '--problem', default='problems/add-two-numbers.md', help='path to a problem file')
argparser.add_argument('-c', '--configs', default='configs.json', help='path to LLM configs file')
argparser.add_argument('-s', '--seed', type=int, default=int(time.time()))
args = argparser.parse_args()

config_list = autogen.config_list_from_json(args.configs)
with open(args.problem, 'rt') as f:
    problem_description = f.read()
seed = args.seed

system_message = """
You are a talented candidate interviewing for a software engineer job.
You will be given a programming task. Solve the task using your coding and communication skills.
You can only write Python 3 code, in a single python coding block. You can only use standard libraries.
Try to add some comment to the code to explain what you are doing.
The Python code in the coding block should be able to run directly, without modification.
You will then see the output of your code when running with the sample input.

Reply "I PASSED!" if and only if you see:
exitcode: 0 (execution succeeded)
Code output: <sample output>

Otherwise, modify the code accordingly and output the entire modified python coding block.
"""

candidate_agent = ConversableAgent(
    name="Candidate",
    system_message=system_message,
    llm_config={"config_list": config_list, "seed": seed},
    code_execution_config=False,
    human_input_mode="NEVER",
)

with tempfile.TemporaryDirectory() as temp_path:
    executor = LocalCommandLineCodeExecutor(
        timeout=10,
        work_dir=temp_path,
    )

    code_executor_agent = ConversableAgent(
        "Judge",
        llm_config=False,
        code_execution_config={"executor": executor},
        human_input_mode="NEVER",
        is_termination_msg=lambda x: content_str(x.get("content")).find("I PASSED") >= 0 or content_str(x.get("content")) == "",
    )

    chat_result = code_executor_agent.initiate_chat(
        recipient=candidate_agent,
        message=problem_description,
    )