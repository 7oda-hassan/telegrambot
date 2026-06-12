import os
import importlib
import logging

logger = logging.getLogger("telegram_bot.parsers.plugin_loader")
import pkgutil

def load_all_plugins():
    """Dynamically loads all plugins in the parsers structure to register them."""
    base_pkg = "parsers"
    packages = ["blocks", "lists", "media", "advanced", "tables", "math", "references"]
    
    for pkg in packages:
        pkg_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), pkg)
        if not os.path.exists(pkg_path):
            continue
            
        for _, module_name, _ in pkgutil.iter_modules([pkg_path]):
            try:
                importlib.import_module(f"{base_pkg}.{pkg}.{module_name}")
            except Exception as e:
                logger.error(f"Failed to load plugin {module_name}: {e}")
