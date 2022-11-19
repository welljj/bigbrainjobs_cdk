import aws_cdk.aws_ec2 as ec2
from aws_cdk import Stack
from constructs import Construct

from .server_config import gen


class BigbrainjobsCdkStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        default_vpc = ec2.Vpc.from_lookup(self, "MyVPC", is_default=True)

        user_data = ec2.UserData.for_linux(shebang="#cloud-config")
        user_data.add_commands(gen.get_yaml())

        my_instance = ec2.Instance(
            self,
            "MyInstance",
            vpc=default_vpc,
            instance_type=ec2.InstanceType("t4g.nano"),
            machine_image=ec2.MachineImage.from_ssm_parameter(
                "/aws/service/canonical/ubuntu/server-minimal/22.10/stable/current/arm64/hvm/ebs-gp2/ami-id"
                # "/aws/service/canonical/ubuntu/server/22.10/stable/current/arm64/hvm/ebs-gp2/ami-id"
            ),
            key_name="MyKeyPair",
            user_data=user_data,
            user_data_causes_replacement=True,
            # machine_image=ec2.MachineImage.latest_amazon_linux(
            #     cpu_type=ec2.AmazonLinuxCpuType.ARM_64,
            #     edition=ec2.AmazonLinuxEdition.STANDARD,
            #     generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2,
            #     kernel=ec2.AmazonLinuxKernel.KERNEL5_X,
            #     storage=ec2.AmazonLinuxStorage.GENERAL_PURPOSE,
            #     virtualization=ec2.AmazonLinuxVirt.HVM,
            # ),
            # init=ec2.CloudFormationInit.from_elements(
            #     ec2.InitPackage.yum("nginx"),
            #     ec2.InitPackage.yum("python38"),
            #     ec2.InitPackage.yum("postgresql"),
            # ),
        )

        # HTTP
        my_instance.connections.allow_from_any_ipv4(ec2.Port.tcp(80))
        # HTTPS
        my_instance.connections.allow_from_any_ipv4(ec2.Port.tcp(443))
        # SSH
        my_instance.connections.allow_from_any_ipv4(ec2.Port.tcp(22))

        # Elastic IP: 3.136.184.243
        eip = ec2.CfnEIP(self, "MyEIP", instance_id=my_instance.instance_id)
