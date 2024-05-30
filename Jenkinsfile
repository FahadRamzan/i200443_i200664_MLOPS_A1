
pipeline {
    agent any

    triggers {
        githubPush()
    }
    
    environment {
        DOCKERHUB_CREDENTIALS_ID = 'dockerhub-credentials'
        IMAGE_NAME = 'rumaisailyas/mlops_a1'
        TAG = 'latest' 
        DOCKER_HOST = 'tcp://localhost:2375'
    }
    
    stages {
        stage('Checkout') {
            steps {
                
                checkout scm
            }
        }
        
        stage('Build') {
            steps {
                script {
                    
                    docker.build("${IMAGE_NAME}:${TAG}")
                }
            }
        }
        
        stage('Login Dockerhub and Push Docker Image') {
    environment {
        DOCKER_HUB_CREDENTIALS = credentials('dockerhub-credentials')
    }
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
        echo 'OK'
    }
    failure {
       echo 'NOT OK'
    }
}

}
