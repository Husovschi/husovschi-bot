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
                        // Use StringBuilder to construct the .env file securely
                        def envContent = new StringBuilder()
                        envContent.append("API_ID=${env.API_ID}\n")
                        envContent.append("API_HASH=${env.API_HASH}\n")
                        envContent.append("BOT_TOKEN=${env.BOT_TOKEN}\n")

                        // Write the .env file
                        writeFile file: '.env', text: envContent.toString()
                    }
                }
            }
        }
        stage('Deploy Services') {
            steps {
                script {
                    // Deploy using Docker Compose
                    sh '''
                    docker compose pull
                    docker compose up -d --remove-orphans
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
