pipeline {
    agent any

    environment {
        PYTHON = 'C:\\Users\\admin\\AppData\\Local\\Programs\\Python\\Python312\\python.exe'
        WORKSPACE_DIR = "${env.WORKSPACE}"
        ALLURE_RESULTS = "${env.WORKSPACE}\\reports\\allure_results"
        ALLURE_REPORT_DIR = "${env.WORKSPACE}\\allure-report"
        HTML_REPORT = "${env.WORKSPACE}\\reports\\html_reports\\report.html"
    }

    stages {

        stage('Clean Workspace') {
            steps {
                deleteDir()
            }
        }

        stage('Checkout Code') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/vinay-k94/pytest_framework_project.git',
                    credentialsId: 'github-creds'
            }
        }

        stage('Install Dependencies') {
            steps {
                bat "\"${PYTHON}\" -m pip install --upgrade pip"
                bat "\"${PYTHON}\" -m pip install -r requirements.txt"
            }
        }

        stage('Run Pytest') {
            steps {
                echo 'Running pytest with Allure and HTML reports'
                // Run tests but continue even if some fail
                bat "\"${PYTHON}\" -m pytest \"${WORKSPACE_DIR}\\tests\" --alluredir=\"${ALLURE_RESULTS}\" --html=\"${HTML_REPORT}\" --self-contained-html || exit 0"
            }
        }

        stage('Generate Allure Report') {
            steps {
                echo 'Generating Allure report'
                catchError(buildResult: 'UNSTABLE', stageResult: 'UNSTABLE') {
                    bat "\"C:\\ProgramData\\Jenkins\\.jenkins\\tools\\ru.yandex.qatools.allure.jenkins.tools.AllureCommandlineInstallation\\AllureCommand\\bin\\allure.bat\" generate \"${ALLURE_RESULTS}\" -o \"${ALLURE_REPORT_DIR}\" --clean"
                }
            }
        }

        stage('Publish Reports') {
            steps {
                // Publish HTML report
                publishHTML([
                    allowMissing: false,
                    alwaysLinkToLastBuild: true,
                    keepAll: true,
                    reportDir: "${WORKSPACE_DIR}\\reports\\html_reports",
                    reportFiles: 'report.html',
                    reportName: 'HTML Test Report'
                ])
                
                // Publish Allure report
                allure([
                    includeProperties: false,
                    jdk: '',
                    results: [[path: "${ALLURE_RESULTS}"]],
                    reportBuildPolicy: 'ALWAYS'
                ])
            }
        }
    }

    post {
        always {
            echo 'Cleaning workspace after build'
            deleteDir()
        }
        unstable {
            echo 'Build is unstable due to test failures'
        }
        failure {
            echo 'Build failed due to errors outside of tests'
        }
    }
}
