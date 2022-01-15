from tir.deploy import Deploy


def test_deployment_connectivity():
    deploy = Deploy()
    deploy.connect()
