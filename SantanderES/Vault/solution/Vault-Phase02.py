from diagrams import Cluster, Diagram, Edge
from diagrams.k8s.compute import Pod, STS
from diagrams.k8s.network import SVC, Ing
from diagrams.k8s.storage import PVC
from diagrams.k8s.podconfig import CM
from diagrams.onprem.ci import Jenkins
from diagrams.onprem.vcs import Github
from diagrams.onprem.compute import Server

with Diagram("Vault Solution Diagram - Fase 02", show=False, direction="LR"):
	with Cluster("Openshift PAAS2"):
		with Cluster("namespace sanes-vostok-sec"):
			route = Ing("vault-route")
			pod = Pod("vault-pod-1")
			service = SVC("vault-service")
			statefulset = STS("vault")
			configmap = CM("vault-config")
			with Cluster("Storage"):
				storages = [PVC("vault-file"),
				            PVC("vault-logs")]
		with Cluster("namespace sanes-fmw-test"):
			taas = Ing("taas-route")

		with Cluster("namespace sanes-vostok-release"):
			podTaskRelease = Pod("task-deploy")
			podTaskSwitch = Pod("task-switch")

		with Cluster("namespace san-vostok"):
			podOnboardingCloud = Pod("onboarding-cloud")

		with Cluster("namespace sanes-mialm"):
			podMialm = Pod("mialm")

	pod - statefulset - storages
	pod >> configmap
	flow = route >> service >> pod >> storages

	with Cluster("ALM MULTICLOUD"):
		jenkins = Jenkins("master")
		with Cluster("github.alm.europe"):
			github = Github("")
		with Cluster("nexus.alm.europe"):
			nexus = Server("")
		with Cluster("sonar.alm.europe"):
			sonar = Server("")

	with Cluster("Estructurales"):
		estructurales = Server("")

	route << Edge(color="red") << jenkins
	estructurales << Edge(color="red") << jenkins
	taas << Edge(color="red") << jenkins
	jenkins >> nexus
	jenkins >> sonar
	jenkins >> github

	podTaskRelease >> route
	podTaskSwitch >> route
	podOnboardingCloud >> route
	podMialm >> route