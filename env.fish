. env36/bin/activate.fish
help_session

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
    cd ui
    npm run build
    cd ..
    cp ui/dist/bundle.js api/bundle.js
    python tools.py ui_deploy
end

function help_session
    echo dynamodb
    echo notebook
    echo frontend_server
    echo api_server
    echo ui_deploy
end
