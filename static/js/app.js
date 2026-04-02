function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (const rawCookie of cookies) {
      const cookie = rawCookie.trim();
      if (cookie.startsWith(name + "=")) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

async function postJson(url, payload) {
  const response = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken"),
    },
    body: JSON.stringify(payload),
  });

  let data = {};
  try {
    data = await response.json();
  } catch (error) {
    data = {};
  }

  if (!response.ok) {
    throw new Error(data.message || "Request gagal diproses.");
  }

  return data;
}

window.handleCredentialResponse = async function (response) {
  try {
    const payload = await postJson(window.portalConfig.googleAuthUrl, {
      credential: response.credential,
    });

    if (payload.ok && payload.redirect) {
      window.location.href = payload.redirect;
      return;
    }

    alert(payload.message || "Login Google gagal diproses.");
  } catch (error) {
    alert(error.message || "Terjadi kendala saat login Google.");
    console.error(error);
  }
};

window.addEventListener("DOMContentLoaded", () => {
  const config = window.portalConfig || {};

  document.querySelectorAll("[data-debug-login]").forEach((button) => {
    button.addEventListener("click", async () => {
      const role = button.getAttribute("data-debug-login");
      const url = role === "editor" ? config.debugEditorUrl : config.debugViewerUrl;

      try {
        const response = await fetch(url, {
          method: "POST",
          headers: {
            "X-CSRFToken": getCookie("csrftoken"),
          },
        });

        const payload = await response.json();

        if (payload.ok && payload.redirect) {
          window.location.href = payload.redirect;
          return;
        }

        alert(payload.message || "Debug login gagal.");
      } catch (error) {
        alert("Terjadi kendala saat debug login.");
        console.error(error);
      }
    });
  });
});