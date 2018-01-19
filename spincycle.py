"""Rotates instances in a specified ASG that are not using the latest launch configuration"""

import logging
import argparse
import sys
import time
import boto3

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - [%(levelname)s] - %(message)s')
LOGGER = logging.getLogger()

def autoscaling_connection():
    """Boto3 connection to EC2 for autoscaling"""
    client = boto3.client('autoscaling')
    return client

def ec2_connection():
    """Boto3 connection to EC2"""
    client = boto3.resource('ec2')
    return client

def get_autoscaling_group(asg_name):
    """Gets autoscaling group details"""
    client = autoscaling_connection()
    response = client.describe_auto_scaling_groups(AutoScalingGroupNames=[asg_name])
    if not response['AutoScalingGroups']:
        LOGGER.error("Autoscaling group %s not found", asg_name)
        sys.exit(1)
    return response


def get_old_asg_instances(asg_object):
    """Gets instances from ASG that are not using the correct launch configuration"""
    all_instances = []
    instances = asg_object['AutoScalingGroups'][0]['Instances']
    for instance in instances:
        if 'LaunchConfigurationName' not in instance:
            all_instances.append(instance['InstanceId'])
    return all_instances

def terminate_ec2_instance(instance_id):
    """Terimates an EC2 instance with the instance id"""
    client = ec2_connection()
    client.instances.filter(InstanceIds=[instance_id]).terminate()

def all_asg_instances_healthy(asg_name):
    """Validates that all instances in ASG are marked Healthy
    This is a basic sanity check so we dont continue rotating Instances
    in a case where there is a problem with the AMI itself"""
    client = autoscaling_connection()
    response = client.describe_auto_scaling_groups(AutoScalingGroupNames=[asg_name])
    if not response['AutoScalingGroups']:
        LOGGER.error("Autoscaling group %s not found", asg_name)
        sys.exit(1)
    for instance in response['AutoScalingGroups'][0]['Instances']:
        if instance['HealthStatus'] != 'Healthy':
            return False
    return True


def rotate_asg(asg_name):
    """Main function that facilitates rotating instances in the ASG"""

    asg_object = get_autoscaling_group(asg_name)
    instances = get_old_asg_instances(asg_object)
    LOGGER.info("Found %s instances that have old launch configuration", len(instances))

    #exit if there are no instances to rotate
    if not instances:
        sys.exit(0)

    for instance_id in instances:
        if not all_asg_instances_healthy(asg_name):
            LOGGER.error("All instances in ASG are not healthy, exiting")
            sys.exit(1)
        terminate_ec2_instance(instance_id)
        LOGGER.info("Terminating instance id: %s sleeping for %i seconds",
                    instance_id, ARGS.sleep_time)
        time.sleep(ARGS.sleep_time)

def get_instance_ip(instance_id):
    """Gets ip address from a given instance id
    it will return the public ip if the instnace has one
    otherwise it returns the private ip"""
    client = ec2_connection()
    instance = client.Instance(instance_id)
    if instance.public_ip_address is not None:
        return instance.public_ip_address
    return instance.private_ip_address

PARSER = argparse.ArgumentParser(description='Rotate old instances from an ASG')
PARSER.add_argument('--asg-name', '-a', dest='asg_name', required=True, help='The name of the ASG you want to rotate')
PARSER.add_argument('--sleep-time', '-s', dest='sleep_time', required=False, default=600, help="The time you want to wait between rotating instances (default 600)")


ARGS = PARSER.parse_args()

rotate_asg(ARGS.asg_name)
