pipeline {
    agent any

    environment {
        PROJECT_DIR = '/var/jenkins_home/workspace/integracion_continua'
    }

    stages {
        stage('Preparar entorno') {
            steps {
                echo '🔧 Verificando código fuente disponible...'
                dir("${PROJECT_DIR}") {
                    sh 'ls -la'
                }
            }
        }

        stage('Build Backend') {
            steps {
                dir("${PROJECT_DIR}") {
                    echo '⚙️ Construyendo Backend...'
                    sh 'docker-compose build hr-backend'
                }
            }
        }

        stage('Build Frontend') {
            steps {
                dir("${PROJECT_DIR}") {
                    echo '🧱 Construyendo Frontend...'
                    sh 'docker-compose build hr-frontend'
                }
            }
        }

        stage('Stop Old Containers') {
            steps {
                dir("${PROJECT_DIR}") {
                    echo '🛑 Deteniendo contenedores anteriores...'
                    sh 'docker-compose down hr-backend hr-frontend || true'
                }
            }
        }

        stage('Deploy') {
            steps {
                dir("${PROJECT_DIR}") {
                    echo '🚀 Desplegando aplicación...'
                    sh 'docker-compose up -d hr-db hr-backend hr-frontend'
                }
            }
        }

        stage('Verify') {
            steps {
                dir("${PROJECT_DIR}") {
                    echo '🔍 Verificando despliegue...'
                    sh 'docker-compose ps'
                    sh 'sleep 5'
                    sh 'curl -f http://localhost:8000/ || exit 1'
                }
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
