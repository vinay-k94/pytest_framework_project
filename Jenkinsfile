pipeline {
    agent any

    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/vinay-k94/pytest_framework_project.git'
            }
        }

        stage('Setup Python Environment') {
            steps {
                bat '''
                    "C:\\Users\\admin\\AppData\\Local\\Programs\\Python\\Python311\\python.exe" -m venv venv
                    call venv\\Scripts\\activate
                    "C:\\Users\\admin\\AppData\\Local\\Programs\\Python\\Python311\\python.exe" -m pip install --upgrade pip
                    "C:\\Users\\admin\\AppData\\Local\\Programs\\Python\\Python311\\python.exe" -m pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                bat '''
                    call venv\\Scripts\\activate
                    pytest --html=reports/report.html --self-contained-html --alluredir=reports/allure
                '''
            }
        }

        stage('Publish HTML Report') {
            steps {
                publishHTML([
                    allowMissing: false,
                    alwaysLinkToLastBuild: true,
                    keepAll: true,
                    reportDir: 'reports',
                    reportFiles: 'report.html',
                    reportName: 'Pytest HTML Report'
                ])
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'reports/**', followSymlinks: false
        }
    }
}
