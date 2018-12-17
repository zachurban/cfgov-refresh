/* ==========================================================================
   SampleTextIndex: sample JS for setting up tests. This is not included in
   any pages in the site.
   ========================================================================== */

/**
 * Set up event handler for button to scroll to top of page.
 */
function init() {
  behavior.attach( 'return-to-top', 'click', event => {
    event.preventDefault();
    _scrollToTop();
  } );
}

export { init };
