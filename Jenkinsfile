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


// Import UUID for generating unique temporary file names
import java.util.UUID

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
                    // Check if the current build is a Pull Request based on environment variables
                    if (env.CHANGE_BRANCH) {
                        IS_PR = true
                        BRANCH_NAME = env.CHANGE_BRANCH
                        echo "📦 Pull Request from branch: ${BRANCH_NAME}"
                    } else if (env.BRANCH_NAME) { // If not a PR, check for a regular branch build
                        echo "🔁 Branch build: ${env.BRANCH_NAME}"
                    } else { // If neither is detected, it's an unsupported event
                        error("Unsupported event: Could not detect branch from environment")
                    }

                    // Define a list of allowed branches for the pipeline to run on
                    def allowedBranches = ['main', 'automation1', 'automation2']
                    if (!allowedBranches.contains(BRANCH_NAME)) {
                        echo "⚠️ Skipping branch ${BRANCH_NAME} as it is not in the allowed list."
                        // Set the current build result to SUCCESS so it doesn't appear as a failure in Jenkins,
                        // but still terminates the build with an informative message.
                        currentBuild.result = 'SUCCESS'
                        // Terminate the pipeline with a custom error message indicating the branch is not allowed
                        error("Branch ${BRANCH_NAME} is not allowed, skipping the build.")
                    }
                }
            }
        }

        stage('Checkout Code') {
            steps {
                // Standard SCM checkout step to get the repository code
                checkout scm
            }
        }

        stage('Set up Python & Run Tests') {
            steps {
                script {
                    echo "📋 Running tests with GitHub Checks enabled..."
                    // Use withChecks to integrate build status and details with GitHub Checks API
                    withChecks(name: 'Python Tests') {
                        def testStatus = 0   // Variable to hold the exit status of the pytest command (an Integer)
                        def testOutput = ""  // Variable to hold the full output of the pytest command (a String)
                        def outputFileName = "pytest_output_${UUID.randomUUID().toString()}.txt" // Unique temp file name

                        try {
                            // Clear or create the temporary file before starting
                            sh "> ${outputFileName}"

                            // Execute all Python setup and test commands within a single shell script.
                            // We redirect all pytest output (stdout and stderr) to a temporary file.
                            // We capture pytest's exit code and then ensure the shell script exits with that same code,
                            // allowing 'returnStatus: true' to correctly capture it.
                            testStatus = sh(script: """
                                python3 -m venv venv
                                . venv/bin/activate

                                # Verify Python version
                                python --version

                                # Upgrade pip and install pytest
                                pip install --upgrade pip
                                pip install pytest
                                pip list

                                # Run pytest, redirecting all output (stdout and stderr) to the temporary file.
                                # Capture pytest's exit code for later use.
                                pytest tests/test_calculator_logic.py > ${outputFileName} 2>&1
                                pytest_exit_code=\$?

                                # Deactivate the virtual environment. '|| true' ensures the script doesn't fail
                                # if deactivate encounters an issue (e.g., if it's already deactivated).
                                deactivate || true

                                # Exit the shell script with the actual exit code from pytest.
                                # This is the status that Jenkins' 'sh' step with 'returnStatus: true' will capture.
                                exit \$pytest_exit_code
                            """, returnStatus: true) // Captures the final exit status of the shell script

                            // After the shell command completes, read the content of the temporary file
                            // into a Groovy variable for parsing.
                            testOutput = readFile outputFileName
                            
                            // Clean up the temporary file to avoid clutter in the workspace.
                            sh "rm -f " + outputFileName

                            echo "Pytest raw output captured:\n${testOutput}"
                            echo "Pytest exit status: ${testStatus}"

                            // Check if the captured testStatus indicates a failure (non-zero exit code)
                            if (testStatus != 0) {
                                echo "Python tests or setup failed with exit status: ${testStatus}"
                                def failureDetails = "A Python test failed. Check the full console output for details."
                                // Split the captured output into lines for parsing
                                def lines = testOutput.split('\n')
                                def foundSpecificFailure = false

                                // --- Advanced Parsing of Pytest Output ---
                                // This section attempts to extract specific test failure details
                                // by looking for pytest's typical failure report format.
                                for (int i = 0; i < lines.size(); i++) {
                                    def line = lines[i].trim()
                                    // Pytest failure sections are often delimited by lines of underscores
                                    // e.g., "___________________________ test_my_feature_failure ____________________________"
                                    if (line.startsWith("__________") && line.endsWith("__________")) {
                                        // Use a regular expression to extract the test function name
                                        def testNameMatch = (line =~ /_______+\s*(test_[^\s]+)\s*_______+/)
                                        if (testNameMatch.find()) {
                                            def testName = testNameMatch.group(1)
                                            def assertionLine = ""
                                            // Search a few lines after the test name for the assertion error line,
                                            // which typically starts with "E "
                                            for (int k = i + 1; k < Math.min(i + 10, lines.size()); k++) { // Look up to 10 lines max
                                                def currentSubLine = lines[k].trim()
                                                if (currentSubLine.startsWith("E ")) { // Found the assertion error line
                                                    assertionLine = currentSubLine.substring(2).trim() // Remove "E " prefix
                                                    break // Stop searching for this test's assertion
                                                }
                                                // Stop if we hit another test section, a summary, or a large empty block
                                                if (currentSubLine.startsWith("===") || currentSubLine.startsWith("_________") || (currentSubLine.isEmpty() && k > i + 2)) {
                                                    break
                                                }
                                            }
                                            if (assertionLine) {
                                                // Construct a detailed failure message
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
                                        // Look for the final summary line indicating a failure,
                                        // e.g., "FAILED tests/test_calculator_logic.py::test_addition_failure - assert 4 == 5"
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
                                // Terminate the pipeline with the custom, dynamic error message
                                error("Test run failed: ${failureDetails}")
                            } else {
                                echo "Python tests passed successfully."
                            }
                        } catch (err) {
                            // This catch block will only be executed if there's an unexpected Groovy exception
                            // within this Jenkinsfile logic itself (e.g., issues with 'readFile'),
                            // or a fundamental error with the 'sh' command execution.
                            echo "An unexpected error occurred during test setup or execution: ${err}"
                            error("Pipeline execution failed unexpectedly: ${err}")
                        }
                    }
                }
            }
        }
    }

    // Post-build actions based on the overall pipeline result
    post {
        success {
            echo "Pipeline completed successfully for branch: ${BRANCH_NAME}"
        }
        failure {
            echo "Pipeline failed for branch: ${BRANCH_NAME}"
        }
    }
}
