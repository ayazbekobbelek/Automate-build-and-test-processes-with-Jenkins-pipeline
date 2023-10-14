pipeline {
    agent any

    environment {
        REPO_URL = 'https://github.com/Astrodynamic/DNA_Analazer-Algorithms-for-working-with-text-in-CPP.git'
        DESTINATION_FOLDER = '/Users/belekayazbekov/Desktop/test'
    }

    stages {
        stage('Clone/Update Repository') {
            steps {
                script {
                    // Check if repo already cloned
                    if (fileExists("${DESTINATION_FOLDER}/.git")) {
                        echo "Repository exists, updating..."
                        sh "python3 sync.py update ${DESTINATION_FOLDER}"
                    } else {
                        echo "Cloning repository..."
                        sh "python3 sync.py clone ${REPO_URL} ${DESTINATION_FOLDER}"
                    }
                }
            }
        }
        // Additional stages like 'Build', 'Test', 'Deploy' etc. can be added here as needed.
    }

    post {
        success {
            echo 'Job succeeded!'
        }
        failure {
            echo 'Job failed!'
        }
    }
}
