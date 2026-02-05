from password_manager.utils.clipboard import copy_to_clipboard


def test_clipboard_copy(monkeypatch):
    captured = {}

    monkeypatch.setattr(
            "pyperclip.copy",
            lambda x: captured.update(value = x)
    )

    copy_to_clipboard("Password123!")
    assert captured["value"] == "Password123!"

    copy_to_clipboard("Password123!", True)
    assert captured["value"] == "Password123"
