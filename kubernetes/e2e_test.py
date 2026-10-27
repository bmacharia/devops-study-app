#!/usr/bin/env python3
import os
import sys
import time
import subprocess
import argparse
import requests
import logging
import shutil
from urllib.parse import urljoin


# Setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("e2e-tests")


class K8sTestEnvironment:
    def __init__(self, cluster_name="study-app-cluster", skip_cluster_creation=False):
        self.cluster_name = cluster_name
        self.skip_cluster_creation = skip_cluster_creation
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.root_dir = os.path.dirname(self.base_dir)
        self.backend_url = ""
        self.frontend_url = ""
        self.port_forwards = []

        # Sample data for testing
        self.test_session = {"minutes": 45, "tag": "kubernetes"}

        # Check if kubectl is installed
        self.check_kubectl_installed()

    def check_kubectl_installed(self):
        """Check if kubectl is installed and available"""
        if shutil.which("kubectl") is None:
            logger.error(
                "kubectl is not installed or not in PATH. Please install kubectl before running tests."
            )
            sys.exit(1)
        logger.info("kubectl is installed and available.")

    def run_command(self, cmd, cwd=None, shell=False, check=True, capture_output=False):
        """Run a shell command and handle errors"""
        logger.info(f"Running command: {cmd}")
        if shell:
            result = subprocess.run(
                cmd, shell=True, check=check, cwd=cwd, capture_output=capture_output
            )
        else:
            result = subprocess.run(
                cmd.split(), check=check, cwd=cwd, capture_output=capture_output
            )
        return result

    def setup_cluster(self):
        """Set up k3d cluster if not already running"""
        if self.skip_cluster_creation:
            logger.info("Skipping cluster creation as requested")
            return

        # Check if cluster already exists and delete it if it does
        result = self.run_command(
            "k3d cluster list", shell=True, check=False, capture_output=True
        )

        # Safely check if cluster exists in the output
        cluster_exists = False
        if hasattr(result, "stdout") and result.stdout is not None:
            cluster_exists = self.cluster_name in result.stdout.decode("utf-8")

        if cluster_exists:
            logger.info(f"Cluster {self.cluster_name} exists, deleting it")
            self.run_command(f"k3d cluster delete {self.cluster_name}")

        # Create the k3d cluster using our config
        config_path = os.path.join(self.base_dir, "k3d-config.yaml")
        self.run_command(f"k3d cluster create --config {config_path}")

        # Configure kubectl to use the new cluster
        self.run_command("kubectl config use-context k3d-study-app-cluster")

        # Wait for cluster to be ready
        logger.info("Waiting for cluster to be ready...")
        self.run_command("kubectl wait --for=condition=Ready nodes --all --timeout=60s")

    def build_and_load_images(self):
        """Build Docker images and load them into k3d"""
        # Build the backend image
        logger.info("Building backend Docker image")
        self.run_command(
            "docker build -t backend:dev -f ./src/backend/Dockerfile ./src/backend",
            cwd=self.root_dir,
        )

        # Build the frontend image
        logger.info("Building frontend Docker image")
        self.run_command(
            "docker build -t frontend:dev -f ./src/frontend/Dockerfile ./src/frontend",
            cwd=self.root_dir,
        )

        # Import images into k3d
        logger.info("Importing images into k3d")
        self.run_command(f"k3d image import backend:dev -c {self.cluster_name}")
        self.run_command(f"k3d image import frontend:dev -c {self.cluster_name}")

    def get_service_urls(self):
        """Expose Kubernetes Services to the test runner via port-forwarding."""
        services = [
            ("dev-backend", 32112, 22112),
            ("dev-frontend", 32111, 22111),
        ]

        for service_name, local_port, service_port in services:
            command = [
                "kubectl",
                "-n",
                "study-app",
                "port-forward",
                f"service/{service_name}",
                f"{local_port}:{service_port}",
                "--address=127.0.0.1",
            ]
            logger.info("Starting port-forward for %s", service_name)
            try:
                process = subprocess.Popen(
                    command,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
            except OSError as exc:
                logger.error("Failed to start port-forward: %s", exc)
                return False
            self.port_forwards.append(process)

        self.backend_url = "http://127.0.0.1:32112"
        self.frontend_url = "http://127.0.0.1:32111"
        logger.info("Backend URL: %s", self.backend_url)
        logger.info("Frontend URL: %s", self.frontend_url)
        return True

    def deploy_application(self):
        """Deploy the application using kubectl and kustomize"""
        logger.info("Deploying application using kustomize")
        kustomize_path = os.path.join(self.base_dir, "manifests/dev")

        # Apply using kubectl apply and kustomize
        self.run_command(f"kubectl apply -k {kustomize_path}")

        # Wait for pods to be ready
        logger.info("Waiting for pods to be ready...")
        self.run_command(
            "kubectl wait --for=condition=Ready pods --all -n study-app --timeout=120s"
        )

        # Get the service URLs
        if not self.get_service_urls():
            logger.error("Failed to get service URLs")
            return False

        return True

    def wait_for_service_availability(self, url, max_retries=20, delay=5):
        """Check if a service is available by making HTTP requests"""
        logger.info(f"Checking service availability: {url}")
        for i in range(max_retries):
            try:
                response = requests.get(url, timeout=5)
                if response.status_code < 500:  # Consider even 4xx as "available"
                    logger.info(f"Service at {url} is available")
                    return True
            except requests.RequestException:
                pass

            logger.info(
                f"Service not ready yet, retrying in {delay} seconds (attempt {i + 1}/{max_retries})"
            )
            time.sleep(delay)

        logger.error(f"Service at {url} is not available after {max_retries} attempts")
        return False

    def test_backend(self):
        """Test the backend service"""
        logger.info("Testing backend API")
        try:
            # Test root endpoint
            response = requests.get(self.backend_url, timeout=5)
            assert response.status_code == 200, (
                f"Backend root endpoint failed with status code {response.status_code}"
            )
            assert "DevOps Study Tracker API" in response.json().get("message", ""), (
                "Root endpoint doesn't have expected content"
            )
            logger.info("Backend root endpoint test passed")

            # Test health endpoint
            response = requests.get(urljoin(self.backend_url, "/health"), timeout=5)
            assert response.status_code == 200, (
                f"Backend health check failed with status code {response.status_code}"
            )
            assert response.json().get("status") == "healthy", (
                "Health endpoint doesn't report as healthy"
            )
            logger.info("Backend health check passed")

            # Test creating a session
            response = requests.post(
                urljoin(self.backend_url, "/sessions"),
                json=self.test_session,
                timeout=5,
            )
            assert response.status_code == 200, (
                f"Session creation failed with status code {response.status_code}"
            )
            created_session = response.json()
            assert created_session["minutes"] == self.test_session["minutes"], (
                "Created session has incorrect minutes"
            )
            assert created_session["tag"] == self.test_session["tag"], (
                "Created session has incorrect tag"
            )
            assert "id" in created_session, "Created session doesn't have ID field"
            assert "timestamp" in created_session, (
                "Created session doesn't have timestamp field"
            )
            logger.info("Session creation test passed")

            # Test retrieving sessions
            response = requests.get(urljoin(self.backend_url, "/sessions"), timeout=5)
            assert response.status_code == 200, (
                f"Session retrieval failed with status code {response.status_code}"
            )
            sessions = response.json()
            assert isinstance(sessions, list), "Sessions endpoint didn't return a list"
            assert any(
                session["tag"] == self.test_session["tag"] for session in sessions
            ), "Created session not found in sessions list"
            logger.info("Session retrieval test passed")

            # Test filtering sessions by tag
            response = requests.get(
                urljoin(self.backend_url, f"/sessions?tag={self.test_session['tag']}"),
                timeout=5,
            )
            assert response.status_code == 200, (
                f"Filtered sessions retrieval failed with status code {response.status_code}"
            )
            filtered_sessions = response.json()
            assert all(
                session["tag"] == self.test_session["tag"]
                for session in filtered_sessions
            ), "Filtered sessions contain incorrect tags"
            logger.info("Filtered sessions test passed")

            # Test retrieving statistics
            response = requests.get(urljoin(self.backend_url, "/stats"), timeout=5)
            assert response.status_code == 200, (
                f"Stats retrieval failed with status code {response.status_code}"
            )
            stats = response.json()
            assert "total_time" in stats, "Stats doesn't include total_time"
            assert "time_by_tag" in stats, "Stats doesn't include time_by_tag"
            assert "total_sessions" in stats, "Stats doesn't include total_sessions"
            assert "sessions_by_tag" in stats, "Stats doesn't include sessions_by_tag"
            assert stats["total_sessions"] > 0, (
                "Stats shows no sessions despite adding one"
            )
            assert self.test_session["tag"] in stats["sessions_by_tag"], (
                "Added tag not found in stats"
            )
            logger.info("Statistics retrieval test passed")

            return True
        except Exception as e:
            logger.error(f"Backend test failed: {str(e)}")
            return False

    def test_frontend(self):
        """Test the frontend service"""
        logger.info("Testing frontend")
        try:
            # Basic connectivity check
            response = requests.get(self.frontend_url, timeout=5)
            assert response.status_code == 200, (
                f"Frontend check failed with status code {response.status_code}"
            )
            logger.info("Frontend connectivity check passed")

            # Check if the page contains expected content
            content = response.text
            assert "DevOps Study Tracker" in content, (
                "Frontend page doesn't contain expected title"
            )

            assert "Tag:" in content, "Frontend page doesn't contain tag input field"
            logger.info("Frontend content check passed")

            # Check for form elements
            assert 'form action="/add_session"' in content, (
                "Frontend page doesn't contain the session form"
            )
            assert 'input type="number" id="minutes"' in content, (
                "Frontend page doesn't contain minutes input"
            )
            assert 'button type="submit"' in content, (
                "Frontend page doesn't contain submit button"
            )
            logger.info("Frontend form elements check passed")

            # Test the frontend health endpoint
            health_url = urljoin(self.frontend_url, "/health")
            response = requests.get(health_url, timeout=5)
            assert response.status_code == 200, (
                f"Frontend health check failed with status code {response.status_code}"
            )
            health_data = response.json()
            assert "status" in health_data, (
                "Frontend health endpoint doesn't include status field"
            )
            assert "api_connectivity" in health_data, (
                "Frontend health endpoint doesn't include api_connectivity field"
            )
            assert health_data["status"] == "healthy", (
                "Frontend reports an unhealthy status"
            )
            assert health_data["api_connectivity"] is True, (
                "Frontend cannot connect to the backend API"
            )
            logger.info("Frontend health endpoint check passed")

            # End-to-end connectivity check - look for elements that would make API calls
            # This is a basic check - in a real test we might use Selenium to test actual functionality

            return True
        except Exception as e:
            logger.error(f"Frontend test failed: {str(e)}")
            return False

    def test_frontend_to_backend(self):
        """Submit a session through Flask and confirm FastAPI stored it."""
        tag = f"ci-frontend-{time.time_ns()}"
        minutes = 7

        try:
            response = requests.post(
                urljoin(self.frontend_url, "/add_session"),
                data={"minutes": str(minutes), "tag": tag},
                allow_redirects=False,
                timeout=5,
            )
            assert response.status_code in (302, 303), (
                f"Frontend form submission returned HTTP {response.status_code}"
            )

            api_response = requests.get(
                urljoin(self.backend_url, f"/sessions?tag={tag}"),
                timeout=5,
            )
            assert api_response.status_code == 200, (
                f"Backend session retrieval returned HTTP {api_response.status_code}"
            )
            sessions = api_response.json()
            assert isinstance(sessions, list), (
                "Backend returned a non-list session response"
            )
            assert any(
                session.get("tag") == tag and session.get("minutes") == minutes
                for session in sessions
            ), "Session submitted through Flask was not found in the backend"

            logger.info("Frontend-to-backend session creation test passed")
            return True
        except (
            requests.RequestException,
            AssertionError,
            ValueError,
            TypeError,
        ) as exc:
            logger.error("Frontend-to-backend integration test failed: %s", exc)
            return False

    def e2e_test_workflow(self):
        """Full end to end test for both frontend and backend integration"""
        logger.info("Running end-to-end integration tests")
        try:
            # Add specific end-to-end tests here that test the interaction between frontend and backend
            # For example, using a headless browser like Selenium to interact with the frontend
            # and verify that it properly communicates with the backend

            # For now, just a simple check that both services are responding
            backend_ok = self.test_backend()
            frontend_ok = self.test_frontend()
            if not (backend_ok and frontend_ok):
                return False

            return self.test_frontend_to_backend()
        except Exception as e:
            logger.error(f"E2E test workflow failed: {str(e)}")
            return False

    def cleanup(self):
        """Clean up resources"""
        if not self.skip_cluster_creation:
            logger.info("Cleaning up: deleting k3d cluster")
            self.run_command(f"k3d cluster delete {self.cluster_name}", check=False)
        else:
            logger.info("Cleaning up: removing study-app namespace")
            self.run_command("kubectl delete namespace study-app", check=False)

    def run(self, cleanup_on_success=True, cleanup_on_failure=False):
        """Run the full test suite"""
        success = False
        try:
            # Setup infrastructure
            self.setup_cluster()
            self.build_and_load_images()
            if not self.deploy_application():
                logger.error("Failed to deploy application")
                return False

            # Wait for services to be available
            backend_available = self.wait_for_service_availability(
                urljoin(self.backend_url, "/health")
            )
            frontend_available = self.wait_for_service_availability(self.frontend_url)

            if not backend_available or not frontend_available:
                logger.error("Services did not become available in time")
                return False

            # Run tests
            success = self.e2e_test_workflow()
            logger.info(f"Tests completed with {'SUCCESS' if success else 'FAILURE'}")

            return success
        except Exception as e:
            logger.error(f"Test run failed with exception: {str(e)}")
            return False
        finally:
            # Stop port-forward processes on both success and failure.
            for process in self.port_forwards:
                if process.poll() is None:
                    process.terminate()
                    try:
                        process.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        process.kill()
                        process.wait()

            # Preserve the existing Kubernetes cleanup policy.
            if (success and cleanup_on_success) or (not success and cleanup_on_failure):
                self.cleanup()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run end-to-end tests for study-app in k3d"
    )
    parser.add_argument(
        "--skip-cluster-creation",
        action="store_true",
        help="Skip creating a new cluster",
    )
    parser.add_argument(
        "--no-cleanup", action="store_true", help="Don't cleanup resources after tests"
    )
    args = parser.parse_args()

    test_env = K8sTestEnvironment(skip_cluster_creation=args.skip_cluster_creation)

    success = test_env.run(cleanup_on_success=not args.no_cleanup)

    sys.exit(0 if success else 1)
