pipeline {
    agent any

    tools {
        // ✅ Must match the name you gave in Global Tool Configuration
        python 'Python3'
    }

    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/vinay-k94/pytest_framework_project.git',
                    credentialsId: 'your-git-credentials-id'   // replace if using private repo
            }
        }

        stage('Setup Virtual Environment') {
            steps {
                bat '''
                    python -m venv venv
                    call venv\\Scripts\\activate
                    python -m pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                bat '''
                    call venv\\Scripts\\activate
                    pytest --maxfail=1 --disable-warnings -q --alluredir=allure-results
                '''
            }
        }

        stage('Allure Report') {
            steps {
                allure includeProperties: false,
                       jdk: '',
                       results: [[path: 'allure-results']]
            }
        }
    }

    post {
        always {
            junit 'reports/*.xml'   // If you generate JUnit XML reports
        }
    }
}
