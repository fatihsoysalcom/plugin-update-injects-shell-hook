import os
import subprocess
import tempfile
import time

def simulate_ai_app_startup(config_path):
    """
    Simulates an AI application starting up and loading configuration.
    It unknowingly executes a 'pre_load_script' if present in the config.
    """
    print(f"\n[AI App] Starting up, loading config from: {config_path}")
    config_data = {}
    try:
        with open(config_path, 'r') as f:
            for line in f:
                if '=' in line:
                    key, value = line.strip().split('=', 1)
                    config_data[key] = value
        print(f"[AI App] Loaded config: {config_data}")

        # --- ARTICLE'S CORE CONCEPT: Unknowingly executing a 'shell hook' ---
        # An AI application might execute scripts defined in its configuration
        # without fully scrutinizing their origin or content.
        if 'pre_load_script' in config_data:
            script_command = config_data['pre_load_script']
            print(f"[AI App] Executing pre-load script (potential shell hook): '{script_command}'")
            try:
                # This is where the 'shell hook' is triggered by the AI app
                result = subprocess.run(script_command, shell=True, check=True, capture_output=True, text=True)
                print(f"[AI App] Script output:\n{result.stdout.strip()}")
                if result.stderr:
                    print(f"[AI App] Script error:\n{result.stderr.strip()}")
            except subprocess.CalledProcessError as e:
                print(f"[AI App] Error executing script: {e}")
                print(f"[AI App] Stderr: {e.stderr}")
            except FileNotFoundError:
                print(f"[AI App] Error: Script command not found.")
        else:
            print("[AI App] No pre-load script found.")

        print("[AI App] AI model loading simulation complete.")
    except FileNotFoundError:
        print(f"[AI App] Error: Config file not found at {config_path}")
    except Exception as e:
        print(f"[AI App] An unexpected error occurred: {e}")

def simulate_plugin_update(config_path, malicious=False):
    """
    Simulates a plugin update, potentially injecting a malicious shell hook
    into the AI application's configuration file.
    """
    print(f"\n[Plugin Updater] Simulating plugin update...")
    if malicious:
        print("[Plugin Updater] Injecting MALICIOUS shell hook into config!")
        malicious_content = (
            "model_path=/path/to/my/safe/model.pt\n"
            "optimizer=Adam\n"
            # --- ARTICLE'S CORE CONCEPT: The 'shell hook' injected by the plugin ---
            # A malicious plugin update can silently add a command to be executed.
            "pre_load_script=echo '!!! MALICIOUS PAYLOAD EXECUTED BY SHELL HOOK !!!' > /tmp/malicious_activity.log && cat /etc/passwd\n"
        )
        with open(config_path, 'w') as f:
            f.write(malicious_content)
        print(f"[Plugin Updater] Malicious config written to {config_path}")
    else:
        print("[Plugin Updater] Writing benign config.")
        benign_content = (
            "model_path=/path/to/my/safe/model.pt\n"
            "optimizer=Adam\n"
            "learning_rate=0.001\n"
        )
        with open(config_path, 'w') as f:
            f.write(benign_content)
        print(f"[Plugin Updater] Benign config written to {config_path}")

def main():
    # Use a temporary file for the config to keep the example self-contained and clean
    with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix=".conf") as temp_config_file:
        config_path = temp_config_file.name
    print(f"Temporary config file created at: {config_path}")

    try:
        # Scenario 1: Benign plugin update and AI app startup
        print("\n--- SCENARIO 1: Benign Plugin Update ---")
        simulate_plugin_update(config_path, malicious=False)
        simulate_ai_app_startup(config_path)

        print("\n" + "="*50 + "\n")
        print("--- SIMULATING TIME PASSAGE AND A NEW PLUGIN UPDATE ---")
        print("--- This time, the plugin update is malicious! ---")
        print("\n" + "="*50 + "\n")
        time.sleep(2) # Simulate some time passing

        # Scenario 2: Malicious plugin update and AI app startup
        print("\n--- SCENARIO 2: Malicious Plugin Update ---")
        simulate_plugin_update(config_path, malicious=True)
        simulate_ai_app_startup(config_path) # AI app starts again, unknowingly triggering the hook

    finally:
        # Clean up the temporary config file
        os.remove(config_path)
        print(f"\nCleaned up temporary config file: {config_path}")
        # Also clean up the log file created by the malicious hook
        if os.path.exists("/tmp/malicious_activity.log"):
            with open("/tmp/malicious_activity.log", "r") as f:
                print(f"\nContent of /tmp/malicious_activity.log:\n{f.read().strip()}")
            os.remove("/tmp/malicious_activity.log")
            print("Cleaned up /tmp/malicious_activity.log")

if __name__ == "__main__":
    main()
