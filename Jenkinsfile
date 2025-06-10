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
//                     if (env.CHANGE_BRANCH) {
//                         IS_PR = true
//                         BRANCH_NAME = env.CHANGE_BRANCH
//                         echo "📦 Pull Request from branch: ${BRANCH_NAME}"
//                     } else if (env.BRANCH_NAME) {
//                         echo "🔁 Branch build: ${env.BRANCH_NAME}"
//                     } else {
//                         error("Unsupported event: Could not detect branch from environment")
//                     }

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
//                 script {
//                     withChecks(name: 'Python Tests') {
//                         try {
//                             sh '''
//                                 set -e
//                                 python3 -m venv venv
//                                 . venv/bin/activate
//                                 python --version
//                                 pip install --upgrade pip
//                                 pip install pytest
//                                 pip list
//                                 pytest tests/test_calculator_logic.py
//                             '''
//                         } catch (err) {
//                             // Print which test failed (you can enhance this using pytest output parsing)
//                             echo "❌ Python tests failed"
//                             error("Test run failed: ${err}")
//                         }
//                     }
//                 }
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
        // Initialize these; they will be overridden in the 'Determine Event Type' stage.
        // Use def or env. as needed. For global use across stages, env. is better.
        BRANCH_NAME_DETERMINED = "${env.BRANCH_NAME ?: env.CHANGE_BRANCH ?: 'unknown'}"
        IS_PULL_REQUEST = false
        IS_ALLOWED_BRANCH_FLAG = false // Flag to control stage execution
    }

    stages {
        stage('Initialize & Determine Event Type') {
            steps {
                script {
                    // Start a generic check for this initial setup phase
                    withChecks('Pipeline Initialization') {
                        if (env.CHANGE_BRANCH) {
                            env.IS_PULL_REQUEST = true
                            env.BRANCH_NAME_DETERMINED = env.CHANGE_BRANCH
                            echo "📦 Pull Request from branch: ${env.BRANCH_NAME_DETERMINED}"
                            // For PRs, the 'pr-head' check usually gets the detailed status
                            // The 'branch' check might still say 'cannot be built' if it's not applicable
                        } else if (env.BRANCH_NAME) {
                            echo "🔁 Branch build: ${env.BRANCH_NAME}"
                            env.BRANCH_NAME_DETERMINED = env.BRANCH_NAME
                        } else {
                            // This error will halt the pipeline if branch name can't be determined
                            error("Unsupported event: Could not detect branch from environment. Build aborted.")
                        }

                        def allowedBranches = ['main', 'automation1', 'automation2']
                        if (allowedBranches.contains(env.BRANCH_NAME_DETERMINED)) {
                            env.IS_ALLOWED_BRANCH_FLAG = true
                            echo "✅ Branch '${env.BRANCH_NAME_DETERMINED}' is in the allowed list."
                            // Update check status to success for this phase
                            currentBuild.currentResult = 'SUCCESS'
                        } else {
                            env.IS_ALLOWED_BRANCH_FLAG = false
                            echo "⚠️ Skipping pipeline for branch '${env.BRANCH_NAME_DETERMINED}' as it is not in the allowed list."
                            // Use AbortException to stop the pipeline gracefully without marking it as a failure
                            // The GitHub check for 'Pipeline Initialization' will show as 'Success' if it gets here,
                            // but subsequent stages will be skipped. You might want to update the check status explicitly.
                            manager.addWarning("Branch '${env.BRANCH_NAME_DETERMINED}' is not allowed. Pipeline will be skipped.")
                            // Force the build result to NOT_BUILT to show as skipped in Jenkins UI
                            currentBuild.result = 'NOT_BUILT'
                            throw new hudson.AbortException("Branch '${env.BRANCH_NAME_DETERMINED}' is not allowed, skipping the build.")
                        }
                    } // End withChecks 'Pipeline Initialization'
                }
            }
        }

        stage('Checkout Code') {
            // Only run this stage if the branch is allowed
            when { expression { env.IS_ALLOWED_BRANCH_FLAG == 'true' } }
            steps {
                // Ensure the checkout operation itself is wrapped in a check
                withChecks('Code Checkout') {
                    try {
                        checkout scm
                        echo "Code checked out successfully."
                        currentBuild.currentResult = 'SUCCESS' // Explicitly set success status for the check
                    } catch (err) {
                        echo "❌ Code checkout failed: ${err}"
                        // Use a custom message for the GitHub Check
                        manager.addError("Failed to checkout code: ${err.message}")
                        error("Failed to checkout code: ${err}") // Re-throw to fail the stage
                    }
                }
            }
        }

        stage('Set up Python & Run Tests') {
            // Only run this stage if the branch is allowed
            when { expression { env.IS_ALLOWED_BRANCH_FLAG == 'true' } }
            steps {
                // This 'withChecks' will specifically report for 'Python Tests'
                withChecks(name: 'Python Tests') {
                    try {
                        sh '''
                            set -e # Exit immediately if a command exits with a non-zero status.
                            echo "Setting up Python virtual environment..."
                            python3 -m venv venv
                            . venv/bin/activate
                            echo "Python version: $(python --version)"
                            echo "Upgrading pip..."
                            pip install --upgrade pip
                            echo "Installing pytest..."
                            pip install pytest
                            echo "Installed Python packages:"
                            pip list
                            echo "Running tests..."
                            pytest --junitxml=test-results.xml tests/test_calculator_logic.py
                            echo "Python tests completed successfully."
                        '''
                        // If pytest generates a JUnit XML report, publish it
                        junit 'test-results.xml'
                        currentBuild.currentResult = 'SUCCESS' // Explicitly set success status for the check
                    } catch (err) {
                        echo "❌ Python tests failed: ${err}"
                        // Add a specific message to the GitHub Check
                        manager.addError("Python tests failed. Check build logs for details.")
                        error("Test run failed: ${err}") // Re-throw to fail the stage
                    }
                }
            }
        }
    }

    post {
        always {
            // This runs regardless of build success/failure
            script {
                echo "Pipeline finished. Final status: ${currentBuild.result} for branch: ${env.BRANCH_NAME_DETERMINED}"
                // The withChecks blocks automatically send status updates,
                // but you can add final messages if needed.
            }
        }
        success {
            echo "✅ Pipeline completed successfully for branch: ${env.BRANCH_NAME_DETERMINED}"
        }
        failure {
            echo "❌ Pipeline failed for branch: ${env.BRANCH_NAME_DETERMINED}"
            // The individual `withChecks` will have already reported specific failures.
            // This global failure message is for Jenkins console output.
        }
        aborted {
            echo "🚫 Pipeline aborted for branch: ${env.BRANCH_NAME_DETERMINED}"
            // This will catch builds aborted due to the 'AbortException' for unallowed branches.
        }
        unstable {
            echo "⚠️ Pipeline unstable for branch: ${env.BRANCH_NAME_DETERMINED}"
        }
        notBuilt {
            echo "⏭️ Pipeline not built for branch: ${env.BRANCH_NAME_DETERMINED} (e.g., due to an unallowed branch)."
        }
    }
}