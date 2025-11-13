pipeline {
    agent any

    stages {
        stage('Preparar entorno') {
            steps {
                echo '🔧 Verificando código fuente disponible...'
                sh 'pwd'
                sh 'ls -la'
            }
        }

        stage('Build Backend') {
            steps {
                echo '⚙️ Construyendo Backend...'
                dir('/workspace') {
                    sh 'docker-compose build hr-backend'
                }
            }
        }

        stage('Build Frontend') {
            steps {
                echo '🧱 Construyendo Frontend...'
                dir('/workspace') {
                    sh 'docker-compose build hr-frontend'
                }
            }
        }

        stage('Stop Old Containers') {
            steps {
                echo '🛑 Deteniendo y removiendo contenedores anteriores...'
                dir('/workspace') {
                    sh 'docker-compose down hr-backend hr-frontend || true'
                    sh 'docker rm -f hr-backend hr-frontend || true'
                }
            }
        }

        stage('Deploy') {
            steps {
                echo '🚀 Desplegando aplicación...'
                dir('/workspace') {
                    sh 'docker-compose up -d hr-db hr-backend hr-frontend'
                }
            }
        }

        stage('Verify') {
            steps {
                echo '🔍 Verificando despliegue...'
                dir('/workspace') {
                    sh 'docker-compose ps'
                    sh 'sleep 10'
                    sh 'curl -f http://hr-backend:8000/ || curl -f http://localhost:8000/ || exit 1'
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
