/* ==========================================================================
   Scripts for Email Signup organism.
   ========================================================================== */

'use strict';

var FormSubmit = require( '../../organisms/FormSubmit.js' );
var validators = require( '../../modules/util/validators' );

var BASE_CLASS = 'o-email-signup';
var language = document.body.querySelector( '.content' ).lang;
var acceptPhone = document.body.querySelector( '[name="accept_phone"]' );
var validationType = acceptPhone ? 'emailOrPhone' : 'email';


/**
 * validate - Call the validation function.
 *
 * @param {Object} fields - The set of fields present in the form
 * @returns {Object} - The `status` object from the called validation function
 */
function validate( fields ) {
  var status = validators[validationType](
    fields.contact_info,
    '',
    { language: language }
  );
  return status.msg;
}


var formSubmit = new FormSubmit(
  document.body.querySelector( '.' + BASE_CLASS ),
  BASE_CLASS,
  { validator: validate, language: language }
);


formSubmit.init();
