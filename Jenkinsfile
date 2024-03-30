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
                // Build Docker image
                script {
                    bat "docker build -t $DOCKER_IMAGE_NAME ."
                }
            }
        }

        
        stage('Login Dockerhub and Push Docker Image') {
            environment {
                DOCKER_HUB_CREDENTIALS = credentials('dockerhub-credentials')
            }
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'dockerhub-credentials', usernameVariable: 'DOCKER_HUB_USERNAME', passwordVariable: 'DOCKER_HUB_PASSWORD')]) {
                        // Echo Docker Hub username
                        echo "Docker Hub username: $DOCKER_HUB_USERNAME"
                        
                        // Perform Docker login
                        def loginCmd = "echo $DOCKER_HUB_PASSWORD | docker login -u $DOCKER_HUB_USERNAME --password-stdin"
                        def loginStatus = bat script: loginCmd, returnStatus: true
                        
                        if (loginStatus == 0) {
                            echo "Docker login successful."
                        } else {
                            error "Docker login failed. Exit code: $loginStatus"
                        }
                        
                        // Push Docker image
                        def pushCmd = "docker push $DOCKER_IMAGE_NAME"
                        bat pushCmd
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
