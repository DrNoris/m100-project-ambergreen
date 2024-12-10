from ambergreen.GUI.loginDBRepository import LoginDBRepository


class LoginService:
    def __init__(self, loginRepo: LoginDBRepository):
        self.loginRepo = loginRepo

    def login(self, username, password):
        try:
            result = self.loginRepo.login(username, password)
            return result

        except Exception as e:
            return {"success": False, "message": f"An error occurred: {str(e)}"}