from invoke import task


@task
def start(ctx, tablefile="test_data/test_table.tbl", vllfile="test_data/test_vll.vll"):
  ctx.run(f"python3 src/main.py {tablefile} {vllfile}", pty=True)


@task
def test(ctx):
  ctx.run("pytest src", pty=True)


@task
def coverage(ctx):
  ctx.run("coverage run --branch -m pytest src", pty=True)


@task(coverage)
def coverage_report(ctx):
  ctx.run("coverage html", pty=True)
