pipeline {
    agent any

    parameters {
        booleanParam(name: 'ENCRYPT', defaultValue: false, description: 'Enable encryption')
        booleanParam(name: 'COMPRESS', defaultValue: false, description: 'Enable compression')
    }

    environment {
        PATH = "/usr/local/bin:${PATH}"
        REPO_URL = 'https://github.com/Astrodynamic/DNA_Analazer-Algorithms-for-working-with-text-in-CPP.git'
        DESTINATION_FOLDER = '/Users/belekayazbekov/Desktop/test'
        BUILD_DIRECTORY = "${DESTINATION_FOLDER}/build" // Ensure this is a separate build directory
    }

    stages {
        stage('Clone/Update Repository') {
            steps {
                script {
                    // Check if the repo already cloned
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
                    // Construct compile command with optional flags
                    def compileCommand = "python3 compile.py ${DESTINATION_FOLDER} ${BUILD_DIRECTORY}"
                    if (params.ENCRYPT) {
                        compileCommand += " --encrypt"
                    }
                    if (params.COMPRESS) {
                        compileCommand += " --compress"
                    }
                    // Run the compile command
                    sh compileCommand
                }
            }
        }

        // Additional stages like 'Test', 'Deploy' etc. can be added here as needed.
    }

    post {
        always {
            // This will always run regardless of success or failure.
            archiveArtifacts artifacts: '**/build/**', allowEmptyArchive: true
        }
        success {
            echo 'Job succeeded!'
        }
        failure {
            echo 'Job failed!'
        }
    }
}
