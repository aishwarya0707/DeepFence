import os
import re
from pathlib import Path
import json
import PyPDF2
from autogen import ConversableAgent
import google.generativeai as genai
from dotenv import load_dotenv, find_dotenv
import pyzipper
import ssl
import win32api
import win32con
from diffprivlib.mechanisms import Laplace
import pandas as pd
_ = load_dotenv(find_dotenv())  # Load from .env file if it exists


# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
# GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GOOGLE_API_KEY='AIzaSyA5DSkhNvRQ-2uLhVmkvyF6SPPT_cJkOU4'
GROQ_API_KEY = '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'

generation_config = {
            "temperature":0.9,
            "top_p":1,
            "top_k":0,
            "max_output_tokens":4096
        }
safety_settings = [
{
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
},
{
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
},
{
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
},
{
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
},
]
genai.configure(api_key=GOOGLE_API_KEY)  # This is the correct way

model = genai.GenerativeModel(model_name="gemini-1.5-flash-latest",
                                    generation_config=generation_config,
                                    safety_settings=safety_settings)
if os.path.exists("PatientSummary.txt"):
    os.remove("PatientSummary.txt")

password='Password123'
# LLM Configurations
config_list = [{'model': 'gemini-1.5-flash', 'api_key': GOOGLE_API_KEY, "api_type": "google"}]
groq_config_list = [
    {
        "api_type": "groq",
        "model": "llama3-8b-8192",
        "api_key": GROQ_API_KEY,
        
    }
]
llm_config = {
    "cache_seed": 42,
    "temperature": 0,
    "config_list": config_list,
    "timeout": 120,
}
groq_llm_config = {
    "cache_seed": 42,
    "temperature": 0,
    "config_list": groq_config_list,
    "timeout": 120,
}

user_agent = ConversableAgent(
    name="User_Agent",
    system_message="Return the same message as Input",
    llm_config=llm_config,
    human_input_mode="NEVER",
)

convert_to_zip_agent = ConversableAgent(
    name="Convert_To_Zip_Agent",
    system_message="You should execute function convert_to_zip with the input",
    llm_config=groq_llm_config,
    human_input_mode="NEVER",
)

unzip_file_agent = ConversableAgent(
    name="Unzip_File_Agent",
    system_message="You should execute function unzip_file_agent with the input",
    llm_config=groq_llm_config,
    human_input_mode="NEVER",
)

lock_folder_agent = ConversableAgent(
    name="Lock_Folder_Agent",
    system_message="You should execute function lock_folder with the input",
    llm_config=groq_llm_config,
    human_input_mode="NEVER",
)

unlock_folder_agent = ConversableAgent(
    name="Unlock_Folder_Agent",
    system_message="You should execute function unlock_folder with the input",
    llm_config=groq_llm_config,
    human_input_mode="NEVER",
)

hide_folder_agent = ConversableAgent(
    name="Hide_Folder_Agent",
    system_message="You should execute function hide_folder with the input",
    llm_config=groq_llm_config,
    human_input_mode="NEVER",
)
unhide_folder_agent = ConversableAgent(
    name="Unhide_Folder_Agent",
    system_message="You should execute function unhide_folder with the input",
    llm_config=groq_llm_config,
    human_input_mode="NEVER",
)

differential_privacy_agent = ConversableAgent(
    name="Differential_Privacy_Agent",
    system_message="You should execute function Differential_Privacy with the input",
    llm_config=groq_llm_config,
    human_input_mode="NEVER",
)


source_dir='C:/DataBench/Workspace/slope.expedition@gmail.com/AccountWorkspace/DataFiles/HeartAttackDetection.csv-Classification-Feb06-25-13-58-26.pkl'
zip_path='C:/DataBench/Workspace/slope.expedition@gmail.com/AccountWorkspace/DataFiles/zippedHeartAttackDetection.csv-Classification-Feb06-25-13-58-26.pkl.zip'
folder_path='C:/DataBench/Workspace/slope.expedition@gmail.com/AccountWorkspace/DataFiles/'
password='Password123'

@user_agent.register_for_execution()
@convert_to_zip_agent.register_for_llm(description="You should execute the function")
def convert_to_zip(message:str) -> str:
    usrName = message

    print(message)
    
    try:
        password_bytes = password.encode('utf-8')
    
        with pyzipper.AESZipFile(zip_path, 'w', encryption=pyzipper.WZ_AES) as zipf:
            zipf.setpassword(password_bytes)
            
            if os.path.isdir(source_dir):
                for root, dirs, files in os.walk(source_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, start=source_dir)
                        zipf.write(file_path, arcname=arcname)
            else:
                zipf.write(source_dir, os.path.basename(source_dir))
        

        return {
            "message": f"Created password protected file: {str(zip_path)}",
            "status": "success"
        }

    except Exception as e:
        return {"message": f"Unable to zip file: {str(e)}", "status": "error"}



@user_agent.register_for_execution()
@unzip_file_agent.register_for_llm(description="You should execute the function")
def unzip_file(message:str) -> str:
    usrName = message
   
    password_bytes = password.encode('utf-8')
    
    try:
        os.makedirs(folder_path, exist_ok=True)
        
        with pyzipper.AESZipFile(zip_path) as zipf:
            zipf.setpassword(password_bytes)
            
            zipf.extractall(path=folder_path)
        
        return {
            "message": f"Successfully extracted zip to: {str(folder_path)}",
            "status": "success"
        }
    
    except RuntimeError as e:
        print(f"Error extracting zip file: {e}")
        if "password" in str(e):
            print("Incorrect password or file is corrupted.")
        return {
            "message": f"Created password protected file: {str(folder_path)}",
            "status": "success"
        }

    except Exception as e:
        return {"message": f"Unable to zip file: {str(e)}", "status": "error"}


@user_agent.register_for_execution()
@lock_folder_agent.register_for_llm(description="You should execute the function")
def lock_folder(message:str) -> str:
    usrName = message
    
    try:
        os.system(f'icacls "{folder_path}" /deny Everyone:(D)')      
        return {
            "message": f"Folder Locked: {str(folder_path)}",
            "status": "success"
        }

    except Exception as e:
        return {"message": f"Unable to lock folder: {str(e)}", "status": "error"}

@user_agent.register_for_execution()
@unlock_folder_agent.register_for_llm(description="You should execute the function")
def unlock_folder(message:str) -> str:
    usrName = message
    
    try:
        os.system(f'icacls "{folder_path}" /remove:d Everyone') 
        return {
            "message": f"Folder Unlocked: {str(folder_path)}",
            "status": "success"
        }

    except Exception as e:
        return {"message": f"Unable to lock folder: {str(e)}", "status": "error"}


@user_agent.register_for_execution()
@hide_folder_agent.register_for_llm(description="You should execute the function")
def hide_folder(message:str) -> str:
    usrName = message
    
    
    try:
        win32api.SetFileAttributes(folder_path, win32con.FILE_ATTRIBUTE_HIDDEN)
        return {
            "message": f"Folder Hidden: {str(folder_path)}",
            "status": "success"
        }

    except Exception as e:
        return {"message": f"Unable to hide folder: {str(e)}", "status": "error"}

@user_agent.register_for_execution()
@unhide_folder_agent.register_for_llm(description="You should execute the function")
def unhide_folder(message:str) -> str:
    usrName = message
    
    try:
        attributes = win32api.GetFileAttributes(folder_path)
        if attributes & win32con.FILE_ATTRIBUTE_HIDDEN:
            win32api.SetFileAttributes(folder_path, attributes & ~win32con.FILE_ATTRIBUTE_HIDDEN)
        return {
            "message": f"Folder Unhidden: {str(folder_path)}",
            "status": "success"
        }

    except Exception as e:
        return {"message": f"Unable to Unhide folder: {str(e)}", "status": "error"}

@user_agent.register_for_execution()
@differential_privacy_agent.register_for_llm(description="You should execute the function")
def differential_privacy(message:str) -> str:
    usrName = message
    
    try:

        file_path = "C:/DataBench/Workspace/slope.expedition@gmail.com/AccountWorkspace/DataFiles/HeartAttackDetection.csv"

        df = pd.read_csv(file_path)

        print(df.head())

        true_mean_age = df['Age'].mean()

        epsilon = 0.5  
        sensitivity = (df['Age'].max() - df['Age'].min()) / len(df)

        laplace_mechanism = Laplace(epsilon=epsilon, sensitivity=sensitivity)
        noisy_mean_age = laplace_mechanism.randomise(true_mean_age)

        print(f"True Mean of Age: {true_mean_age}")
        print(f"Noisy Mean of Age (Differentially Private): {noisy_mean_age}")

        return {
            "message": f"Folder Unhidden: {str(folder_path)}",
            "status": "success"
        }

    except Exception as e:
        return {"message": f"Unable to Unhide folder: {str(e)}", "status": "error"}

# Start a sequence of two-agent chats.
# Each element in the list is a dictionary that specifies the arguments
# for the initiate_chat method.

def file_handling(source):
    chat_results = user_agent.initiate_chats(
        [
            {
                "recipient": convert_to_zip_agent,
                "message": source,
                "max_turns": 2,
                "summary_method": "last_msg",
            },
            {
                "recipient": unzip_file_agent,
                "message": source,
                "max_turns": 2,
                "summary_method": "last_msg",
            },
             {
                "recipient": lock_folder_agent,
                "message": source,
                "max_turns": 2,
                "summary_method": "last_msg",
            },
              {
                "recipient": unlock_folder_agent,
                "message": source,
                "max_turns": 2,
                "summary_method": "last_msg",
            },
            {
                "recipient": hide_folder_agent,
                "message": source,
                "max_turns": 2,
                "summary_method": "last_msg",
            },
             {
                "recipient":unhide_folder_agent,
                "message": source,
                "max_turns": 2,
                "summary_method": "last_msg",
            },
             {
                "recipient":differential_privacy_agent,
                "message": source,
                "max_turns": 2,
                "summary_method": "last_msg",
            },

        ]
    )


    return_values = []
    for message in chat_results[0].chat_history:
        if message.get('role') == 'tool' and message.get('tool_responses'):
            for response in message['tool_responses']:
                return_value = response.get('content')
                try:
                    # Try to parse as JSON if it is a JSON string
                    return_value = json.loads(return_value)
                except (TypeError, json.JSONDecodeError):
                    # If not JSON, keep as is
                    pass
                return_values.append(return_value)

    return return_values

file_handling(source_dir)
