pipeline {
    agent any

    parameters {
        booleanParam(name: 'ENCRYPT', defaultValue: false, description: 'Enable encryption')
        booleanParam(name: 'COMPRESS', defaultValue: false, description: 'Enable compression')
    }

    environment {
        PATH = "/usr/local/bin:${PATH}"
        REPO_URL = 'https://github.com/ayazbekobbelek/DNA_Analazer-Algorithms-for-working-with-text-in-CPP.git'
        DESTINATION_FOLDER = '/Users/belekayazbekov/university'
        BUILD_DIRECTORY = "${DESTINATION_FOLDER}/build" // Ensure this is a separate build directory
        TESTS_DIRECTORY = "${DESTINATION_FOLDER}/test"
        TEST_BUILD_DIRECTORY = "${BUILD_DIRECTORY}/test/build"
        STATIC_ANALYSIS_LOG_FILE = "${BUILD_DIRECTORY}/static_analysis_results.log"
    }

    stages {
        stage('Setup python environment') {
            steps {
                script {
                    sh 'pip install --upgrade google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client'
                }
            }
        }
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
        stage('Run Tests') {
            steps {
                script {
                    echo "Running unit tests..."
                    // Assuming the test script is named run_tests.py and is located in the same directory as compile.py
                    def testCommand = "python3 run_tests.py ${TESTS_DIRECTORY} ${BUILD_DIRECTORY}"
                    sh testCommand
                }
            }
        }

        stage('Run Static Code Analysis') {
            steps {
                script {
                    echo "Running static code analyzer"
                    sh "python3 run_static_analysis.py ${DESTINATION_FOLDER} ${STATIC_ANALYSIS_LOG_FILE}"
                }
            }
        }

    }

    post {
        always {
        // This will always run regardless of the success or failure.
        archiveArtifacts artifacts: '**/build/**', allowEmptyArchive: true
    }
    success {
        script {
            def emailSubject = "Build Successful"
            def emailBody = "The build completed successfully. Check the artifacts for details."
            sendEmailNotification(emailSubject, emailBody, "${STATIC_ANALYSIS_LOG_FILE}")
        }
    }
    failure {
        script {
            def emailSubject = "Build Failed"
            def emailBody = "The build failed. Please check the Jenkins logs for more information."
            sendEmailNotification(emailSubject, emailBody, "${STATIC_ANALYSIS_LOG_FILE}")
        }
    }
}
}

def sendEmailNotification(String subject, String body, String attachmentPath = '') {
    def pythonEmailScript = "send_email.py"
    def recipientEmail = 'developer.belek@gmail.com'  // Set the recipient's email
    def command = "python3 ${pythonEmailScript} '${subject}' '${body}' '${recipientEmail}'"

    if (attachmentPath) {
        command += " --attachment '${attachmentPath}'"
    }

    sh command
}

