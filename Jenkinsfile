pipeline {
    agent any
    
    environment {
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
                    sh "docker build -t $DOCKER_IMAGE_NAME ."
                }
            }
        }
        
        stage('Login Dockerhub abd Push Docker Image') {
            environment {
                DOCKER_HUB_CREDENTIALS = credentials('dockerhub-credentials')
            }
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'dockerhub-credentials', usernameVariable: 'DOCKER_HUB_USERNAME', passwordVariable: 'DOCKER_HUB_PASSWORD')]) {
                        sh "echo $DOCKER_HUB_PASSWORD | docker login -u $DOCKER_HUB_USERNAME --password-stdin"

                        sh "docker push $DOCKER_IMAGE_NAME"
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
