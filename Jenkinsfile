pipeline {
    agent any

    environment {
        // Azure Service Principal credentials from Jenkins credentials store
        AZURE_CLIENT_ID = credentials('AZURE_CLIENT_ID')
        AZURE_CLIENT_SECRET = credentials('AZURE_CLIENT_SECRET')
        AZURE_SUBSCRIPTION_ID = credentials('AZURE_SUBSCRIPTION_ID')
        AZURE_TENANT_ID = credentials('AZURE_TENANT_ID')

        FUNCTIONAPP_NAME = 'FunctionsAppHello'
        RESOURCE_GROUP = 'FunctionsAppHello_group'
        FUNCTIONAPP_PATH = '.' // Folder containing your function code
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/prabhgill02/PyFuncs'
            }
        }

    stages {
        stage('Install Azure CLI and Func Tools') {
            steps {
                bat '''
                    powershell -Command "Invoke-WebRequest -Uri https://aka.ms/installazurecliwindows -OutFile .\\AzureCLI.msi"
                    msiexec /i AzureCLI.msi /quiet

                    npm install -g azure-functions-core-tools@4 --unsafe-perm true
                    pip install -r %FUNCTIONAPP_PATH%\\requirements.txt
                '''
            }
        }

        stage('Azure Login') {
            steps {
                bat '''
                    az logout || exit 0
                    az login --service-principal ^
                        --username "%AZURE_CLIENT_ID%" ^
                        --password "%AZURE_CLIENT_SECRET%" ^
                        --tenant "%AZURE_TENANT_ID%"
                    az account set --subscription "%AZURE_SUBSCRIPTION_ID%"
                '''
            }
        }

        stage('Run Unit Tests') {
            steps {
                bat '''
                    pytest > test-output.txt || echo "Tests failed"
                '''
                // Archive test output
                archiveArtifacts artifacts: '%FUNCTIONAPP_PATH%/test-output.txt', fingerprint: true
            }
        }

        stage('Deploy to Azure') {
            steps {
                bat '''
                    func azure functionapp publish "%FUNCTIONAPP_NAME%"
                '''
            }
        }
    }

    post {
        always {
            bat 'az logout || exit 0'
        }
    }
}
