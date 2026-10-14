
pipeline {
    agent any

    options {
        timestamps()
    }

    environment {
        XDG_RUNTIME_DIR = '/run/user/989'
        DBUS_SESSION_BUS_ADDRESS = 'unix:path=/run/user/989/bus'
        IMAGE_NAME = 'mhdsanjid/devops-mastery-app'
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/mohammedsanjid-stack/devops-mastery-challenge.git'
            }
        }

        stage('Check Tools') {
            steps {
                sh 'python3 --version'
                sh 'git --version'
                sh 'podman --version'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    python3 -m venv .venv
                    .venv/bin/python -m pip install --upgrade pip
                    .venv/bin/python -m pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '.venv/bin/python -m pytest -v'
            }
        }

        stage('Build Container Image') {
            steps {
                sh '''
                    podman build \
                      --memory=300m \
                      --memory-swap=300m \
                      --jobs=1 \
                      --tag localhost/devops-mastery-app:${BUILD_NUMBER} \
                      .
                '''
            }
        }

        stage('Push Image to Docker Hub') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-credentials',
                        usernameVariable: 'DOCKERHUB_USERNAME',
                        passwordVariable: 'DOCKERHUB_TOKEN'
                    )
                ]) {
                    sh '''
                        set +x
                        AUTHFILE="$WORKSPACE/.docker-auth.json"
                        trap 'podman logout --authfile "$AUTHFILE" docker.io >/dev/null 2>&1 || true; rm -f "$AUTHFILE"' EXIT

                        printf '%s' "$DOCKERHUB_TOKEN" | \
                          podman login \
                            --authfile "$AUTHFILE" \
                            --username "$DOCKERHUB_USERNAME" \
                            --password-stdin docker.io

                        podman tag \
                          localhost/devops-mastery-app:${BUILD_NUMBER} \
                          docker.io/${IMAGE_NAME}:${BUILD_NUMBER}

                        podman tag \
                          localhost/devops-mastery-app:${BUILD_NUMBER} \
                          docker.io/${IMAGE_NAME}:latest

                        podman push \
                          --authfile "$AUTHFILE" \
                          docker.io/${IMAGE_NAME}:${BUILD_NUMBER}

                        podman push \
                          --authfile "$AUTHFILE" \
                          docker.io/${IMAGE_NAME}:latest
                    '''
                }
            }
        }
    }

    post {
        success {
            echo 'CI pipeline completed: tests passed, image built and pushed to Docker Hub.'
        }

        failure {
            echo 'CI pipeline failed. Review the stage logs.'
        }

        always {
            cleanWs()
        }
    }
}

