pipeline {
    agent {
        label 'main'
    }

    stages {
        stage('Generate .env File') {
            steps {
                script {
                    withCredentials([
                        [$class: 'VaultUsernamePasswordCredentialBinding', credentialsId: 'vault-telegram-husovschi-bot', passwordVariable: 'API_HASH', usernameVariable: 'API_ID'],
                        [$class: 'VaultStringCredentialBinding', credentialsId: 'vault-telegram-husovschi-bot-token', variable: 'BOT_TOKEN']
                    ]) {
                        writeFile file: '.env', text: """
                        API_ID=${env.API_ID}
                        API_HASH=${env.API_HASH}
                        BOT_TOKEN=${env.BOT_TOKEN}
                        """
                    }
                    
                }
            }
        }
        stage('Deploy Services') {
            steps {
                script {
                    // Deploy using Docker Compose
                    sh '''
                    docker-compose pull
                    docker-compose up -d --remove-orphans
                    '''
                }
            }
        }
    }

    post {
        always {
            echo 'Pipeline execution completed.'
        }
        failure {
            echo 'Deployment failed.'
        }
    }
}
