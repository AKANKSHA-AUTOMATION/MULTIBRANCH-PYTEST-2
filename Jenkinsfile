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

// (main script)

// -----------------------------------------------------------------------------------
pipeline {
    agent any

    environment {
        BRANCH_NAME = "${env.BRANCH_NAME}"
        IS_PR = false
    }

    stages {
        stage('Determine Event Type') {
            steps {
                script {
                    if (env.CHANGE_BRANCH) {
                        IS_PR = true
                        BRANCH_NAME = env.CHANGE_BRANCH
                        echo "📦 Pull Request from branch: ${BRANCH_NAME}"
                    } else if (env.BRANCH_NAME) {
                        echo "🔁 Branch build: ${env.BRANCH_NAME}"
                    } else {
                        error("Unsupported event: Could not detect branch from environment")
                    }

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
                    echo "📋 Running tests with GitHub Checks enabled..."
                    // withChecks(name: 'Python Tests') {
                    //     try {
                    //         sh '''
                    //             set -e
                    //             python3 -m venv venv
                    //             . venv/bin/activate
                    //             python --version
                    //             pip install --upgrade pip
                    //             pip install pytest
                    //             pip list
                    //             pytest tests/test_calculator_logic.py
                    //         '''
                    //     } catch (err) {
                    //         // Print which test failed (you can enhance this using pytest output parsing)
                    //         echo "❌ Python tests failed"
                    //         error("Test run failed: ${err}")
                    //     }
                    // }
                    withChecks(name: 'Python Tests') {
                        try {
                            sh '''
                                set -e
                                python3 -m venv venv
                                . venv/bin/activate
                                pip install --upgrade pip
                                pip install pytest
                                pytest tests/test_calculator_logic.py --tb=short > result.log || true
                            '''

                            def failedTest = sh(script: "grep -E 'FAILED test_' result.log | cut -d ':' -f1", returnStdout: true).trim()
                            if (failedTest) {
                                error("Test failure: ${failedTest}")
                            }
                        } catch (err) {
                            echo "Python tests failed"
                            error("Python test failed: ${err}")
                        }
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
        }
    }
}




