from fabric.api import (
    cd,
    env,
    run,
    sudo,
    task,
)

env.hosts = ['dev-dashboard02']
env.user = 'chango'

base_dir = '/apps/bfkac'


@task
def update():
    with cd(base_dir):
        run('find . -name "*.pyc" -delete')
        run('git pull --prune')


def status():
    return run('status bfkac', quiet=True).stdout


@task
def shutdown():
    if 'start/running' in status():
        sudo('stop bfkac')


@task
def startup():
    if 'stop/waiting' in status():
        sudo('start bfkac')


@task
def restart():
    shutdown()
    startup()


@task
def deploy():
    update()
    restart()
