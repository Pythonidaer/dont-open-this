'use strict';
(() => {
 const key = 'news-explorer-theme';
 const system = window.matchMedia('(prefers-color-scheme: dark)');
 let preference;
 try { preference = localStorage.getItem(key); } catch (_) {}
 if (!['light', 'dark'].includes(preference)) preference = null;
 function apply(theme) {
  document.documentElement.dataset.theme = theme;
  const button = document.getElementById('theme-toggle');
  if (button) button.setAttribute('aria-checked', String(theme === 'dark'));
 }
 apply(preference || (system.matches ? 'dark' : 'light'));
 system.addEventListener('change', event => {
  if (!preference) apply(event.matches ? 'dark' : 'light');
 });
 document.addEventListener('DOMContentLoaded', () => {
  apply(document.documentElement.dataset.theme);
  document.getElementById('theme-toggle').addEventListener('click', () => {
   document.documentElement.classList.add('theme-transition');
   preference = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark';
   apply(preference);
   try { localStorage.setItem(key, preference); } catch (_) {}
  });
 });
})();
