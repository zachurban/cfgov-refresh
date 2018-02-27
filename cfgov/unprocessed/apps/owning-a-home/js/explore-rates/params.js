const $ = require( '../../node_modules/jquery' );

// List all the parameters the user can change and set
// their default values.
// `verbotenKeys` are as follows:
// 9 = tab
// 37, 38, 39, 40 = arrow keys.
// 13 = enter
// 16 = shift
const params = {
  'credit-score':   700,
  'down-payment':   '20,000',
  'house-price':    '200,000',
  'loan-amount':    UNDEFINED,
  'location':       'AL',
  'rate-structure': 'fixed',
  'loan-term':      30,
  'loan-type':      'conf',
  'arm-type':       '5-1',
  'edited':         false,
  'isJumbo':        false,
  'prevLoanType':   '',
  'prevLocation':   '',
  'verbotenKeys':   [ 9, 37, 38, 39, 40, 13, 16 ],
  'update':         function() {
    this.prevLoanType = this['loan-type'];
    this.prevLocation = this.location;
    $.extend( params, _getSelections() );
  }
};


/**
 * Get values of all HTML elements in the control panel.
 * @returns {Object} Key-value hash of element ids and values.
 */
function _getSelections() {
  var selections = {};
  var ids = [];

  for ( var param in params ) {
    selections[param] = getSelection( param );
  }

  return selections;
}

export { params };
