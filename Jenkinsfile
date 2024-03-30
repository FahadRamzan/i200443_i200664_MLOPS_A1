pipeline {
    agent any
    
    environment {
        DOCKER_CREDENTIALS = 'docker-hub-credentials'
        DOCKER_IMAGE_NAME = 'RumaisaIlyas/mlops_A1:latest'
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
                // Build Docker image
                script {
                    docker.build(DOCKER_IMAGE_NAME, "-f Dockerfile .")
                }
            }
        }
        
        stage('Push to Docker Hub') {
            steps {
                script {
                    docker.withRegistry('https://registry.hub.docker.com', DOCKER_CREDENTIALS) {
                        docker.image(DOCKER_IMAGE_NAME).push()
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
