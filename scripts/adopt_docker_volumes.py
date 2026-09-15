"""Закрепить существующие тома Redis/RabbitMQ без копирования или удаления данных."""

import json
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parent.parent


def docker(*args: str) -> str:
    return subprocess.check_output(
        ["docker", *args], cwd=ROOT, text=True,
    ).strip()


def main() -> None:
    override = ROOT / "docker-compose.override.yml"
    if override.exists():
        raise SystemExit(
            "docker-compose.override.yml уже существует. "
            "Сохраните его и объедините настройки вручную; файл не изменён."
        )

    config: dict = {"services": {}, "volumes": {}}
    for service, destination in (
        ("redis", "/data"), ("rabbitmq", "/var/lib/rabbitmq"),
    ):
        ids = docker("compose", "ps", "--all", "--quiet", service).splitlines()
        if not ids:
            print(f"{service}: контейнера нет; Compose создаст постоянный том.")
            continue
        if len(ids) != 1:
            raise SystemExit(f"{service}: ожидался один контейнер, найдено {len(ids)}.")
        # Не читаем и не выводим environment контейнера: там могут быть секреты.
        info = json.loads(docker(
            "inspect", "--format",
            '{"hostname":{{json .Config.Hostname}},"mounts":{{json .Mounts}}}',
            ids[0],
        ))
        mounts = [m for m in info["mounts"] if m["Destination"] == destination]
        if len(mounts) != 1 or mounts[0]["Type"] != "volume":
            raise SystemExit(f"{service}: неожиданный тип хранения; файл не изменён.")
        config["volumes"][f"{service}_data"] = {
            "external": True, "name": mounts[0]["Name"],
        }
        if service == "rabbitmq":
            config["services"][service] = {"hostname": info["hostname"]}

    if not config["volumes"]:
        print("Существующих томов для привязки нет. Изменения не требуются.")
        return
    # JSON является допустимым YAML. Режим x не перезапишет чужой override.
    with override.open("x", encoding="utf-8") as output:
        json.dump(config, output, ensure_ascii=False, indent=2)
        output.write("\n")
    print(f"Создан {override.name}. Тома и имя узла сохранены; контейнеры не изменены.")


if __name__ == "__main__":
    main()
