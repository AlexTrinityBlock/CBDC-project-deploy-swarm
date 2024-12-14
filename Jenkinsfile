pipeline {
  agent any
  stages {
    stage('Build') {
      steps {
        // 建置程式碼的步驟，例如：
        echo "Local echo"
        sh 'ls -al' // Use sh to execute shell commands
      }
    }
    stage('Remote Echo') {
      steps {
        sshPublisher(publishers: [
          sshPublisherDesc(configName: 'vm', 
                           transfers: [
                             sshTransfer(sourceFiles: '**/*',  // 傳輸當前目錄下的所有檔案和資料夾
                                         remoteDirectory: '/root/') 
                           ], //  不需要傳輸檔案
                           execCommand: 'touch /root/i-am-here') 
        ])
      }
    }
  }
}
