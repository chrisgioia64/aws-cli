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

def get_reservations(data, state : str = "all", **kwargs):
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
                    "PublicIpAddress": instances.get("PublicIpAddress", " "),
                    "State" : instances['State']['Name'],
            }
            current_state = instances['State']['Name']
            if state == "all" or current_state == state:
                output.append(instance_info)
    return output

def print_output(data, output_format, **kwargs):
    if output_format == "json":
        print(json.dumps(data, indent=4))
    elif output_format == "list":
        print(f"{'Name':<20} {'InstanceType':<15} {'PublicIpAddress':<20} {'State':<10}")
        print("-" * 85)
        for instance in data:
            print(f"{instance['Name']:<20} {instance['InstanceType']:<15} {instance['PublicIpAddress']:<20} {instance['State']:<10}")

if __name__ == "__main__":
    response = run_aws_describe_instances()
    
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--state", default="all", help="Filter instances by state")
    argparser.add_argument("--data", default=response)
    argparser.add_argument("--output-format", default="json", help="Output format")
    args = argparser.parse_args()
    output = get_reservations(**vars(args))
    print_output(data=output, output_format=args.output_format)

# s1 = {'a': 1, 'b': 2, 'c': 3}
# print(s1.get('x', None))