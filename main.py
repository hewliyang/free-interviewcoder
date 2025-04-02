import os
import uuid
from datetime import datetime, timedelta

import supabase
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table

# Load environment variables
load_dotenv()

# Initialize Rich console
console = Console()


class SubscriptionManager:
    def __init__(self):
        self.supabase_url = os.getenv("SUPABASE_URL")
        self.supabase_key = os.getenv("SUPABASE_KEY")

        if not self.supabase_url or not self.supabase_key:
            console.print(
                Panel(
                    "[bold red]Error: Missing Supabase credentials![/bold red]\n"
                    "Please ensure SUPABASE_URL and SUPABASE_KEY are set in your .env file."
                ),
                justify="center",
            )
            exit(1)

        try:
            self.supabase = supabase.create_client(self.supabase_url, self.supabase_key)
            self.user = None
        except Exception as e:
            console.print(
                Panel(
                    f"[bold red]Error connecting to Supabase:[/bold red] {str(e)}\n"
                    "Please check your Supabase credentials."
                ),
                justify="center",
            )
            exit(1)

    def sign_up_user(self, email, password):
        try:
            sign_up_resp = self.supabase.auth.sign_up(
                {
                    "email": email,
                    "password": password,
                    "options": {"data": {"email_confirmed": True}},
                }
            )
            self.user = sign_up_resp.user
            return True
        except Exception as e:
            console.print(f"[bold red]Error during sign up:[/bold red] {str(e)}")
            return False

    def sign_in_user(self, email, password):
        try:
            sign_in_resp = self.supabase.auth.sign_in_with_password(
                {
                    "email": email,
                    "password": password,
                }
            )
            self.user = sign_in_resp.user
            return True
        except Exception as e:
            console.print(f"[bold red]Error during sign in:[/bold red] {str(e)}")
            return False

    def create_subscription(self, plan="monthly", preferred_language="python"):
        if not self.user:
            console.print(
                "[bold red]Error:[/bold red] User must be signed in to create a subscription"
            )
            return False

        now = datetime.now()
        end_date = now + timedelta(days=30)

        subscription_data = {
            "id": str(uuid.uuid4()),
            "user_id": self.user.id,
            "stripe_customer_id": f"cus_{uuid.uuid4().hex[:8]}",
            "stripe_subscription_id": f"sub_{uuid.uuid4().hex[:8]}",
            "status": "active",
            "plan": plan,
            "current_period_start": now.isoformat(),
            "current_period_end": end_date.isoformat(),
            "preferred_language": preferred_language,
        }

        try:
            self.supabase.table("subscriptions").insert(subscription_data).execute()
            return True, end_date
        except Exception as e:
            console.print(f"[bold red]Error creating subscription:[/bold red] {str(e)}")
            return False, None


def display_welcome():
    console.print(
        Panel.fit(
            "[bold blue]Welcome to InterviewCoder Subscription Manager[/bold blue]\n\n"
            "This tool helps you sign up for a new account with a 30-day subscription\n"
            "or activate a subscription with your existing account.",
            title="✨ InterviewCoder ✨",
            border_style="blue",
        ),
        justify="center",
    )


def display_success(email, end_date):
    table = Table(show_header=False, box=None)
    table.add_column(style="bold green")
    table.add_column()

    table.add_row("Email:", email)
    table.add_row("Status:", "Active")
    table.add_row("Plan:", "Monthly")
    table.add_row("Expires:", end_date.strftime("%B %d, %Y"))

    console.print(
        Panel(
            table,
            title="[bold green]✅ Subscription Activated![/bold green]",
            border_style="green",
        ),
        justify="center",
    )


def main():
    try:
        display_welcome()

        manager = SubscriptionManager()

        # Ask if user is new or existing
        user_type = Prompt.ask(
            "\n[bold]Are you a new or existing user?[/bold]",
            choices=["new", "existing"],
            default="new",
        )

        # Get email
        email = Prompt.ask("\n[bold]Enter your email[/bold]")

        # Get password
        password = Prompt.ask("[bold]Enter your password[/bold]", password=True)

        # Process user authentication
        success = False
        if user_type == "new":
            # For new users, sign them up
            with console.status("[bold blue]Creating account...[/bold blue]") as status:
                success = manager.sign_up_user(email, password)

            if success:
                console.print("\n[green]Account created successfully![/green]")
            else:
                console.print(
                    "\n[bold red]Failed to create account. Please try again.[/bold red]"
                )
                return
        else:
            # For existing users, sign them in
            with console.status("[bold blue]Logging in...[/bold blue]") as status:
                success = manager.sign_in_user(email, password)

            if not success:
                console.print(
                    "\n[bold red]Login failed. Please check your credentials.[/bold red]"
                )
                return

        # Ask for preferred programming language
        languages = ["python", "javascript", "typescript", "java", "c++", "go", "rust"]
        lang = Prompt.ask(
            "\n[bold]Choose your preferred programming language[/bold]",
            choices=languages,
            default="python",
        )

        # Create subscription
        with console.status(
            "[bold blue]Activating subscription...[/bold blue]"
        ) as status:
            success, end_date = manager.create_subscription(preferred_language=lang)

        if success:
            # Display success message
            display_success(email, end_date)
        else:
            console.print(
                "\n[bold red]Failed to activate subscription. Please try again.[/bold red]"
            )

    except KeyboardInterrupt:
        console.print("\n\n[yellow]Process canceled by user.[/yellow]")
    except Exception as e:
        console.print(
            f"\n\n[bold red]An unexpected error occurred:[/bold red] {str(e)}"
        )


if __name__ == "__main__":
    main()
