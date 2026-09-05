import subprocess
import shutil

def check_system_environment():
    results = {}

    # Проверка прав root
    results["is_root"] = (subprocess.run(["id", "-u"], capture_output=True, text=True).stdout.strip() == "0")

    # Проверка наличия docker
    results["docker_installed"] = shutil.which("docker") is not None

    # Проверка статуса контейнера remnanode
    if results["docker_installed"]:
        try:
            res = subprocess.run(
                ["docker", "inspect", "-f", "{{.State.Running}}", "remnanode"],
                capture_output=True,
                text=True
            )
            results["remnanode_running"] = (res.stdout.strip() == "true")
        except Exception:
            results["remnanode_running"] = False
    else:
        results["remnanode_running"] = False

    return results