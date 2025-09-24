pipeline {
    agent any

    environment {
        PYTHON = 'C:\\Users\\admin\\AppData\\Local\\Programs\\Python\\Python312\\python.exe'
        WORKSPACE_PATH = "${env.WORKSPACE}"
        ALLURE_RESULTS = "${env.WORKSPACE}\\reports\\allure-results"
        HTML_REPORT = "${env.WORKSPACE}\\reports\\html_reports\\report.html"
        ALLURE_REPORT_DIR = "${env.WORKSPACE}\\allure-report"
        PIP_REQUIREMENTS = "${env.WORKSPACE}\\requirements.txt"
    }

    stages {

        stage('Checkout Code') {
            steps {
                git branch: 'main', credentialsId: 'github-creds', url: 'https://github.com/vinay-k94/pytest_framework_project.git'
            }
        }

        stage('Setup Python') {
            steps {
                echo 'Upgrading pip and installing dependencies'
                bat "\"%PYTHON%\" -m pip install --upgrade pip"
                bat "\"%PYTHON%\" -m pip install -r \"%PIP_REQUIREMENTS%\""
            }
        }

        stage('Run Pytest') {
            steps {
                echo 'Running pytest with HTML and Allure reports'
                // Ensure a fixed folder for Allure results
                bat "mkdir \"%ALLURE_RESULTS%\" 2>nul"
                bat "\"%PYTHON%\" -m pytest \"%WORKSPACE%\\tests\" --alluredir=\"%ALLURE_RESULTS%\" --html=\"%HTML_REPORT%\" --self-contained-html"
            }
        }

        stage('Generate Allure Report') {
            steps {
                echo 'Generating Allure report'
                // Assuming you installed Allure in Jenkins global tools
                bat "\"C:\\ProgramData\\Jenkins\\.jenkins\\tools\\ru.yandex.qatools.allure.jenkins.tools.AllureCommandlineInstallation\\AllureCommand\\bin\\allure.bat\" generate \"%ALLURE_RESULTS%\" -o \"%ALLURE_REPORT_DIR%\" --clean"
            }
        }

        stage('Publish Reports') {
            steps {
                echo 'Publishing HTML report'
                publishHTML([allowMissing: false,
                             alwaysLinkToLastBuild: true,
                             keepAll: true,
                             reportDir: 'reports\\html_reports',
                             reportFiles: 'report.html',
                             reportName: 'Pytest HTML Report'])
                
                echo 'Publishing Allure report'
                allure([
                    includeProperties: false,
                    jdk: '',
                    reportBuildPolicy: 'ALWAYS',
                    results: [[path: 'reports\\allure-results']]
                ])
            }
        }
    }

    post {
        always {
            echo 'Cleaning workspace'
            cleanWs()
        }
        success {
            echo 'Build completed successfully!'
        }
        failure {
            echo 'Build failed! Check console output.'
        }
    }
}
