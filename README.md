# AmigoProxy

A proxy for transportation devices.


## Running with Docker

This is the easiest way to get AmigoProxy running, specially on a development environment.

1. Install [docker](https://docs.docker.com/engine/installation/) and [docker-compose](https://docs.docker.com/compose/install/)
2. Clone this repository: `git clone git@github.com:amigocloud/amigoproxy.git`
3. Create a secrets file:
```bash
cd amigoproxy/src/amigoproxy
cp secrets.py.dist secrets.py
```
4. Edit the `secrets.py` with your favorite editor and
Set an appropriate [`SECRET_KEY`](https://docs.djangoproject.com/en/1.8/ref/settings/#secret-key).
You can leave `HIPCHAT_TOKEN` variable empty.
5. If you wish to change the broker's username and/or password, do so in `docker-compose.yml`
(lines 68-69). Then reflect the changes in lines 55-56 and in the `secrets.py` file.
6. Run `docker-compose up -d` to bring up all the services.
7. Create database tables and superuser:
```bash
docker exec -ti amigoproxy_django_1 manage.py syncdb
```
8. That's it. You can now open the dashboard at `http://localhost`

## Running on production

Additionally to the steps presented above, you might want to disable `DEBUG` mode.
To do so, either edit `src/amigoproxy/settings.py`
or create a new file `src/amigoproxy/local_settings.py` and set the `DEBUG = False` there.
You can use this file to tweak any other setting you want.

## Usage

Let's first define the purpose of each term presented in the dashboard:

1. **Targets**: The services that will receive the requests (described by a name and an URL).
2. **Sources**: The devices that send data (for example, buses).
3. **Groups**: Groups of targets.

Devices can send data to the proxy through a `POST` request to the main URL, for instance:
`https://proxy.amigocloud.com`

Once devices start sending data to the proxy, you will be able to search them by their ID.
Then you can then assign them Groups (of Targets) that will recive data from that particular
device.

Optionally, you can set a Group to be default, meaning that all its Targets will receive
data coming from all the devices.
