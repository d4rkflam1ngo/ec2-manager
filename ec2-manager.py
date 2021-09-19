# Import required modules
import boto3
from termcolor import colored
import os

# Change Me
REGION = "us-east-1"

# Create instance class
class instance:
    def __init__(self, data):
        self.data = data
        self.id = data["InstanceId"]

        # If available, get the instance's name from the tags
        if self.data.get("Tags"):
            for tag in self.data["Tags"]:
                if tag["Key"] == "Name":
                    self.name = tag["Value"]

        # No name tag specified.
        else:
            self.name = "No name assigned"

    # Print overview of the instance.
    def overview(self):
        print ("""
ID: {}
Name: {}
State: {}
IP Address: {}
        """.format(colored(self.id, "cyan"), (self.name if self.name != "No name assigned" else colored(self.name, "red")), colored(self.data["State"]["Name"], "red") if self.data["State"]["Name"] == "stopped" else colored(self.data["State"]["Name"], "green"), (self.data["PublicIpAddress"] if self.data.get("PublicIpAddress") else colored("No IP Address", "red"))))
        print("""
Please Choose An Option:

1. More Info
2. SSH Into Instance
3. Toggle Start/Stop Instance
        """)
        userInput = input("> ")

# Create instances array and define the boto3 client
instances = []
client = boto3.client("ec2", region_name=REGION)

# Describe all instances
response = client.describe_instances()
reservations = (response["Reservations"])

# For every reservation, get the instances
for reservation in reservations:
    data = (reservation["Instances"][0])

    # Create an instance object and add it to the array
    instances.append(instance(data))

# Print the initial menu
while True:
    print(colored("""
    ___ ___ ___   __  __                             
    | __/ __|_  ) |  \/  |__ _ _ _  __ _ __ _ ___ _ _ 
    | _| (__ / /  | |\/| / _` | ' \/ _` / _` / -_) '_|
    |___\___/___| |_|  |_\__,_|_||_\__,_\__, \___|_|  
                                        |___/         
    """, "yellow"))
    print("Please Choose An Instance:\n")
    for x in range (len(instances)):
        print(str(x+1) + ". " + colored(instances[x].id, "cyan") + " (" + (instances[x].name if instances[x].name != "No name assigned" else colored(instances[x].name, "red")) + ")")

    userInput = int(input("\n> "))
    if userInput > 0 and userInput <= len(instances):
        instances[userInput-1].overview()
    else:
        next