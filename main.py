from workflows.ProjectRunner import ProjectRunner


def main():
    project_runner = ProjectRunner('create_plots')
    project_runner.run()

main()