from diagrams import Diagram, Cluster, Edge
from diagrams.onprem.client import Users
from diagrams.onprem.network import Nginx
from diagrams.programming.framework import Django
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.monitoring import Grafana
from diagrams.onprem.network import Internet
from diagrams.generic.device import Mobile

graph_attr = {"fontsize": "20", "bgcolor": "white", "pad": "0.3"}

with Diagram("EcoRecicla AQP - Vista de despliegue", filename="img/despliegue",
             show=False, direction="LR", graph_attr=graph_attr, outformat="png"):
    usuarios = Users("Vecinos, recicladores\ny municipalidad")
    movil = Mobile("PWA en\ncelular")
    with Cluster("Servidor en la nube (VPS)"):
        proxy = Nginx("Nginx\n(HTTPS)")
        with Cluster("Monolito modular"):
            app = Django("API\n(5 módulos)")
        db = PostgreSQL("PostgreSQL")
        mon = Grafana("Monitoreo")
    usuarios >> movil >> proxy >> app
    app >> Edge(label="lee y escribe") >> db
    app >> Edge(label="notificación", style="dashed") >> Internet("WhatsApp\n(servicio externo)")
    app >> Edge(style="dotted") >> mon