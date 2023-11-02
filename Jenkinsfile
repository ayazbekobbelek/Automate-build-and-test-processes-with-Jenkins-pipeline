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
                    sh "python3 run_static_analysis.py ${DESTINATION_FOLDER}"
                }
            }
        }


        // Additional stages like 'Test', 'Deploy' etc. can be added here as needed.
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
                sendEmailNotification(emailSubject, emailBody)
            }
        }
        failure {
            script {
                def emailSubject = "Build Failed"
                def emailBody = "The build failed. Please check the Jenkins logs for more information."
                sendEmailNotification(emailSubject, emailBody)
            }
        }
    }
}

def sendEmailNotification(String subject, String body) {
    emailext (
        subject: subject,
        body: body,
        recipientProviders: [[$class: 'DevelopersRecipientProvider']],
        to: 'ayazbekov2002@gmail.com', // replace with actual recipient
        replyTo: 'jenkins@example.com' // replace with actual reply-to address
    )
}
