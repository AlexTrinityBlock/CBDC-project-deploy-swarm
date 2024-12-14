pipeline {
  agent any
  stages {
    stage('Build') {
      steps {
        // 建置程式碼的步驟，例如：
        echo "Local echo"
      }
    }
    stage('Remote Echo') {
      steps {
        sshPublisher(publishers: [
          sshPublisherDesc(configName: 'vm', 
                           transfers: [
                             sshTransfer(execCommand: "touch /root/iam-here")
                           ]
        ])
      }
    }
  }
}
