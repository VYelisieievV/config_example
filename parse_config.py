import argparse
import re
import logging
import os
import yaml

logging.basicConfig(
    format="%(levelname)s - %(asctime)s - %(module)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger()


def load_yaml_config(file_path):
    try:
        with open(file_path, "r") as file:
            config_data = yaml.safe_load(file)
        return config_data
    except FileNotFoundError:
        logger.error(f"Config file not found: {file_path}")
        return None
    except yaml.YAMLError as e:
        logger.error(f"Error loading YAML config: {e}")
        return None


def replace_variables_in_file(input_path, output_path, config_data):
    try:
        with open(input_path, "r") as file:
            file_content = file.read()

        # Define a regular expression pattern to match ${var}
        pattern = r"\$\{(.*?)\}"

        # Define a callback function for the replacement
        def replace_callback(match):
            key = match.group(1)
            if key in config_data:
                return str(config_data[key])
            else:
                logger.warning(f"Key' {key}' not found in the YAML config.")
                user_input = input(f"Please enter a value for '{key}': ")
                config_data[key] = user_input
                return user_input

        # Use the re.sub function with the callback function to replace matches
        updated_content = re.sub(pattern, replace_callback, file_content)

        # Ensure the output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Write the updated content to the output file
        with open(output_path, "w") as output_file:
            output_file.write(updated_content)

        logger.info("Replacement completed. Updated content saved to: %s", output_path)
    except Exception as e:
        logger.error(f"Error replacing variables in file: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Replace variables in a text file using values from a YAML config."
    )
    parser.add_argument("--config", help="Path to the YAML config file")
    parser.add_argument("--input_path", help="Path to the input text file")
    parser.add_argument("--output_path", help="Path to the output text file")

    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)

    config_data = load_yaml_config(args.config)

    if config_data is not None:
        replace_variables_in_file(args.input_path, args.output_path, config_data)
