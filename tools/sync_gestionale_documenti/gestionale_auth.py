"""Browser Playwright: sessione da secret o login password+TOTP."""
from __future__ import annotations

import os
from typing import TYPE_CHECKING

import pyotp
from playwright.sync_api import sync_playwright

from env_config import gestionale_base_url, has_password_login, load_config, storage_state, storage_state_path

if TYPE_CHECKING:
    from playwright.sync_api import BrowserContext, Page


def open_context():
    """Context manager: (playwright, browser, context)."""
    return _GestionaleSession()


class _GestionaleSession:
    def __enter__(self):
        self._pw = sync_playwright().start()
        self._browser = self._pw.chromium.launch(headless=True)
        sp = storage_state_path()
        if sp:
            self._context = self._browser.new_context(storage_state=sp)
            return self._pw, self._browser, self._context
        state = storage_state()
        if state:
            self._context = self._browser.new_context(storage_state=state)
            return self._pw, self._browser, self._context
        if not has_password_login():
            self._browser.close()
            self._pw.stop()
            raise SystemExit(
                "Serve GESTIONALE_STORAGE_STATE oppure GESTIONALE_USER+GESTIONALE_PASSWORD"
            )
        self._context = self._browser.new_context()
        page = self._context.new_page()
        _login_form(page)
        return self._pw, self._browser, self._context

    def __exit__(self, *args):
        self._browser.close()
        self._pw.stop()


def _login_form(page: Page) -> None:
    cfg = load_config()
    base = gestionale_base_url(cfg)
    user = os.environ["GESTIONALE_USER"].strip()
    password = os.environ["GESTIONALE_PASSWORD"]
    page.goto(base + "/", wait_until="domcontentloaded", timeout=120_000)
    # Selettori generici: adattare in config.local se il pannello usa nomi diversi
    for sel_user in ("input[name='username']", "input[name='email']", "#username", "#email"):
        if page.locator(sel_user).count():
            page.fill(sel_user, user)
            break
    for sel_pass in ("input[name='password']", "#password", "input[type='password']"):
        if page.locator(sel_pass).count():
            page.fill(sel_pass, password)
            break
    for sel_btn in ("button[type='submit']", "input[type='submit']", "button:has-text('Accedi')"):
        if page.locator(sel_btn).count():
            page.click(sel_btn)
            break
    totp_secret = os.environ.get("GESTIONALE_TOTP_SECRET", "").strip()
    if totp_secret:
        code = pyotp.TOTP(totp_secret.replace(" ", "")).now()
        for sel_otp in ("input[name='otp']", "#otp", "input[name='code']", "input[autocomplete='one-time-code']"):
            if page.locator(sel_otp).count():
                page.fill(sel_otp, code)
                page.keyboard.press("Enter")
                break
    page.wait_for_load_state("networkidle", timeout=120_000)


def fetch_page_html(context: BrowserContext, url: str) -> str:
    page = context.new_page()
    try:
        page.goto(url, wait_until="domcontentloaded", timeout=120_000)
        return page.content()
    finally:
        page.close()
