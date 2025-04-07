pipeline {
    agent any

    environment {
        // Set your Azure Service Principal credentials (from Jenkins Credentials Store)
        AZURE_CLIENT_ID = credentials('AZURE_CLIENT_ID')
        AZURE_CLIENT_SECRET = credentials('AZURE_CLIENT_SECRET')
        AZURE_SUBSCRIPTION_ID = credentials('AZURE_SUBSCRIPTION_ID')
        AZURE_TENANT_ID = credentials('AZURE_TENANT_ID')
        FUNCTIONAPP_NAME = 'FunctionsAppHello'
        RESOURCE_GROUP = 'FunctionsAppHello_group'
    }

    stages {
        stage('Install Azure CLI and Func Tools') {
            steps {
                sh '''
                    curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
                    npm install -g azure-functions-core-tools@4 --unsafe-perm true
                '''
            }
        }

        stage('Azure Login') {
            steps {
                sh '''
                    az logout || true
                    az login --service-principal --username %AZURE_CLIENT_ID% --password %AZURE_CLIENT_SECRET% --tenant %AZURE_TENANT_ID%
                    az account set --subscription "AZURE_SUBSCRIPTION_ID"

                '''
            }
        }

        stage('Build Function App') {
            steps {
                sh 'func azure functionapp publish $FUNCTIONAPP_NAME --python'
            }
        }
    }

    post {
        always {
            sh 'az logout || true'
        }
    }
}
