import structlog

log = structlog.get_logger()

class EmailService:
    async def send_password_reset_email(self, *, email_to: str, reset_token: str):
        """
        This is the DEVELOPMENT version of the email service.
        It simulates sending an email by logging the reset link to the console.
        """
        
        frontend_url = "http://localhost:3000"
        reset_link = f"{frontend_url}/reset-password?token={reset_token}"
        
        print("="*80)
        log.info("📧  SENDING PASSWORD RESET EMAIL (SIMULATED) 📧")
        log.info(f"Recipient: {email_to}")
        log.info(f"Reset Link: {reset_link}")
        log.info("👆 COPY THE LINK ABOVE TO TEST THE PASSWORD RESET FLOW 👆")
        print("="*80)

email_service = EmailService()