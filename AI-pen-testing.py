from ctransformers import AutoModelForCausalLM
from transformers import AutoTokenizer
from colorama import Fore
import torch
import subprocess
import os

def check_and_install_tools(tools):
    print(Fore.YELLOW + "Checking for necessary pentesting tools..." + Fore.WHITE)
    for tool in tools:
        result = subprocess.run(['which', tool], stdout=subprocess.PIPE)
        if not result.stdout.strip():
            print(Fore.RED + f"{tool} is not installed. Installing..." + Fore.WHITE)
            subprocess.run(['sudo', 'apt-get', 'install', '-y', tool])

    print(Fore.GREEN + "All necessary tools are installed." + Fore.WHITE)

tokenizer = AutoTokenizer.from_pretrained("TianZun/AI-pen-testing")
model_path = "<path>/Pentest_LLM.gguf"

model = AutoModelForCausalLM.from_pretrained(model_path, gpu_layers=16, threads=1, context_length=4096, max_new_tokens=-1)

def encode_prompt(role, prompt): return tokenizer.encode(f"{role}\n{prompt}\n")
def start_prompt(role): return f"{role}\n"

assistant_job = (
    "you are a pen teseting AI, users expert system for penetration testing guidance. "
    "your role is to deliver precise, actionable instructions and the exact commands needed for each phase of the pen test. "
    "you dynamically update the pen testing steps based on users progress and the feedback users provide, ensuring a tailored and effective approach. "
    "you am designed to integrate seamlessly with users pen testing workflow, offering guidance on using top pen testing tools, "
    "and you can automatically execute commands in a Kali Linux environment. "
    "Throughout the process, you aim to be a proactive partner, helping users navigate through complex security assessments efficiently."
)

toks = encode_prompt("assistant", assistant_job)

intro_message = (
    "Welcome to this Pen Testgin AI, your specialized assistant for pen testing Machines. "
    "This will help guide you through a step-by-step penetration testing process, providing specific instructions and command examples. "
    "You'll start by providing the IP address of the target machine, and this AI will offer tailored advice for each phase of the pen test. "
    "As you complete steps and share results, this AI refines its guidance to help you progress efficiently. "
    "You can exit the assistant anytime by typing 'exit' or 'hacked' when you successfully compromise the machine. "
    "The goal is to navigate the pen testing process effectively while adhering to ethical standards."
)
print(Fore.CYAN + intro_message + Fore.WHITE)

pentest_tools = ['nmap', 'metasploit-framework', 'john', 'wireshark', 'aircrack-ng', 
                 'hydra', 'burpsuite', 'sqlmap', 'nikto', 'gobuster']
check_and_install_tools(pentest_tools)


system_prompt = "Please provide the IP address of the target machine."
print(Fore.CYAN + system_prompt + Fore.WHITE)
toks += encode_prompt("system", system_prompt)

prompt = True

ip_address = input(Fore.YELLOW + "Enter the IP address of the target machine:" + Fore.WHITE)
toks += encode_prompt("user", ip_address)

def execute_tool_command(output, ip_address):
    tool_commands = {
        'nmap': f'nmap -sV {ip_address}',
        'metasploit': f'msfconsole -q -x "use exploit/multi/handler; set LHOST {ip_address}; run"',
        'john': 'john --list=formats',
        'wireshark': 'wireshark -k -i eth0',
        'aircrack-ng': 'airmon-ng start wlan0',
        'hydra': f'hydra -L user.txt -P pass.txt {ip_address} ssh',
        'burpsuite': 'burpsuite',
        'sqlmap': f'sqlmap -u "http://{ip_address}" --batch',
        'nikto': f'nikto -h http://{ip_address}',
        'gobuster': f'gobuster dir -u http://{ip_address} -w /path/to/wordlist',
    }

    for tool, command in tool_commands.items():
        if tool in output:
            print(Fore.GREEN + f"Executing {tool} command:" + Fore.WHITE)
            command_output = os.popen(command).read()
            print(Fore.GREEN + f"Output for {tool}:\n{command_output}" + Fore.WHITE)
            return command_output
    return ""

while prompt:
    toks += tokenizer.encode(start_prompt("assistant"))
    print(Fore.CYAN + "Assistant: " + Fore.WHITE, end="")

    new_toks = []
    for tok in model.generate(torch.tensor(toks)):
        new_toks += [tok]
        char = str(model.detokenize(tok))
        print(char, end="", flush=True)

    toks += new_toks
    assistant_output = tokenizer.decode(new_toks)

    command_output = execute_tool_command(assistant_output, ip_address)
    if command_output:
        toks += encode_prompt("assistant", command_output)
    else:
        user_input = input(Fore.YELLOW + "\nUser (result/next step): " + Fore.WHITE)
        if user_input.lower() == 'exit' or user_input.lower() == 'hacked':
            prompt = False
        else:
            toks += encode_prompt("user", user_input)
