import inquirer



def startMenu(authenticated : bool = False):
    actions = [
        inquirer.List(
            "choice",
            message="Select an action:",
            choices=["Authenticate" if not authenticated else "Read Emails", "Exit"]
        )
    ]

    answers = inquirer.prompt(actions)

    return answers['choice']