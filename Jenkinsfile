pipeline {
    agent any

    environment {
        PATH = "/usr/local/bin:${PATH}"
        REPO_URL = 'https://github.com/Astrodynamic/DNA_Analazer-Algorithms-for-working-with-text-in-CPP.git'
        DESTINATION_FOLDER = '/Users/belekayazbekov/Desktop/test'
        BUILD_DIRECTORY = "${DESTINATION_FOLDER}"  // Define a build directory
        SHOULD_ENCRYPT = 'true' // or 'false' based on your requirement
        SHOULD_COMPRESS = 'true' // or 'false' based on your requirement
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

        stage('Compile Code') {
            steps {
                script {
                    echo "Compiling C code..."
                    sh "python3 compile.py ${DESTINATION_FOLDER} --encrypt --compress"
                }
            }
        }

        // Additional stages like 'Test', 'Deploy' etc. can be added here as needed.
    }

    post {
        always {
            // This will always run regardless of success or failure.
            archiveArtifacts artifacts: '*', allowEmptyArchive: true
        }
        success {
            echo 'Job succeeded!'
        }
        failure {
            echo 'Job failed!'
        }
    }
}
