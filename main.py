from ui.console_ui import ConsoleUI


def main():
    print("Starting the supermarket POS system...")

    # 创建并运行控制台界面
    ui = ConsoleUI()
    ui.run()


if __name__ == "__main__":
    main()