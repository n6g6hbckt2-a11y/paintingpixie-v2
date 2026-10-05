(function(){
  var trigs=[].slice.call(document.querySelectorAll('.mtrig'));
  function closeAll(except){trigs.forEach(function(t){if(t!==except){t.setAttribute('aria-expanded','false');document.getElementById(t.getAttribute('aria-controls')).hidden=true;}});}
  trigs.forEach(function(t){t.addEventListener('click',function(e){e.stopPropagation();var open=t.getAttribute('aria-expanded')==='true';closeAll(t);t.setAttribute('aria-expanded',String(!open));document.getElementById(t.getAttribute('aria-controls')).hidden=open;});});
  document.addEventListener('click',function(e){if(!e.target.closest('.mega'))closeAll();});
  document.addEventListener('keydown',function(e){if(e.key==='Escape')closeAll();});
  document.querySelectorAll('.mega a').forEach(function(a){a.addEventListener('click',function(){closeAll();});});
})();

document.addEventListener('click', function(e) {
  var link = e.target.closest('a[href*="wa.me"]');
  if (link) {
    var isFloating = function(a){ return !!a.closest('.mbar') || getComputedStyle(a).position === 'fixed'; };
    var inPage = [].slice.call(document.querySelectorAll('a[href*="wa.me"]')).filter(function(a){ return !isFloating(a); });
    var pos = isFloating(link) ? 'floating' : (inPage.indexOf(link) === 0 ? 'top' : 'lower');
    gtag('event', 'whatsapp_click', {'link_url': link.href, 'page_location': location.href, 'page_path': location.pathname, 'button_position': pos, 'transport_type': 'beacon'});
  }
  var tel = e.target.closest('a[href^="tel:"]');
  if (tel) { gtag('event', 'phone_click', {'link_url': tel.href, 'page_location': location.href}); }
});
document.addEventListener('submit', function(e) {
  gtag('event', 'booking_request', {'form_destination': e.target.action || '', 'page_location': location.href, 'transport_type': 'beacon'});
});
