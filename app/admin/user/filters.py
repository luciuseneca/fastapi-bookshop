from app.user.db.postgres.models import UserRoleENUM, OAuthProviderENUM

class UserRoleFilterAdmin:
    title = "User Role"
    parameter_name = "role"

    def lookups(self, request, model, run_query) -> list[tuple[str, str]]:
        return [
            (role.value, role.value.capitalize())
            for role in UserRoleENUM
        ]

    async def get_filtered_query(self, stmt, value, model):
        if value:
            stmt = stmt.where(model.role == value)

        return stmt
    

class OauthProviderFilterAdmin:
    title = "Oauth"
    parameter_name = "oauth"

    def lookups(self, request, model, run_query) -> list[tuple[str, str]]:
        return [
            (provider.value, provider.value.capitalize())
            for provider in OAuthProviderENUM
        ]

    async def get_filtered_query(self, stmt, value, model):
        if value:
            stmt = stmt.where(model.oauth_provider == value)

        return stmt