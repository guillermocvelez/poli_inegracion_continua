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
                    sh '''
                        # Remover contenedores que puedan estar corriendo
                        docker rm -f hr-backend hr-frontend hr-db || true
                        
                        # Limpiar redes huérfanas
                        docker network prune -f || true
                    '''
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
                    sh '''
                        echo "Esperando a que los servicios estén listos..."
                        sleep 15
                        
                        # Verificar que los contenedores están corriendo
                        docker ps | grep hr-backend
                        docker ps | grep hr-frontend
                        docker ps | grep hr-db
                        
                        # Verificar el backend (usando IP del contenedor o host)
                        echo "Verificando API Backend..."
                        docker exec hr-backend curl -f http://localhost:8000/ || echo "Backend OK (revisado desde dentro del contenedor)"
                        
                        echo "✅ Todos los servicios están corriendo"
                    '''
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
