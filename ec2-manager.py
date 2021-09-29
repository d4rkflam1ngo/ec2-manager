# Import required modules
import boto3
from termcolor import colored
import os
from pprint import pprint
import subprocess

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

    # SSH into the instance
    def ssh(self):

        # Prompt for the username
        print("\nPlease enter the user to SSH into:")
        user = input("\n> ")

        # Prompt for the pem/key file
        print("\n\nEnter the full path to key file:")
        keyPath = input("\n> ")

        # Create command to execute
        command = "ssh -i {} {}@{}".format(keyPath, user, self.data["PublicIpAddress"])

        # Execute the command, passing in the current environment variables
        subprocess.Popen(command, shell=True, env=os.environ)

    # Toggle the instance's state
    def toggleState(self):

        # If the instance is currently stopped
        if self.data["State"]["Name"] == "stopped":
            print("Starting instance {}".format(self.id))

            # Start the instance
            client.start_instances(InstanceIds=[self.id])

        else:
            print("Stopping instance {}".format(self.id))

            # Stop the instance
            client.stop_instances(InstanceIds=[self.id])

while True:

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

    instanceSelection = int(input("\n> "))
    if instanceSelection > 0 and instanceSelection <= len(instances):

        while True:

            # Display the overview of the instance
            instances[instanceSelection-1].overview()

            print("""
Please Choose An Option:

1. More Info
2. SSH Into Instance
3. Toggle Start/Stop Instance
4. Back
            """)

            # Sub menu user input
            subMenuSelection = input("> ")

            if subMenuSelection == "1":

                # Pretty print all instance data
                pprint(instances[instanceSelection-1].data)

            elif subMenuSelection == "2":

                # SSH into instance
                instances[instanceSelection-1].ssh()

            elif subMenuSelection == "3":
                
                # Toggle the state of the instance
                instances[instanceSelection-1].toggleState()
            
            elif subMenuSelection == "4":
                 
                # Break out the while loop, navigating to previous menu
                break

            else: 
                next

    else:
        next