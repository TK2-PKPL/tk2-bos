function getCsrfToken() {
  const tokenElement = document.querySelector('[name=csrfmiddlewaretoken]');
  if (tokenElement) return tokenElement.value;
  const cookieMatch = document.cookie.match(/csrftoken=([^;]+)/);
  return cookieMatch ? cookieMatch[1] : '';
}
async function postJson(url, payload) {
  const response = await fetch(url, {method:'POST', headers:{'Content-Type':'application/json','X-CSRFToken':getCsrfToken()}, body:JSON.stringify(payload)});
  return response.json();
}
window.handleCredentialResponse = async function(response) {
  try {
    const payload = await postJson(window.portalConfig.googleAuthUrl, {credential: response.credential});
    if (payload.ok && payload.redirect) {
      window.location.href = payload.redirect;
      return;
    }
    alert(payload.message || 'Login Google gagal diproses');
  } catch (error) {
    alert('Terjadi kendala saat menghubungkan login Google ke server');
  }
};
window.addEventListener('DOMContentLoaded', () => {
  const config = window.portalConfig || {};
  if (config.googleClientId && window.google?.accounts?.id) {
    google.accounts.id.initialize({client_id: config.googleClientId, callback: handleCredentialResponse});
    google.accounts.id.renderButton(document.getElementById('googleSignInButton'), {theme:'outline', size:'large', text:'signin_with', shape:'pill', width:'300'});
  }
  document.querySelectorAll('[data-debug-login]').forEach((button) => {
    button.addEventListener('click', async () => {
      const role = button.getAttribute('data-debug-login');
      const url = role === 'editor' ? config.debugEditorUrl : config.debugViewerUrl;
      const response = await fetch(url, {method:'POST', headers:{'X-CSRFToken': getCsrfToken()}});
      const payload = await response.json();
      if (payload.ok && payload.redirect) window.location.href = payload.redirect;
    });
  });
});
