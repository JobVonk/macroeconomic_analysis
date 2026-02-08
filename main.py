from workflows.ProjectRunner import ProjectRunner


def main():
    project_runner = ProjectRunner('backtest')
    project_runner.run()

if __name__ == "__main__":
    main()