. env36/bin/activate.fish

function api_server
    python use_flask.py
end

function frontend_server
    npm run serve
end

function notebook
    jupyter notebook
end

function dynamodb
    python tools.py dynamodb
end

function ui_deploy
    # requires the python env
    set -x API_LOCAL false
    python tools.py exportconfig

    cd ui
    npm run build

    cd ..
    cp ui/dist/bundle.js api/bundle.js
    #python tools.py ui_deploy
end

function help_session
    echo dynamodb
    echo notebook
    echo frontend_server
    echo api_server
    echo ui_deploy
end

help_session
