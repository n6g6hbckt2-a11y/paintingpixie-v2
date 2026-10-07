(function(){
  var trigs=[].slice.call(document.querySelectorAll('.marr'));
  trigs.forEach(function(b){b.addEventListener('click',function(){var open=b.getAttribute('aria-expanded')==='true';b.setAttribute('aria-expanded',String(!open));b.closest('.msec').querySelector('.msub').hidden=open;});});
  document.addEventListener('keydown',function(e){if(e.key==='Escape'&&document.activeElement&&document.activeElement.closest('.dd'))document.activeElement.blur();});
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

// GA4: count when someone starts filling in a booking form (form_start), alongside booking_request on submit
document.addEventListener('focusin', function(e) {
  var f = e.target.closest && e.target.closest('form');
  if (!f || f.dataset.started) return;
  f.dataset.started = '1';
  gtag('event', 'form_start', {'page_path': location.pathname, 'form_destination': f.action || ''});
});
