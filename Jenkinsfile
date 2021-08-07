import jenkins.plugins.git.*;
import groovy.json.JsonOutput;

def repo = "use_case_1"
def buildNode = "x.x.x.x"
def supportedBranches = ['master']
def github_url = 'https://github.com'

node(buildNode) {
    def changedDirs
    def commit_id
    def isBuilt = 'failure'
    def currentBuild.result = 'SUCCESS'
    def status
	stage "checkout"
	dir('/build'){
		checkout scm
		changedDirs = sh(returnStdout: true, script: "git diff-tree --first-parent -m --name-only HEAD | awk 'NR>1'").trim().readLines()
		commit_id = sh(returnStdout: true, script: "git rev-parse --short HEAD").trim()
		changedDirs.removeAll(['README.md', 'Jenkinsfile'] as Object[])

	    stage "unittest"

        if(supportedBranches.contains(env.BRANCH_NAME))  {
            try {
                echo "Unit test is started for ${env.BRANCH_NAME} in ${env.NODE_NAME}"
                // code for unit test here
                status = "success"
            } catch(Exception e){
                echo 'ERROR: Something failed! please check below error message '
                status = "failure"
                print "ERROR: : "+e.toString()
                currentBuild.result = 'FAILURE'
            }finally {
                print "Status: "+status
                if (status == 'success'){
                    echo "DEBUG: Going to build rpm"
                } else {
                    print "No new package has been built, Unit test cases are Failed for ${env.BRANCH_NAME}"
                    return
                }
            }
        } else {
            echo "DEBUG: Not supported for ${env.BRANCH_NAME} branch, only MASTER branch is allowed"
            return
        }

        stage "Build"

        if(!supportedBranches.contains(env.BRANCH_NAME)){
            print "${env.BRANCH_NAME} doesn't support build"
            deleteDir()
            return
        }else{
            try {
                print  "Going to build package for ${env.BRANCH_NAME} branch"
                sh "python3 setup.py"
                sh "mv dist/helloworld.app helloworld_${BUILD_NUMBER}_${BUILD_ID}.app"
                isBuilt = 'success'            
            } catch(Exception e){
                echo 'ERROR: Something failed! please check below error message '
                isBuilt = 'failure'
                print "ERROR: : "+e.toString()
                currentBuild.result = 'FAILURE'
            }
        }

        stage "Deploy"
        if(isBuilt== 'success'){
            try {
            if(env.BRANCH_NAME == 'master'){
            	//sample from jfrog doc.
            	sh "jfrog rt u helloworld_${BUILD_NUMBER}_${BUILD_ID}.app my-repository/my/new/artifact/directory/ --user=myUser --password=myP455w0rd!"
            }
                buildDeployed = 'success'
            } catch(Exception e){
                echo 'ERROR: Something failed! please check below errors message running ansible deploy again'
                print "ERROR: : "+e.toString()
                buildDeployed = 'failure'
                print "ERROR: : "+e.toString()
                currentBuild.result = 'FAILURE'
            }

        }else{
            print "No new package has been built, so deployment isn't required"
        }
	}
}
