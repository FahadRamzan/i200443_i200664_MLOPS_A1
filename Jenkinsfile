
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
        // Notifying the administrator via email using an external SMTP server
        mail to: 'i200443@nu.edu.pk',
             subject: "Successful Docker Image Build",
             body: "The Docker image ${IMAGE_NAME}:${TAG} has been built and pushed successfully.",
             smtpHost: 'smtp.gmail.com',
             smtpPort: '587',
             credentialsId: 'your-gmail-credentials-id' // Jenkins credentials ID for Gmail
    }
    failure {
       //notify if the pipeline fails using an external SMTP server
        mail to: 'i200443@nu.edu.pk',
             subject: "Docker Image Build Failed",
             body: "There was a problem building or pushing the Docker image ${IMAGE_NAME}:${TAG}.",
             smtpHost: 'smtp.gmail.com',
             smtpPort: '587',
             credentialsId: 'your-gmail-credentials-id' // Jenkins credentials ID for Gmail
    }
}

}
