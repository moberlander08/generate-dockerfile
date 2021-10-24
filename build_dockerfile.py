#!/bin/env python

import os
import boto3
from sys import argv


def main():

    # if a container image was sepcified
    if len(argv) > 2:

        source_image = str(argv[1])
        app_image = str(argv[2])

    else:
        print("A source and application ECR image is required to proceed!")
        print("ex: python build_dockerfile <exmapleimagename> <exampleapplication")
        exit(1)

    REGION = os.environ.get('AWS_REGION')
    BASEPATH = os.getcwd()

    # first get the aws account id
    accountid = account_id(REGION)

    image_tag = get_approved_repo_tag(accountid, source_image, REGION)

    if image_tag:
        # construct image name
        full_image_name = f'{accountid}.dkr.ecr.{REGION}.amazonaws.com/{source_image}:{image_tag}'

        construct_dockerfile(full_image_name, app_image, BASEPATH)
    else:
        print(f"There is no approved image for {source_image}, unable to continue")
        exit(1)


# find the account id
def account_id(REGION: str):

    # get the account id
    sts_client = boto3.client('sts', region_name=REGION)
    aws_account = sts_client.get_caller_identity()
    awsaccount = aws_account['Account']

    # return the account id
    return awsaccount


def get_approved_repo_tag(accountid: str, repo: str, REGION: str):

    # create the ecr_client
    ecr_client = boto3.client('ecr', region_name=REGION)

    # get the repo arn
    response = ecr_client.describe_repositories(
        repositoryNames=[
            repo,
        ]
    )

    repo_arn = str(response['repositories'][0]['repositoryArn'])

    # need to perform some tag logic
    response = ecr_client.list_tags_for_resource(
        resourceArn=repo_arn
    )

    # if there is an adminoverride tag
    if response['tags']:
        for tag in response['tags']:
            if tag['Key'] == 'adminoverride':
                return str(tag['Value'])
            elif tag['Key'] == 'approvedimage':
                return str(tag['Value'])

    return None


# create the Dockerfile
def construct_dockerfile(full_image_name: str, app_image: str, BASEPATH: str):

    # open the Dockerfile.template
    with open(f'{BASEPATH}/{app_image}/Dockerfile.template', 'r') as read_obj, open(f'{BASEPATH}/{app_image}/Dockerfile', 'w') as write_obj:
        write_obj.write('FROM ' + full_image_name + '\n')

        # add in the template file, lines
        for line in read_obj:
            write_obj.write(line)


if __name__ == '__main__':
    main()
