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

def get_instance_private_ip(instance_id):
    client = ec2_connection()
    instance = client.Instance(instance_id)
    if instance.public_ip_address is not None:
        return instance.public_ip_address
    return instance.private_ip_address

def get_old_asg_instances(asg_object):
    """Gets instances from ASG that are not using the correct launch configuration"""
    all_instances = []
    instances = asg_object['AutoScalingGroups'][0]['Instances']
    for instance in instances:
        print(instance)
        print('####################')
        if 'LaunchConfigurationName' not in instance:
            all_instances.append(instance['InstanceId'])
    return all_instances

asg = get_autoscaling_group('mesos-application-s1')

print(get_instance_private_ip('i-072e7161c222149a9'))
