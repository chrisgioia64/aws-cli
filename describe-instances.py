import json
import argparse

import subprocess
import json

JSON_FILE = "data/instances.json"

def run_aws_cli(command):
    """Run an AWS CLI command and return the output as JSON."""
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return json.loads(result.stdout)  # Convert JSON output to a dictionary
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return None

def run_aws_describe_instances():
    command = ["aws", "ec2", "describe-instances", "--output", "json"]
    response = run_aws_cli(command)
    if response is not None:
        print("Successfully ran the AWS EC2 describe-instances command.")
    return response

def get_reservations(data, state : str = "all"):
    # with open(JSON_FILE, 'r', encoding='utf-16') as f:
    #     data = json.load(f)
    output = []
    reservations = data['Reservations']
    for reservation in reservations:
        for instances in reservation['Instances']:
            name = ""
            for tag in instances['Tags']:
                if tag['Key'] == 'Name':
                    name = tag['Value']
            instance_info = {
                    "Name": name,
                    # "InstanceId": instances['InstanceId'],
                    # "ImageId": instances['ImageId'],
                    "InstanceType": instances['InstanceType'],
                    "PublicIpAddress": instances.get("PublicIpAddress", None),
                    "State" : instances['State']['Name'],
            }
            current_state = instances['State']['Name']
            if state == "all" or current_state == state:
                output.append(instance_info)
    return output


if __name__ == "__main__":
    response = run_aws_describe_instances()
    
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--state", default="all", help="Filter instances by state")    
    argparser.add_argument("--data", default=response)
    args = argparser.parse_args()
    output = get_reservations(**vars(args))
    print(json.dumps(output, indent=4))