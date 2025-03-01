# AI Pen Testing Assistant

## Overview
This is an advanced AI-powered assistant designed to streamline penetration testing. Built on top of Mistral-7B, it has been jailbroken, trained on extensive dataset of sucessful pen tests, and fine-tuned with command sets of Kali Linux tools. This AI provides automated command execution and guidance to facilitate in-depth security assessments. Tools used include nmap, metasploit, john the ripper, wireshark, hydra, burpsuite, sqlmap, and more!

---

## Getting Started

### Requirements
- **Operating System**: Kali Linux
- **Python**: Version 3.x
- **Install Required Python Libraries**: Found in requirement.txt
- **Attention**: Download the file in the ATTENTION.md file and add it as AI-pen-testing/Pentest_LLM.guff
- **Download the Model**: [Model](https://huggingface.co/TianZun/AI-pen-testing)
- **Configure the Model Path**: Update the `model_path` variable in the script to match the downloaded model’s location.

---

## Usage

### Running the AI
Execute the script and follow the prompts to begin penetration testing.
```bash
python AI-pen-testing.py
```

### Required Tools
First it verifies the availability of essential penetration testing tools and installs missing ones:
```python
def check_and_install_tools(tools):
    for tool in tools:
        result = subprocess.run(['which', tool], stdout=subprocess.PIPE)
        if not result.stdout.strip():
            subprocess.run(['sudo', 'apt-get', 'install', '-y', tool])
```

### Model Initialization
The script loads the the model and configures its execution environment:
```python
from transformers import AutoTokenizer, AutoModelForCausalLM

tokenizer = AutoTokenizer.from_pretrained("FILEPATH")
model_path = "<path_to_model>"
model = AutoModelForCausalLM.from_pretrained(model_path, gpu_layers=12, threads=1)
```

### Interactive User Interface
```python
sys_env = input("Select your environment (1, 2, or 3): ")
if sys_env == '1':
    check_and_install_tools(pentest_tools)
```

### Automated Command Execution
This AI can recognize commands and execute them directly. This function parses the assistant’s output, detects relevant penetration testing commands, and executes them dynamically:
```python
def execute_tool_command(output, ip_address):
    if 'nmap' in output:
        command_output = os.popen(f'nmap -sV {ip_address}').read()
        print(command_output)
```
