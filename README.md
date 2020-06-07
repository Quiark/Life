# Life

This is a personal 'social network' - a place where you can share your life experiences with
your closest people. It is completely hosted and owned by you, without advertising, privacy
leaks or manipulation by advertisers or platform.

In short it is your **Life** and yours only.

This software is 

* **PRIVATE** - no public posts are supported (but you are still trusting your cloud provider)
* **NOT SCALABLE** - it's not about increasing engagement or having as many friends as possible

## Running things

```
npm install
cd ui
./node_modules/webpack-cli/bin/cli.js
./node_modules/webpack-dev-server/bin/webpack-dev-server.js

cd api
../env/bin/python use_flask.py
```

## python environment

Since the lambda runtime is py3.6, we need to install that version locally. One way to do that 
is using nix. In a `shell.nix` file we require the attribute `nixpkgs.python36Full` and then
create a venv from that

```
python -m venv env36
. env36/bin/activate
pip install -r requirements.txt
```

## image resizer lambda

To build the zip, use this:

`npm pack`

Manually built zip cannot be used because files should have read for all permissions.

After upgrading to Nodejs12 runtime, a layer with imagemagick binaries needs to be added. The
one pre-built by the `aws-lambda-image` authors works.
