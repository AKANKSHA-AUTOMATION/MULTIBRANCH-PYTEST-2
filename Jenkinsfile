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
        BRANCH_NAME = "${env.BRANCH_NAME}"
        IS_PR = false
        GITHUB_TOKEN = credentials('github-pat-token') // 🔐 Add this to Jenkins Credentials
        FAILED_STAGE = ''
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

        stage('Run Python Tests') {
            steps {
                script {
                    try {
                        sh '''
                            set -e
                            python3 -m venv venv
                            . venv/bin/activate
                            pip install --upgrade pip
                            pip install pytest
                            pip list
                            pytest tests/test_calculator_logic.py
                        '''
                    } catch (err) {
                        FAILED_STAGE = 'Python Tests'
                        sendGitHubStatus("failure", "❌ ${FAILED_STAGE} failed")
                        error("Stopping pipeline due to failure in: ${FAILED_STAGE}")
                    }
                }
            }
        }
    }

    post {
        success {
            script {
                sendGitHubStatus("success", "✅ All checks passed")
                echo "✅ Pipeline completed successfully for branch: ${BRANCH_NAME}"
            }
        }
        failure {
            script {
                def message = FAILED_STAGE ? "❌ ${FAILED_STAGE} failed" : "❌ Pipeline failed"
                sendGitHubStatus("failure", message)
                echo "❌ Pipeline failed for branch: ${BRANCH_NAME}"
            }
        }
    }
}

// 🔧 Helper method to send GitHub commit status
def sendGitHubStatus(String state, String description) {
    def repo = sh(script: "git config --get remote.origin.url | sed -e 's/.*github.com[/:]//;s/.git\$//'", returnStdout: true).trim()
    def commitSha = env.GIT_COMMIT ?: sh(script: "git rev-parse HEAD", returnStdout: true).trim()
    def context = "continuous-integration/jenkins/pr-head"
    def apiUrl = "https://api.github.com/repos/${repo}/statuses/${commitSha}"

    sh """
        curl -s -X POST ${apiUrl} \
        -H "Authorization: token ${env.GITHUB_TOKEN}" \
        -H "Accept: application/vnd.github.v3+json" \
        -d '{
            "state": "${state}",
            "context": "${context}",
            "description": "${description}"
        }'
    """
}
