// pipeline {
//     agent any

//     environment {
//         BRANCH_NAME = "${env.BRANCH_NAME}"
//         IS_PR = false
//     }

//     stages {
//         stage('Determine Event Type') {
//             steps {
//                 script {
//                     // Determine if this is a PR build (for multibranch, use env.CHANGE_BRANCH)
//                     if (env.CHANGE_BRANCH) {
//                         IS_PR = true
//                         BRANCH_NAME = env.CHANGE_BRANCH
//                         echo "📦 Pull Request from branch: ${BRANCH_NAME}"
//                     } else if (env.BRANCH_NAME) {
//                         echo "🔁 Branch build: ${env.BRANCH_NAME}"
//                     } else {
//                         error("Unsupported event: Could not detect branch from environment")
//                     }

//                     // Allowed branches to build
//                     def allowedBranches = ['main', 'automation1', 'automation2']
//                     if (!allowedBranches.contains(BRANCH_NAME)) {
//                         echo "⚠️ Skipping branch ${BRANCH_NAME} as it is not in the allowed list."
//                         currentBuild.result = 'SUCCESS'
//                         error("Branch ${BRANCH_NAME} is not allowed, skipping the build.")
//                     }
//                 }
//             }
//         }

//         stage('Checkout Code') {
//             steps {
//                 checkout scm
//             }
//         }

//         stage('Set up Python & Run Tests') {
//             steps {
//                 sh '''
//                     set -e
//                     python3 -m venv venv
//                     . venv/bin/activate
//                     python --version
//                     pip install --upgrade pip
//                     pip install pytest
//                     pip list
//                     pytest tests/test_calculator_logic.py
//                 '''
//             }
//         }
//     }

//     post {
//         success {
//             echo "✅ Pipeline completed successfully for branch: ${BRANCH_NAME}"
//         }
//         failure {
//             echo "❌ Pipeline failed for branch: ${BRANCH_NAME}"
//         }
//     }
// }


pipeline {
    agent any

    environment {
        BRANCH_NAME = "${env.BRANCH_NAME}"
        IS_PR = false
        FAILURE_REASON = ''
    }

    stages {
        stage('Determine Event Type') {
            steps {
                script {
                    // Determine if this is a PR build (for multibranch, use env.CHANGE_BRANCH)
                    if (env.CHANGE_BRANCH) {
                        IS_PR = true
                        BRANCH_NAME = env.CHANGE_BRANCH
                        echo "📦 Pull Request from branch: ${BRANCH_NAME}"
                    } else if (env.BRANCH_NAME) {
                        echo "🔁 Branch build: ${env.BRANCH_NAME}"
                    } else {
                        error("Unsupported event: Could not detect branch from environment")
                    }

                    // Allowed branches to build
                    def allowedBranches = ['main', 'automation1', 'automation2']
                    if (!allowedBranches.contains(BRANCH_NAME)) {
                        echo "⚠️ Skipping branch ${BRANCH_NAME} as it is not in the allowed list."
                        currentBuild.result = 'SUCCESS'
                        error("Branch ${BRANCH_NAME} is not allowed, skipping the build.")
                    }
                }
            }
        }

        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Set up Python & Run Tests') {
            steps {
                script {
                    try {
                        sh '''
                            set +e
                            python3 -m venv venv
                            . venv/bin/activate
                            python --version
                            pip install --upgrade pip
                            pip install pytest
                            pip list
                            pytest tests/test_calculator_logic.py --tb=short > result.log
                            echo $? > exit_code.txt
                        '''

                        def exitCode = readFile('exit_code.txt').trim()
                        if (exitCode != '0') {
                            def resultLog = readFile('result.log')
                            def failedTestLines = resultLog.readLines().findAll { it.contains("FAILED") }
                            if (failedTestLines) {
                                env.FAILURE_REASON = "❌ Failed tests: " + failedTestLines.join(', ')
                            } else {
                                env.FAILURE_REASON = "❌ Tests failed. See result.log for more info."
                            }
                            error(env.FAILURE_REASON)
                        } else {
                            echo "✅ All tests passed."
                        }
                    } catch (err) {
                        if (!env.FAILURE_REASON) {
                            env.FAILURE_REASON = "❌ Test execution failed: ${err.getMessage()}"
                        }
                        error(env.FAILURE_REASON)
                    }
                }
            }
        }
    }

    post {
        success {
            echo "✅ Pipeline completed successfully for branch: ${BRANCH_NAME}"
        }
        failure {
            echo "❌ Pipeline failed for branch: ${BRANCH_NAME}"
            echo "Reason: ${env.FAILURE_REASON ?: 'Unknown Error'}"
        }
    }
}
