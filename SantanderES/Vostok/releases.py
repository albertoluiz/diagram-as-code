from diagrams import Cluster, Diagram
from diagrams.k8s.compute import Pod, Deployment
from diagrams.k8s.network import SVC, Ing
from diagrams.k8s.storage import PVC
from diagrams.onprem.compute import Server

with Diagram("Vostok Releases Solution Diagram", show=False, direction="LR"):
	openshift = Server("openshift")

	with Cluster("sanes-vostok-release"):
		with Cluster("deployment scdf-server"):
			scdfServerPod = Pod("scdf-server-pod")
			scdfServerDeployment = Deployment("scdf-server")
			scdfServerDeployment - scdfServerPod
		scdfServerService = SVC("scdf-server-service")
		scdfServerRoute = Ing("scdf-server-route")

		with Cluster("deployment mysql"):
			mysqlMasterDeployment = Deployment("mysql-master")
			mysqlMasterPod = Pod("mysql-master-pod")
			mysqlMasterDeployment - mysqlMasterPod
		mysqlMasterService = SVC("mysql-master-service")

		with Cluster("storage"):
			mysqlPvc = PVC("mysql")

		with Cluster("rabbitmq"):
			rabbitmqDeployment = Deployment("rabbitmq")
			rabbitmqPod = Pod("rabbitmq")
			rabbitmqDeployment - rabbitmqPod

		with Cluster("reader"):
			scdfServerReaderDeployment = Deployment("scdf-server-reader-deployment")
			scdfServerReaderPod = Pod("scdf-server-reader-pod")
			scdfServerReaderDeployment - scdfServerReaderPod

		with Cluster("Apps"):
			with Cluster("streams"):
				sinkTaskStatusNotificationPod = Pod("sink-task-status-notification")
				logsEvents = Pod("logs-events")
				sinkElastic = Pod("sink-elastic")
				sinkElasticDataRabbit = Pod("sink-elastic-data-rabbit")
				sinkTaskLifeCicle = Pod("sink-task-life-cicle")

			with Cluster("tasks"):
				taskFunctionalTest = Pod("task-functional-test")
				taskOpenshiftDeploy = Pod("task-openshift-deploy")
				taskOpenshiftSwitch = Pod("task-openshift-switch-bg")
				composedTaskRunner = Pod("composed-task-runner")

	scdfServerRoute >> scdfServerService >> scdfServerPod >> mysqlMasterService >> mysqlMasterPod
	mysqlMasterPod >> mysqlPvc
	taskOpenshiftDeploy >> openshift
	taskOpenshiftSwitch >> openshift