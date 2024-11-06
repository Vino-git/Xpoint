import argparse
import subprocess

def main():
    parser = argparse.ArgumentParser(description="Deploy EC2 launch template through ASG.")
    parser.add_argument("-n", "--base_name", required=True, help="Base name for creating resource with environment name as suffix, e.g., 'awesome'")
    parser.add_argument("-s", "--instance_count", type=int, required=True, help="Number of instances that ASG can use to scale up and down. The count should be between the range of 1 to 10")
    #parser.add_argument("-h", "--help", action="help", help="Display this help message and exit") #Be default, argparse considered -h as help message

    args = parser.parse_args()

    if args.instance_count < 1 or args.instance_count > 10:
        parser.error("Instance count must be between 1 and 10")

    stack_name = f"{args.base_name}-stack"

    print(f"Deploying CloudFormation stack with base name '{args.base_name}' and instance count '{args.instance_count}'...")
    command = f"aws cloudformation deploy --template-file Xpoint/Ec2LaunchTemplate/template.yml --stack-name {stack_name} --parameter-overrides EnvironmentName={args.base_name} DesiredCapacity={args.instance_count} --capabilities CAPABILITY_NAMED_IAM"
    try:
        subprocess.run(command, shell=True, check=True)
        print("Stack deployment initiated successfully.")
        print(f"Stack Name: {stack_name}")
        print(f"Base Name: {args.base_name}")
        print(f"Instance Count: {args.instance_count}")
    except subprocess.CalledProcessError as e:
        print(f"Error: Stack deployment failed with return code {e.returncode}")

if __name__ == "__main__":
    main()
