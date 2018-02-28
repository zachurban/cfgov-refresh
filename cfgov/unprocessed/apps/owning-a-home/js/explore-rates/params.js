const domValues = require( './dom-values' );
const $ = require( '../../node_modules/jquery' );

let UNDEFINED;

// List all the parameters the user can change and set
// their default values.
// `verbotenKeys` are as follows:
// 9 = tab
// 37, 38, 39, 40 = arrow keys.
// 13 = enter
// 16 = shift
const _params = {
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
  'verbotenKeys':   [ 9, 37, 38, 39, 40, 13, 16 ]
};

function setVal( key, val ) {
  _params[key] = val;
}

function getVal( key ) {
  return _params[key];
}

function update() {
  _params.prevLoanType = _params['loan-type'];
  _params.prevLocation = _params.location;

  let val;
  for ( const param in _params ) {
    val = domValues.getSelection( param );
    if ( param !== 'prevLoanType' &&
         param !== 'prevLocation' &&
         val !== UNDEFINED &&
         val !== null ) {
      _params[param] = domValues.getSelection( param );
    }
  }
}

module.exports = {
  setVal: setVal,
  getVal: getVal,
  update: update
};
