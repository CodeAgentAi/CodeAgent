import codeagentai
from .fixtures import prepare_and_teardown  # noqa: F401


def test_agent_builder_job(prepare_and_teardown):
    data = prepare_and_teardown

    jobs = codeagent.AgentBuilderJob.list(agent_id=data["agent_id"])
    assert jobs.total_count == 1
    assert jobs.results[0].id == data["agent_builder_job_id"]

    job = codeagent.AgentBuilderJob.retrieve(data["agent_builder_job_id"])
    assert job.id == data["agent_builder_job_id"]


def test_build(prepare_and_teardown):
    data = prepare_and_teardown

    builds = codeagent.Build.list(agent_builder_job_id=data["agent_builder_job_id"])
    assert builds.total_count == 1
    assert builds.results[0].id == data["build_id"]

    build = codeagent.Build.retrieve(data["build_id"])
    assert build.id == data["build_id"]


def test_execution(prepare_and_teardown):
    data = prepare_and_teardown

    executions = codeagent.Execution.list(agent_id=data["agent_id"])
    assert len(executions.results) == 1
    assert executions.results[0].id == data["execution_id"]

    execution = codeagent.Execution.retrieve(data["execution_id"])
    assert execution.id == data["execution_id"]


def test_agent_executor_job(prepare_and_teardown):
    data = prepare_and_teardown

    codeagent.AgentExecutorJob.create(agent_id=data["agent_id"], payload={"foo": "bar"})

    jobs = codeagent.AgentExecutorJob.list(agent_id=data["agent_id"])
    assert len(jobs.results) == 2

    job = codeagent.AgentExecutorJob.retrieve(data["agent_executor_job_id"])
    assert job.id == data["agent_executor_job_id"]


def test_agent(prepare_and_teardown):
    data = prepare_and_teardown

    agent = codeagent.Agent.create(
        name="testagent2",
        script="def main():\n    print('hello world')\n",
        requirements="requests",
        env_vars="FOO=BAR",
        python_version="3.9",
    )
    assert codeagent.Agent.update(agent.id, name="updated").name == "updated"
    assert codeagent.Agent.list().total_count == 2
    assert codeagent.Agent.retrieve(agent.id).id == agent.id
    codeagent.Agent.delete(agent.id)
    assert codeagent.Agent.list().total_count == 1


def test_execute_agent(prepare_and_teardown):
    data = prepare_and_teardown

    agent = codeagent.Agent.retrieve(data["agent_id"])

    execution = agent.execute()
    assert type(execution) is codeagent.Execution

    agent_executor_job = agent.execute(wait=False)
    assert type(agent_executor_job) is codeagent.AgentExecutorJob
