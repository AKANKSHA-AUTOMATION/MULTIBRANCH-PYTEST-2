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

        stage('Set up Python') {
            steps {
                script {
                    sh '''
                        set -e
                        python3 -m venv venv
                        . venv/bin/activate
                        python --version
                        pip install --upgrade pip
                        pip install pytest
                        pip list
                    '''
                }
            }
        }

        stage('Run Addition Tests') {
            steps {
                script {
                    withChecks(name: 'Addition Logic Check') {
                        try {
                            sh '''
                                . venv/bin/activate
                                pytest tests/test_calculator_logic.py -k test_addition_positive
                            '''
                        } catch (err) {
                            echo "❌ Addition logic check failed."
                            error("Addition test failed.")
                        }
                    }
                }
            }
        }

        stage('Run Subtraction Tests') {
            steps {
                script {
                    withChecks(name: 'Subtraction Logic Check') {
                        try {
                            sh '''
                                . venv/bin/activate
                                pytest tests/test_calculator_logic.py -k test_subtraction_positive
                            '''
                        } catch (err) {
                            echo "❌ Subtraction logic check failed."
                            error("Subtraction test failed.")
                        }
                    }
                }
            }
        }

        // Add more `withChecks` blocks for other types of tests
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
