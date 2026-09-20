from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
from app.config import settings


def setup_swagger_ui(app: FastAPI) -> None:
    """Configures Swagger UI with an interactive Light/Dark mode toggle button."""

    # Custom CSS: Adds the floating toggle button & dark mode styling rules
    custom_css = """
    /* Floating Theme Toggle Button */
    #theme-toggle-btn {
        position: fixed;
        top: 12px;
        right: 20px;
        z-index: 9999;
        background: #2d3748;
        color: #ffffff;
        border: 1px solid #4a5568;
        border-radius: 20px;
        padding: 6px 14px;
        font-size: 13px;
        font-weight: 600;
        cursor: pointer;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
        transition: all 0.2s ease;
    }
    #theme-toggle-btn:hover {
        transform: scale(1.05);
        background: #4a5568;
    }

    /* Dark Theme Styles (Active when body has 'dark-theme' class) */
    body.dark-theme {
        background-color: #121212 !important;
        color: #e0e0e0 !important;
    }
    body.dark-theme .swagger-ui {
        filter: invert(88%) hue-rotate(180deg);
    }
    body.dark-theme .swagger-ui .highlight-code,
    body.dark-theme .swagger-ui .microlight,
    body.dark-theme #theme-toggle-btn {
        filter: invert(88%) hue-rotate(180deg);
    }
    """

    # Custom JavaScript: Handles click event and saves user choice in localStorage
    custom_js = """
    document.addEventListener("DOMContentLoaded", function() {
        const btn = document.createElement("button");
        btn.id = "theme-toggle-btn";
        
        // Read saved preference or default to Dark
        const currentTheme = localStorage.getItem("swagger_theme") || "dark";
        if (currentTheme === "dark") {
            document.body.classList.add("dark-theme");
            btn.innerHTML = "☀️ Light Mode";
        } else {
            btn.innerHTML = "🌙 Dark Mode";
        }
        
        btn.onclick = function() {
            document.body.classList.toggle("dark-theme");
            const isDark = document.body.classList.contains("dark-theme");
            localStorage.setItem("swagger_theme", isDark ? "dark" : "light");
            btn.innerHTML = isDark ? "☀️ Light Mode" : "🌙 Dark Mode";
        };

        document.body.appendChild(btn);
    });
    """

    @app.get("/docs", include_in_schema=False)
    def custom_swagger_ui_html():
        html_response = get_swagger_ui_html(
            openapi_url=app.openapi_url,  # type: ignore
            title=f"{settings.PROJECT_NAME} - Swagger UI",
            swagger_js_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js",
            swagger_css_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css",
            swagger_favicon_url="https://fastapi.tiangolo.com/img/favicon.png",
            custom_js_url="",
        )

        # Inject our custom CSS and JS into the generated Swagger HTML response
        content = html_response.body.decode("utf-8")
        injected = content.replace(
            "</head>",
            f"<style>{custom_css}</style><script>{custom_js}</script></head>",
        )

        from fastapi.responses import HTMLResponse
        return HTMLResponse(content=injected)