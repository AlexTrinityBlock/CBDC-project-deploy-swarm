pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                echo 'Build'
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
