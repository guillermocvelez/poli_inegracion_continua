pipeline {
    agent any

    stages {
        stage('Preparar entorno') {
            steps {
                echo '🔧 Verificando código fuente disponible...'
                sh 'ls -la'
                sh 'pwd'
            }
        }

        stage('Build Backend') {
            steps {
                echo '⚙️ Construyendo Backend...'
                sh 'docker-compose build hr-backend'
            }
        }

        stage('Build Frontend') {
            steps {
                echo '🧱 Construyendo Frontend...'
                sh 'docker-compose build hr-frontend'
            }
        }

        stage('Stop Old Containers') {
            steps {
                echo '🛑 Deteniendo contenedores anteriores...'
                sh 'docker-compose stop hr-backend hr-frontend || true'
            }
        }

        stage('Deploy') {
            steps {
                echo '🚀 Desplegando aplicación...'
                sh 'docker-compose up -d hr-db hr-backend hr-frontend'
            }
        }

        stage('Verify') {
            steps {
                echo '🔍 Verificando despliegue...'
                sh 'docker-compose ps'
                sh 'sleep 10'
                sh 'curl -f http://localhost:8000/ || exit 1'
            }
        }
    }

    post {
        success {
            echo '✅ Pipeline ejecutado exitosamente'
        }
        failure {
            echo '❌ Pipeline falló'
        }
    }
}
