. env36/bin/activate.fish

function ensuredir
    set want $argv[1]
    if test (basename $PWD) != $want
        cd $want
    end
end

function api_server
    ensuredir api
    python use_flask.py
end

function frontend_server
    ensuredir ui
    npm run serve
end

function notebook
    jupyter notebook
end

function dynamodb
    python tools.py dynamodb
end

function ui_build
    # requires the python env
    set -x API_LOCAL false
    python tools.py exportconfig

    cd ui
    npm run build

    cd ..
    cp ui/dist/bundle.js api/bundle.js
end

function editor
    nvim -S session.vim
end

function help_session
    echo dynamodb  // run local version of dynamodb for development
    echo notebook
    echo frontend_server
    echo api_server
    echo ui_build // build production frontend package, later deploy with now
    echo editor
end


help_session
