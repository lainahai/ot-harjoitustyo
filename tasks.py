from invoke import task

@task
def start(ctx, tablefile='src/test_table.tbl', vllfile='src/test_vll.vll'):
    ctx.run(f"python3 src/index.py {tablefile} {vllfile}", pty=True)

@task
def test(ctx):
  ctx.run("pytest src", pty=True)


@task
def coverage(ctx):
    ctx.run("coverage run --branch -m pytest src", pty=True)

@task(coverage)
def coverage_report(ctx):
    ctx.run("coverage html", pty=True)
