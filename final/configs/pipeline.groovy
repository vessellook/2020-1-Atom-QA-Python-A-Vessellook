properties([disableConcurrentBuilds()])

pipeline {
	agent {
		label 'master'
	}

	options {
		buildDiscarder(logRotator(numToKeepStr: '3'))
		timestamps()
	}

	stages {
		stage("Build") {
			steps {
				echo 'no building..'
			}
		}
	
		stage("Create configs") {
			steps {
				dir('final') {
					sh 'cp .env_template .env'
					sh 'echo "PROJECT_PATH=$WORKSPACE/final" >> .env'
					sh 'echo "COMPOSE_PROJECT_PATH=${HOST_JENKINS_HOME:-"/var"}$(echo $WORKSPACE | cut -c5-)/final" >> .env'
					sh 'echo "SCREENSHOTS_DIR=$WORKSPACE/final/mount/screenshots" >> .env'
					sh 'echo "VIDEO_DIR=$WORKSPACE/final/mount/videos" >> .env'
					sh 'echo "VIDEO_DIR=$WORKSPACE/final/mount/videos" >> .env'
					sh 'if ! test -z ${HOST_JENKINS_HOME}; then \
						echo "SELENOID_HOST=selenoid" >> .env; \
						echo "PROXY_HOST_UI=proxy" >> .env; \
						echo "PROXY_HOST_API=proxy" >> .env; \
						echo "MOCK_PORT=5000" >> .env; \
						echo "MOCK_HOST=mock" >> .env; \
						echo "MYSQL_HOST=mysql" >> .env; \
					fi'
					sh 'scripts/install.sh'
				}
			}
		}

		stage("Start containers") {
			steps {
				dir('final') {
					sh 'docker-compose down || exit 0'
					sh 'docker-compose up -d'
					sh 'while test -z $(docker-compose ps |sed -n -E "/selenoid.*Up/p"); do sleep 5; done'
					sh 'sleep 5'
				}
			}
		}

		stage("Testing") {
			steps {
				dir('final/builds/tests/code') {
					sh 'pytest \
					-c=$WORKSPACE/final/builds/tests/code/pytest.ini \
					--rootdir=$WORKSPACE/final/builds/tests/code \
					--confcutdir=$WORKSPACE/final/builds/tests/code \
					--numprocesses=3 --showlocals --capture=no \
					--verbosity=2 -rA -m enable_video \
					--alluredir=$WORKSPACE/final/mount/allure-results\
					$WORKSPACE/final/builds/tests/code/'
				}
			}
		}
	}

	post {

		always {
			allure([
				reportBuildPolicy: 'ALWAYS',
				results: [[path: '$WORKSPACE/final/mount/allure-results']]
			])
		}
	}
}

