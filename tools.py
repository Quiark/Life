import os
import sys
import subprocess

import api.config as config

# this should not depend on the virtualenv

subprocess.run('java -Djava.library.path=./DynamoDBLocal_lib -jar DynamoDBLocal.jar -sharedDb',
                shell=True, cwd=config.DYNAMODB_LOCAL_PATH)
