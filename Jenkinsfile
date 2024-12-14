pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                sh 'npm install'
                sh 'npm run build'
            }
        }
        stage('Deploy') {
            steps {
                sshPublisher(publishers: [
                  sshPublisherDesc(
                    configName: 'remote-server',
                    transfers: [
                      sshTransfer(
                        sourceFiles: '**/*',
                         remoteDirectory: './CBDC-project-deploy-swarm',
                        execCommand: 'touch 123'
                      )
                    ]
                  )
                ])
            }
        }
    }
}
