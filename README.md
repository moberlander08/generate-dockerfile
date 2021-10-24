This script is meant to help dynamically generate the FROM line in a standard Dockerfile based on an approvedimage or adminoverride tag that is attached to the sourceimge(runtime) image in the ECR repo.

Workflow:

Buildruntime image > scan image and attach approvedimage tag in ecr > run build_dockerfile.py to generate the FROM line based on the approvedimage tag from before.

NOTE: This script is provided as is and will likely require some slight retooling based on your needs.  As a result it is provided with NO WARRANTY, meaning that I an not respoinable to issues and damages that occur.

