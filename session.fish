. env/bin/activate.fish

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
    python tools.py
end
