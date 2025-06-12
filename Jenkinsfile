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
//                     echo "📋 Running tests with GitHub Checks enabled..."
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
//                             echo "Python tests failed"
//                             error("Test run failed: ${err}")
//                         }
//                     }
//                 }
//             }
//         }
//     }

//     post {
//         success {
//             echo "Pipeline completed successfully for branch: ${BRANCH_NAME}"
//         }
//         failure {
//             echo "Pipeline failed for branch: ${BRANCH_NAME}"
//         }
//     }
// }



// this is useful script to run pytest in a multibranch pipeline with branch filtering


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
                        currentBuild.result = 'SUCCESS' // Set build result to SUCCESS
                        error("Branch ${BRANCH_NAME} is not allowed, skipping the build.") // Terminate pipeline with a custom error message
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
                    withChecks(name: 'Python Tests') {
                        def testResult
                        try {
                            // Execute the shell commands and capture both their standard output (stdout)
                            // and their exit status.
                            // 'set -e' is removed here because we want to explicitly handle
                            // non-zero exit codes from pytest and parse its output, rather than
                            // having the shell script immediately exit.
                            testResult = sh(script: '''
                                python3 -m venv venv
                                . venv/bin/activate
                                python --version
                                pip install --upgrade pip
                                pip install pytest
                                pip list
                                pytest tests/test_calculator_logic.py
                            ''', returnStdout: true, returnStatus: true)

                            // If testResult.status is non-zero, it indicates that
                            // pytest (or a preceding command) exited with an error.
                            if (testResult.status != 0) {
                                echo "Python tests or setup failed with exit status: ${testResult.status}"
                                def failureDetails = "A Python test failed. Check the full console output for details."
                                def lines = testResult.stdout.split('\n')
                                def foundSpecificFailure = false

                                // --- Advanced Parsing of Pytest Output ---
                                // Pytest often uses a series of underscores to delineate individual test failure sections.
                                // We'll try to find the test function name and the assertion error.
                                for (int i = 0; i < lines.size(); i++) {
                                    def line = lines[i].trim()
                                    // Example: ___________________________ test_addition_failure ____________________________
                                    if (line.startsWith("__________") && line.endsWith("__________")) {
                                        def testNameMatch = (line =~ /_______+\s*(test_[^\s]+)\s*_______+/)
                                        if (testNameMatch.find()) {
                                            def testName = testNameMatch.group(1)
                                            def assertionLine = ""
                                            // Search a few lines after the test name for "E " which typically denotes an assertion error
                                            for (int k = i + 1; k < Math.min(i + 10, lines.size()); k++) { // Look up to 10 lines
                                                def currentSubLine = lines[k].trim()
                                                if (currentSubLine.startsWith("E ")) { // This is the assertion error line
                                                    assertionLine = currentSubLine.substring(2).trim() // Remove "E " prefix
                                                    break
                                                }
                                                // Stop if we hit another section or a significant empty block
                                                if (currentSubLine.startsWith("===") || currentSubLine.startsWith("_________") || (currentSubLine.isEmpty() && k > i + 2)) {
                                                    break
                                                }
                                            }
                                            if (assertionLine) {
                                                failureDetails = "Test '${testName}' failed: ${assertionLine}"
                                                foundSpecificFailure = true
                                                break // Specific failure found, no need to parse further
                                            }
                                        }
                                    }
                                }

                                // --- Fallback Parsing for General Failure Summary ---
                                // If specific parsing didn't find details (e.g., if multiple tests failed,
                                // or output format is slightly different), look for the concise "FAILED" summary line.
                                if (!foundSpecificFailure) {
                                    for (line in lines) {
                                        line = line.trim()
                                        // Example: FAILED tests/test_calculator_logic.py::test_addition_failure - assert 4 == 5
                                        if (line.startsWith("FAILED") && line.contains("tests/test_calculator_logic.py")) {
                                            def match = (line =~ /FAILED (.*)/)
                                            if (match.find()) {
                                                failureDetails = "A test failed: ${match.group(1).trim()}"
                                                foundSpecificFailure = true
                                                break
                                            }
                                        }
                                    }
                                }
                                error("Test run failed: ${failureDetails}") // Terminate the pipeline with the custom error message
                            } else {
                                echo "Python tests passed successfully."
                            }
                        } catch (err) {
                            // This catch block will only be executed if the 'sh' command itself
                            // encounters a fundamental issue (e.g., syntax error in the shell script)
                            // or if there's an unexpected Groovy exception within this Jenkinsfile logic.
                            echo "An unexpected error occurred during test setup or execution: ${err}"
                            error("Pipeline execution failed unexpectedly: ${err}")
                        }
                    }
                }
            }
        }
    }

    post {
        success {
            echo "Pipeline completed successfully for branch: ${BRANCH_NAME}"
        }
        failure {
            echo "Pipeline failed for branch: ${BRANCH_NAME}"
        }
    }
}


