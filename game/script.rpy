define e = Character("Eileen")

label start:
    scene bg room
    show eileen happy

    if persistent.PATREON_USER_DATA:
        $ full_name = persistent.PATREON_USER_DATA.get("data").get("attributes").get("full_name")
        e "Hello, [full_name]!"
        e "Looks like you successfully authenticated with Patreon."
    else:
        e "Hello, Anon."
        e "Try to click on the \"Auth with Patreon\" button in the main menu and start the game again. "

    return
