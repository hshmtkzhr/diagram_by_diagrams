from diagrams import Cluster, Diagram, Edge
# generic
from diagrams.generic.device import Mobile, Tablet
from diagrams.generic.storage import Storage
from diagrams.generic.blank import Blank
# gcp
from diagrams.gcp.network import CDN, DNS, LoadBalancing
from diagrams.gcp.analytics import Bigquery
# k8s
from diagrams.k8s.clusterconfig import HPA
from diagrams.k8s.compute import Deployment, Pod, ReplicaSet, StatefulSet , DaemonSet
from diagrams.k8s.network import Ingress, Service
from diagrams.k8s.controlplane import APIServer
from diagrams.gcp.devtools import GCR
from diagrams.gcp.storage import GCS
# onprem
from diagrams.onprem.queue import Kafka
from diagrams.onprem.network import Zookeeper
from diagrams.k8s.storage import PV
from diagrams.k8s.compute import Cronjob
from diagrams.onprem.aggregator import Fluentd
from diagrams.onprem.queue import Kafka
from diagrams.onprem.database import MySQL
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.iac import Terraform, Ansible
from diagrams.onprem.ci import GitlabCI, Jenkins
from diagrams.onprem.vcs import Gitlab

with Diagram(name="A Web Service NOWHERE", filename="./images/overview.png", show=False):
    user = Mobile("User")
    cdn = CDN("CloudCDN")
    gcs = GCS("CloudStorage")
    dns = DNS("CloudDNS")
    hlb = LoadBalancing("HLB")

    # Logging/BI
    bq = Bigquery("BQ")
    bistore = Storage("BI Store")

    # Infra management
    infra_engineer = Tablet("infra engineer")
    provision_tools = [Terraform(), Ansible()]

    # CI/CD
    software_engineer = Tablet("software engineer")
    gitlab = Gitlab("git")
    gitlab_ci = GitlabCI()
    jenkins = Jenkins("jenkins")
    gcr = GCR("container registry")

    with Cluster("GKE Cluster"):
        # api endpoint
        webapp = Pod("WebAPP")
        # queue service
        kafka_broker = Kafka("broker")
        consumer = Pod("consumer")
        # logging
        google_fluentd = Fluentd("google-fluentd")
        # controll plane
        k8s_api_server = APIServer("api-server")

        # flow of web application
        webapp - Deployment() - HPA()
        webapp >> Edge(label="produce") >> kafka_broker
        # flow and relationship of kafka ecosystem
        Service("headless") - kafka_broker - StatefulSet()
        kafka_broker >> PV()
        kafka_broker - Pod("Zookeeper")
        kafka_broker << Edge(label="consume") << consumer
        consumer - Cronjob()
        # flow of logging
        webapp >> Edge(label="logging stdout/err") >> google_fluentd
        google_fluentd - DaemonSet() #>> Edge(label="parse, reform, aggregate")

    with Cluster("Datastore VMs"):
        with Cluster("MySQL shard"):
            mysql_master = MySQL("master")
            mysql_slave = MySQL("slave")
            mysql_for_analysis = MySQL("for analysis")
            mysql_master >> Edge(label="replication") >> [mysql_slave, mysql_for_analysis]

        with Cluster("redis cluster shard"):
            redis_master = Redis("master")
            redis_master >> Edge(label="replication") >> Redis("slave")

    user >> dns
    user >> Edge(label="request static contents") >> cdn
    user >> Edge(label="communicate to API endpoint") >> hlb >> Edge(label="NEG") >> webapp

    webapp >> [mysql_master, mysql_slave]
    webapp >> redis_master

    google_fluentd >> Edge(label="parse,reform,aggregate") >> bq << Edge(label="analyse") << bistore
    mysql_for_analysis << Edge(label="analyse") << bistore

    infra_engineer >> Edge(label="push changes") >> gitlab# - gitlab_ci
    gitlab - gitlab_ci - provision_tools
    provision_tools - mysql_master #>> Edge(label="apply") >> mysql_master
    provision_tools - redis_master #>> Edge(label="run playbook") >> redis_master
    gitlab_ci >> Edge(label="update manifest") >> k8s_api_server

    software_engineer >> Edge(label="merge to master") >> gitlab
    gitlab << Edge(label="bake images") << jenkins
    jenkins >> Edge(label="upload images") >> gcr
    jenkins >> Edge(label="update deployment") >> k8s_api_server
    jenkins >> Edge(label="upload static contents") >> gcs
    cdn - gcs
    gcr << Edge(label="pull images") << k8s_api_server

