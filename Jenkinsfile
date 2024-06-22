pipeline {
   agent any

    stages {

        stage('Clone repo') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh """
                python3 -m venv venv
                . venv/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                pip install unittest-xml-reporting
                """
            }
        }

        stage('Run Tests') {
            steps {
                sh """
                . venv/bin/activate
                python3 -m xmlrunner discover -s tests -o test-reports
                """
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'test-reports/*.xml', allowEmptyArchive: true
            junit 'test-reports/*.xml'
        }
        success {
            echo 'Tests passed successfully!'
        }
        failure {
            echo 'Some tests failed.'
        }
    }
}
