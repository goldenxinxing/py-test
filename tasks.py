from invoke import Collection, task


@task(help={'name': "Name of the person to say hi to."})
def hi(c, name):
    """Say hi to someone."""
    print("Hi %s!" % name)


@task()
def sw(c):
    r = c.run("swcli model list")
    print(r)

# This task & collection could just as easily come from
# another module somewhere.
# @task
# def mytask(c):
#     print(type(c))
#     print(c['conflicted'])
#
#
# inner = Collection('inner', mytask)
# inner.configure({'conflicted': 'default value'})
#
# # Our project's root namespace.
# ns = Collection(inner)
# ns.configure({'conflicted': 'override value'})
