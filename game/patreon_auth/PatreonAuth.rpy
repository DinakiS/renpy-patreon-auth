init python:
    @renpy.pure
    class PatreonAuth(Action):
        def __init__(self, client_id, callback_url = "/auth"):
            self.strategy = auth.OAuth2Strategy(
                authorization_url = "https://www.patreon.com/oauth2/authorize",
                token_url = "https://www.patreon.com/api/oauth2/token",
                client_id = client_id,
                callback_url = callback_url,
                scope = "identity"
            )

        def __call__(self):
            self.strategy.run(self.on_success_auth, self.on_failure_auth)

        def on_success_auth(self, tokens):
            persistent.PATREON_TOKENS = tokens

            client = PatreonClient(tokens["access_token"])

            user = client.get_user_data({"fields[user]": "full_name,image_url", "include": "memberships", "fields[member]": "patron_status,currently_entitled_amount_cents"})
            persistent.PATREON_USER_DATA = user

            renpy.restart_interaction()

        def on_failure_auth(self):
            renpy.notify("Failed to authenticate with Patreon.")
