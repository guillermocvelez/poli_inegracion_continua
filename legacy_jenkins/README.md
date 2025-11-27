# Legacy Jenkins Configuration

Este directorio contiene la configuración histórica de Jenkins que se utilizó previamente para CI/CD.

## ⚠️ DEPRECATED - Solo para referencia histórica

El proyecto ahora utiliza **GitHub Actions** para CI/CD. Esta configuración se mantiene como referencia.

## Archivos incluidos:

- `jenkins/` - Dockerfile personalizado de Jenkins con Docker CLI
- `Jenkinsfile` - Pipeline de CI/CD que se ejecutaba en Jenkins
- `docker-compose-with-jenkins.yml` - Docker Compose completo incluyendo Jenkins

## Para restaurar Jenkins (si es necesario):

1. Copiar `jenkins/` a la raíz del proyecto
2. Copiar `Jenkinsfile` a la raíz del proyecto
3. Agregar el servicio Jenkins desde `docker-compose-with-jenkins.yml` al `docker-compose.yml`
4. Ejecutar: `docker-compose up -d jenkins`

## Pipeline Jenkins vs GitHub Actions

Jenkins se reemplazó por GitHub Actions por las siguientes razones:

- ✅ No requiere infraestructura adicional
- ✅ Integración nativa con GitHub
- ✅ Gratis para repositorios públicos
- ✅ Más simple de configurar y mantener

## Fecha de deprecación

27 de noviembre de 2025
