from diagrams import Cluster, Diagram
from diagrams.k8s.compute import Pod, STS
from diagrams.k8s.network import SVC, Ing
from diagrams.k8s.storage import PVC
from diagrams.k8s.podconfig import CM

with Diagram("Vault Solution Diagram", show=False, direction="LR"):
	with Cluster("namespace sanes-vostok-sec"):
		route = Ing("vaultroute")
		pod = Pod("vault-pod-1")
		service = SVC("vaultservice")
		statefulset = STS("vault")
		configmap = CM("vault-config")
		with Cluster("Storage"):
			storages = [PVC("vault-file"),
			            PVC("vault-logs")]
	pod - statefulset - storages
	pod >> configmap
	flow = route >> service >> pod >> storages