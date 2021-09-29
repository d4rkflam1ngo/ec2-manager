# AWS EC2 Manager
A python script to manage AWS EC2 instances

### Currently Supported Features
* The ability to select instances and display an overview for each one.
* You can now describe instances in more detail (JSON output).
* SSH into instances by specifying a username and pem file.
* Toggle the state of each instance.

### Requirements
* boto3
* termcolor

### Installation
1. Clone this repository using the command:
```
git clone https://github.com/d4rkflam1ngo/ec2-manager && cd ec2-manager
```
2. Install the script requirements using:
```
pip install -r requirements.txt
```
3. Create your own AWS access key using [this guide](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html#Using_CreateAccessKey).
4. Create the file `~/.aws/credentials` and add the following content, inserting your access key:
```
[default]
aws_access_key_id = YOUR_ACCESS_KEY_ID
aws_secret_access_key = YOUR_SECRET_ACCESS_KEY
```
5. Change the line `REGION = "us-east-1"` to specify your own AWS region.
6. Launch the script by running:
```
python3 ec2-manager.py
```

### Requested Features
- [x] Toggle the state of instances
- [ ] Web interface?
- [ ] Create/remove security groups
