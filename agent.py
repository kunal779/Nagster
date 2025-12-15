# agent.py

from agent_core import (
    load_config_file,
    save_config_file,
    verify_employee_with_backend,
    NagsterAgent,
    DEFAULT_BASE_URL,
)
from agent_ui import CompactNagsterUI, prompt_employee_id_popup


def main():
    cfg = load_config_file()
    backend_base = cfg.get("backend_base_url", DEFAULT_BASE_URL)

    employee_id = None

    # Remembered employee
    if cfg.get("remember_me") and cfg.get("employee_id"):
        emp = cfg["employee_id"]
        print("[Nagster] Using saved Employee ID:", emp)
        if verify_employee_with_backend(emp, backend_base):
            employee_id = emp
        else:
            print("[Nagster] Saved Employee ID invalid, clearing it.")
            cfg["remember_me"] = False
            cfg.pop("employee_id", None)
            save_config_file(cfg)

    # If not remembered, ask
    if not employee_id:
        employee_id, _ = prompt_employee_id_popup(cfg)
        backend_base = cfg.get("backend_base_url", backend_base)

    agent = NagsterAgent(employee_id=employee_id, config=cfg)
    ui = CompactNagsterUI(agent)
    print("[Nagster] Compact UI starting...")
    ui.run()
    print("[Nagster] UI closed.")


if __name__ == "__main__":
    main()