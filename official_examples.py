from diagrams import Cluster, Diagram, Edge
# for node example
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB
from diagrams.aws.storage import S3
# for cluster example
from diagrams.aws.compute import ECS
from diagrams.aws.network import Route53
# for edge example
from diagrams.onprem.analytics import Spark
from diagrams.onprem.compute import Server
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.aggregator import Fluentd
from diagrams.onprem.monitoring import Grafana, Prometheus
from diagrams.onprem.network import Nginx
from diagrams.onprem.queue import Kafka


with Diagram(name="./images/official_examples.png", show=False):
    # node
    with Cluster("Node sample"):
        ELB("lb") >> EC2("web") >> RDS("userdb") >> S3("store")
        ELB("lb") >> EC2("web") >> RDS("userdb") << EC2("stat")
        (ELB("lb") >> EC2("web")) - EC2("web") >> RDS("userdb")

    # cluster
    dns = Route53("dns")
    web = ECS("service")

    with Cluster("Cluster example"):
        with Cluster("DB Cluster"):
            db_master = RDS("master")
            db_slaves = [RDS("slave1"), RDS("slave2")]
            db_master - db_slaves

        dns >> web >> db_master

    # Edge
    ingress = Nginx("ingress")

    metrics = Prometheus("metric")
    metrics << Edge(color="firebrick", style="dashed") << Grafana("monitoring")

    with Cluster("Edge example"):
        with Cluster("Service Cluster"):
            grpcsvc = [
                Server("grpc1"),
                Server("grpc2"),
                Server("grpc3")]

        with Cluster("Sessions HA"):
            master = Redis("session")
            master - Edge(color="brown", style="dashed") - Redis("replica") << Edge(label="collect") << metrics
            grpcsvc >> Edge(color="brown") >> master

        with Cluster("Database HA"):
            master = PostgreSQL("users")
            master - Edge(color="brown", style="dotted") - PostgreSQL("slave") << Edge(label="collect") << metrics
            grpcsvc >> Edge(color="black") >> master

        aggregator = Fluentd("logging")
        aggregator >> Edge(label="parse") >> Kafka("stream") >> Edge(color="black", style="bold") >> Spark("analytics")

        ingress >> Edge(color="darkgreen") << grpcsvc >> Edge(color="darkorange") >> aggregator
