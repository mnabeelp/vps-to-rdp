import flet as ft
import paramiko
import threading

def main(page: ft.Page):
    page.title = "VPS to RDP Wizard"
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 500
    page.window_height = 650
    page.window_resizable = True
    page.padding = 40
    page.bgcolor = "#0a0a0d"

    # --- Components ---
    header = ft.Column([
        ft.Text("VPS to RDP Wizard", size=32, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
        ft.Text("Configure your VPS instantly. No downloads required.", size=16, color=ft.colors.GREY_500),
    ], spacing=10)

    vps_ip = ft.TextField(
        label="VPS IP Address", hint_text="e.g. 192.168.1.1",
        border_color="#303033", focused_border_color=ft.colors.BLUE_400,
        text_size=16, prefix_icon=ft.icons.DNS
    )

    vps_port = ft.TextField(
        label="SSH Port", value="22", border_color="#303033",
        width=120, focused_border_color=ft.colors.BLUE_400
    )

    vps_user = ft.TextField(
        label="Username", value="root", border_color="#303033",
        focused_border_color=ft.colors.BLUE_400, prefix_icon=ft.icons.PERSON
    )

    vps_password = ft.TextField(
        label="Password", password=True, can_reveal_password=True,
        border_color="#303033", focused_border_color=ft.colors.BLUE_400,
        prefix_icon=ft.icons.LOCK
    )
    
    status_icon = ft.Icon(name=ft.icons.INFO_OUTLINE, color=ft.colors.TRANSPARENT, size=40)
    status_text = ft.Text("", size=16, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER, color=ft.colors.WHITE)
    status_container = ft.Column([status_icon, status_text], horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    progress_ring = ft.ProgressRing(width=24, height=24, stroke_width=2, color=ft.colors.BLUE_400, visible=False)

    def run_setup(e):
        if not vps_ip.value or not vps_password.value:
            page.snack_bar = ft.SnackBar(ft.Text("Please fill in all fields!"), bgcolor=ft.colors.RED_400)
            page.snack_bar.open = True
            page.update()
            return

        btn_auto.disabled = True
        progress_ring.visible = True
        status_icon.color = ft.colors.TRANSPARENT
        status_text.value = "Configuring VPS... This may take a few minutes."
        status_text.color = ft.colors.BLUE_400
        page.update()

        def ssh_thread():
            error_msg = ""
            try:
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(vps_ip.value, port=int(vps_port.value), username=vps_user.value, password=vps_password.value, timeout=15)
                
                cmd = "export DEBIAN_FRONTEND=noninteractive; sudo apt-get update && sudo apt-get install -y xfce4 xfce4-goodies xrdp && (sudo adduser xrdp ssl-cert || true) && echo 'xfce4-session' > ~/.xsession && (sudo ufw allow 3389/tcp || true) && sudo systemctl restart xrdp"
                
                stdin, stdout, stderr = ssh.exec_command(cmd)
                exit_status = stdout.channel.recv_exit_status()
                
                if exit_status != 0:
                    err = stderr.read().decode('utf-8').strip()
                    if not err:
                        err = stdout.read().decode('utf-8').strip()
                    error_msg = f"Setup failed (Code {exit_status}): {err}"
                    
                ssh.close()
            except paramiko.AuthenticationException:
                error_msg = "Authentication failed. Incorrect Username or Password."
            except Exception as ex:
                error_msg = f"Connection error: {str(ex)}"
            
            progress_ring.visible = False
            btn_auto.disabled = False
            
            if error_msg:
                status_icon.name = ft.icons.ERROR
                status_icon.color = ft.colors.RED_500
                status_text.color = ft.colors.RED_500
                
                # Trim the message if it's too long
                if len(error_msg) > 130:
                    error_msg = error_msg[:130] + "..."
                status_text.value = error_msg
            else:
                status_icon.name = ft.icons.CHECK_CIRCLE
                status_icon.color = ft.colors.GREEN_400
                status_text.color = ft.colors.GREEN_400
                status_text.value = "Success! Open 'Remote Desktop Connection' on Windows, enter your VPS IP, and log in. The machine is running fine!"
            page.update()

        threading.Thread(target=ssh_thread).start()

    btn_auto = ft.ElevatedButton(
        text="Convert VPS to RDP",
        style=ft.ButtonStyle(
            color=ft.colors.WHITE,
            bgcolor={"": ft.colors.BLUE_600, ft.MaterialState.HOVERED: ft.colors.BLUE_700},
            padding=20,
            shape=ft.RoundedRectangleBorder(radius=10)
        ),
        on_click=run_setup
    )

    # --- Layout ---
    page.add(
        header,
        ft.Divider(height=20, color="transparent"),
        ft.Container(
            content=ft.Column([
                vps_ip,
                ft.Row([vps_port, vps_user], spacing=20),
                vps_password,
            ], spacing=20),
            padding=20,
            border=ft.border.all(1, "#303033"),
            border_radius=15,
            bgcolor="#121217"
        ),
        ft.Divider(height=20, color="transparent"),
        ft.Row([progress_ring, btn_auto], alignment=ft.MainAxisAlignment.CENTER, spacing=15),
        ft.Divider(height=20, color="transparent"),
        status_container
    )

if __name__ == "__main__":
    ft.app(target=main)
