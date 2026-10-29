/* Nonmodal disclosure adapted from design-practice navigation-v5.js. */
(()=>{
 'use strict';
 const header=document.querySelector('.site-header');
 const toggle=document.getElementById('nav-toggle');
 const links=document.getElementById('site-navigation');
 const compact=matchMedia('(max-width: 1080px)');
 document.documentElement.classList.add('nav-enhanced');
 function setNavigation(open,returnFocus=false){
  const expanded=compact.matches&&open;
  links.classList.toggle('is-open',expanded);
  toggle.setAttribute('aria-expanded',String(expanded));
  toggle.setAttribute('aria-label',expanded?'Close navigation':'Open navigation');
  links.inert=compact.matches&&!expanded;
  if(returnFocus&&compact.matches)toggle.focus({preventScroll:true});
 }
 setNavigation(false);
 toggle.addEventListener('click',()=>setNavigation(toggle.getAttribute('aria-expanded')!=='true'));
 links.addEventListener('click',event=>{if(event.target.closest('a'))setNavigation(false,true)});
 document.addEventListener('keydown',event=>{if(event.key==='Escape'&&toggle.getAttribute('aria-expanded')==='true'){event.preventDefault();setNavigation(false,true)}});
 document.addEventListener('click',event=>{if(!event.target.closest('.site-header'))setNavigation(false)});
 document.addEventListener('focusin',event=>{if(!event.target.closest('.site-header'))setNavigation(false)});
 compact.addEventListener('change',()=>{
  const focusWasInLinks=links.contains(document.activeElement);
  setNavigation(false,focusWasInLinks&&compact.matches);
 });
 const updateHeader=()=>header.classList.toggle('is-scrolled',window.scrollY>8);
 updateHeader();window.addEventListener('scroll',updateHeader,{passive:true});
})();
