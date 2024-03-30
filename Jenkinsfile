pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE_NAME = 'fahadramzan/mlops_a1:latest'
        DOCKER_HOST = 'tcp://localhost:2375'
    }
    
    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/FahadRamzan/i200443_i200664_MLOPS_A1.git'
            }
        }
        
          stage('Containerize') {
            steps {
                script {
                    
                    docker.build("${IMAGE_NAME}:${TAG}")
                }
            }
        }
        
        stage('Push') {
            steps {
                script {
                    // Logging in to Docker Hub and pushing the image
                    docker.withRegistry('https://index.docker.io/v1/', DOCKERHUB_CREDENTIALS_ID) {
                        docker.image("${IMAGE_NAME}:${TAG}").push()
                    }
                }
            }
        }
    }
    
    post {
        success {
            emailext (
                subject: 'Jenkins Build Success',
                body: 'The Jenkins build was successful.',
                to: 'i200443@nu.edu.pk'
            )
        }
        failure {
            emailext (
                subject: 'Jenkins Build Failure',
                body: 'The Jenkins build failed. Please check the build logs for details.',
                to: 'i200443@nu.edu.pk'
            )
        }
    }
    
    triggers {
        githubPush()
    }
}
