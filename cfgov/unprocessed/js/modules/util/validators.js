/* ==========================================================================
   Validators

   Various utility functions to check if a field contains a valid value
   ========================================================================== */

'use strict';

// Required Modules
var ERROR_MESSAGES = require( '../../config/error-messages-config' );
var typeCheckers = require( '../../modules/util/type-checkers' );

// TODO: Update all the validators to return both passed and failed states
// instead of returning an empty object if the value passed

/**
 * date Determines if a field contains a valid date.
 *
 * @param {Object} field         Field to test.
 * @param {Object} currentStatus A previous tested status for the field.
 * @returns {Object} An empty object if the field passes,
 *   otherwise an object with msg and type properties if it failed.
 */
function date( field, currentStatus ) {
  var status = currentStatus || {};
  var dateRegex =
    /^\d{2}$|^\d{4}$|^\d{2}\/(?:\d{4}|\d{2})$|^\d{2}\/\d{2}\/\d{4}$/;
  if ( field.value && dateRegex.test( field.value ) === false ) {
    status.msg = status.msg || '';
    status.msg += ERROR_MESSAGES.DATE.INVALID;
    status.date = false;
  }
  return status;
}

/**
 * email Determines if a field contains an email address.
 *
 * @param {Object} field         Field to test.
 * @param {Object} currentStatus A previous tested status for the field.
 * @param {Object} options       Options object.
 * @returns {Object} An empty object if the field passes,
 *   otherwise an object with msg and type properties if it failed.
 */
function email( field, currentStatus, options ) {
  var status = currentStatus || {};
  var opts = options || {};
  var regex =
    '^[a-z0-9\u007F-\uffff!#$%&\'*+\/=?^_`{|}~-]+(?:\\.[a-z0-9' +
    '\u007F-\uffff!#$%&\'*+\/=?^_`{|}~-]+)*@(?:[a-z0-9]' +
    '(?:[a-z0-9-]*[a-z0-9])?\\.)+[a-z]{2,}$';
  var emailRegex = new RegExp( regex, 'i' );
  var emptyValidation = required( field );
  var isFilled = typeof emptyValidation.required === 'undefined' ?
                 true : emptyValidation.required;
  var state;
  var key;

  if ( !isFilled ) {
    // TODO: Create a language checker instead of doing this inline like this
    state = 'REQUIRED';
    key = opts.language === 'es' ? state + '_ES' : state;

    status.msg = status.msg || '';
    status.msg += ERROR_MESSAGES.EMAIL[key];
    status.email = false;
    status.result = state;
  } else if ( emailRegex.test( field.value ) === false ) {
    state = 'INVALID';
    key = opts.language === 'es' ? state + '_ES' : state;

    status.msg = status.msg || '';
    status.msg += ERROR_MESSAGES.EMAIL[key];
    status.email = false;
    status.result = state;
  }
  return status;
}


/**
 * phone Determines if a field contains a phone number.
 *
 * @param {Object} field         Field to test.
 * @param {Object} currentStatus A previous tested status for the field.
 * @param {Object} options       Options object.
 * @returns {Object} An empty object if the field passes,
 *   otherwise an object with msg and type properties if it failed.
 */
function phone( field, currentStatus, options ) {
  var status = currentStatus || {};
  var opts = options || {};
  // Note about the below regex: It ignores punctuation because the regex
  // checks against the field value stripped of everything but digits.
  /* eslint-disable no-inline-comments */
  var regex = '^' +        // match from the beginning of the string
              '1?' +        // optional U.S. country code of 1
              '[2-9]' +     // first digit of area code cannot be 0 or 1
              '[0-9]{2}' +  // remaining two digits of area code
              '[2-9]' +     // first digit of exchange code cannot be 0 or 1
              '[0-9]{6}' +  // remaining 6 digits
              '$';         // match to end of the string
  /* eslint-enable no-inline-comments */
  var phoneRegex = new RegExp( regex );
  var emptyValidation = required( field );
  var isFilled = typeof emptyValidation.required === 'undefined' ?
                 true : emptyValidation.required;
  var state;
  var key;

  if ( !isFilled ) {
    // TODO: Create a language checker instead of doing this inline like this
    state = 'REQUIRED';
    key = opts.language === 'es' ? state + '_ES' : state;

    status.msg = status.msg || '';
    status.msg += ERROR_MESSAGES.PHONE[key];
    status.phone = false;
    status.result = state;
  } else if ( !phoneRegex.test( field.value.replace( /[^0-9]/g, '' ) ) ) {
    state = 'INVALID';
    key = opts.language === 'es' ? state + '_ES' : state;

    status.msg = status.msg || '';
    status.msg += ERROR_MESSAGES.PHONE[key];
    status.phone = false;
    status.result = state;
  }

  return status;
}

/**
 * required Determines if a required field contains a value.
 *
 * @param {Object} field         Field to test.
 * @param {Object} currentStatus A previous tested status for the field.
 * @returns {Object} An required object if the field passes,
 *   otherwise an object with msg and type properties if it failed.
 */
 // TODO: Rename this so it's clearer it's checking a required attribute
function required( field, currentStatus ) {
  var status = currentStatus || {};
  var isRequired = field.getAttribute( 'required' ) !== null;
  if ( isRequired && typeCheckers.isEmpty( field.value ) ) {
    status.msg = status.msg || '';
    status.msg += ERROR_MESSAGES.FIELD.REQUIRED;
    status.required = false;
  }
  return status;
}

/**
 * checkbox
 * Determines if a field contains a required number of picked checkbox options.
 *
 * @param {Object} field         Field to test.
 * @param {Object} currentStatus A previous tested status for the field.
 * @param {Array}  fieldset      A list of fields related to the parent field.
 * @returns {Object} An empty object if the field passes,
 *   otherwise an object with msg and type properties if it failed.
 */
function checkbox( field, currentStatus, fieldset ) {
  var status = currentStatus || {};
  return _checkableInput( field, status, fieldset, 'checkbox' );
}

/**
 * radio Determines if a field contains a picked radio option.
 *
 * @param {Object} field         Field to test.
 * @param {Object} currentStatus A previous tested status for the field.
 * @param {Array}  fieldset      A list of fields related to the parent field.
 * @returns {Object} An empty object if the field passes,
 *   otherwise an object with msg and type properties if it failed.
 */
function radio( field, currentStatus, fieldset ) {
  var status = currentStatus || {};
  return _checkableInput( field, status, fieldset, 'radio' );
}

/**
 * _checkableInput
 * Determines if a field contains a required number of
 * picked checkbox or radio button options.
 *
 * @param {Object} field         Field to test.
 * @param {Object} currentStatus A previous tested status for the field.
 * @param {Array}  fieldset      A list of fields related to the parent field.
 * @param {string} type          Should be "radio" or "checkbox".
 * @returns {Object} An empty object if the field passes,
 *   otherwise an object with msg and type properties if it failed.
 */
function _checkableInput( field, currentStatus, fieldset, type ) {
  var statusMsg = currentStatus.msg || '';
  var required = parseInt( field.getAttribute( 'data-required' ) || 0, 10 );
  var groupFieldsLength = fieldset.length;

  if ( groupFieldsLength < required ) {
    statusMsg += ERROR_MESSAGES.CHECKBOX.REQUIRED.replace( '%s', required );
    currentStatus.msg = statusMsg;
    currentStatus[type] = false;
  }

  return currentStatus;
}

module.exports = {
  date:         date,
  email:        email,
  phone:        phone,
  required:     required,
  checkbox:     checkbox,
  radio:        radio
};
