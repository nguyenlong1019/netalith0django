// Base JavaScript
// static/js/tw-config.js
tailwind.config = {
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        primary: {50:'#eff6ff',100:'#dbeafe',200:'#bfdbfe',300:'#93c5fd',
                  400:'#60a5fa',500:'#3b82f6',600:'#2563eb',
                  700:'#1d4ed8',800:'#1e40af',900:'#1e3a8a',950:'#172554'}
      }
    },
    fontFamily: {
      body: ['Inter','ui-sans-serif','system-ui','-apple-system','Segoe UI','Roboto','Helvetica Neue','Arial','Noto Sans','sans-serif','Apple Color Emoji','Segoe UI Emoji','Segoe UI Symbol','Noto Color Emoji'],
      sans: ['Inter','ui-sans-serif','system-ui','-apple-system','Segoe UI','Roboto','Helvetica Neue','Arial','Noto Sans','sans-serif','Apple Color Emoji','Segoe UI Emoji','Segoe UI Symbol','Noto Color Emoji']
    }
  }
}

function refreshToken() { 
  const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  fetch('/api/v1/auth/refresh', {
    method: 'POST', 
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrftoken,
    }
  })
  .then(res => {
    if (res.status === 200)
      return true;
    else
      return false;
  })
  .catch(error => {
    console.error(error);
    return false;
  });
}
