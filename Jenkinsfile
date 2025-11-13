pipeline {
    agent any
    
    stages {
        stage('Checkout') {
            steps {
                echo 'Obteniendo código del repositorio...'
                checkout scm
            }
        }
        
        stage('Build Backend') {
            steps {
                echo 'Construyendo Backend...'
                sh 'docker-compose build hr-backend'
            }
        }
        
        stage('Build Frontend') {
            steps {
                echo 'Construyendo Frontend...'
                sh 'docker-compose build hr-frontend'
            }
        }
        
        stage('Stop Old Containers') {
            steps {
                echo 'Deteniendo contenedores anteriores...'
                sh 'docker-compose down hr-backend hr-frontend || true'
            }
        }
        
        stage('Deploy') {
            steps {
                echo 'Desplegando aplicación...'
                sh 'docker-compose up -d hr-db hr-backend hr-frontend'
            }
        }
        
        stage('Verify') {
            steps {
                echo 'Verificando despliegue...'
                sh 'docker-compose ps'
                sh 'sleep 5'
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