'use strict';

const chai = require( 'chai' );
const expect = chai.expect;
const jsdom = require( 'mocha-jsdom' );
const BASE_JS_PATH = '../../../../cfgov/unprocessed/js/';
const ERROR_MESSAGES = require( BASE_JS_PATH + 'config/error-messages-config' );
const validators = require( BASE_JS_PATH + 'modules/util/validators.js' );
let testField;
let returnedObject;

describe( 'Date field validator', () => {
  jsdom();

  beforeEach( () => {
    testField = document.createElement( 'input' );
  } );

  it( 'should return an empty object for a valid date', () => {
    testField.value = '11/12/2007';
    returnedObject = validators.date( testField );

    expect( returnedObject ).to.be.empty;
  } );

  it( 'should return an error object for a malformed date', () => {
    testField.value = '11-12-07';
    returnedObject = validators.date( testField );

    expect( returnedObject ).to.have.property( 'date', false );
    expect( returnedObject )
      .to.have.property( 'msg', ERROR_MESSAGES.DATE.INVALID );
  } );

  it( 'should return an error object for a UTC date', () => {
    testField.value = new Date( 2007, 11, 12 );
    returnedObject = validators.date( testField );

    expect( returnedObject ).to.have.property( 'date', false );
    expect( returnedObject )
      .to.have.property( 'msg', ERROR_MESSAGES.DATE.INVALID );
  } );
} );

describe( 'Email field validator', () => {
  jsdom();

  beforeEach( () => {
    testField = document.createElement( 'input' );
  } );

  it( 'should return an empty object for a valid email', () => {
    testField.value = 'test@demo.com';
    returnedObject = validators.email( testField );

    expect( returnedObject ).to.be.empty;
  } );

  it( 'should return an error message for an empty field', () => {
    testField.setAttribute( 'required', '' );
    testField.value = '';
    returnedObject = validators.email( testField );

    expect( returnedObject )
      .to.have.property( 'msg', ERROR_MESSAGES.EMAIL.REQUIRED );
  } );

  it( 'should return a Spanish-specific error message for an empty field', () => {
    testField.setAttribute( 'required', '' );
    testField.value = '';
    returnedObject = validators.email(
      testField,
      null,
      { 'language': 'es' }
    );

    expect( returnedObject )
      .to.have.property( 'msg', ERROR_MESSAGES.EMAIL.REQUIRED_ES );
  } );

  it( 'should return an error message for a missing domain', () => {
    testField.value = 'test';
    returnedObject = validators.email( testField );

    expect( returnedObject ).to.have.property( 'email', false );
    expect( returnedObject )
      .to.have.property( 'msg', ERROR_MESSAGES.EMAIL.INVALID );
  } );

  it( 'should return a Spanish-specific error message for a missing domain',
    () => {
      testField.value = 'test';
      returnedObject = validators.email(
        testField,
        null,
        { 'language': 'es' }
      );

      expect( returnedObject ).to.have.property( 'email', false );
      expect( returnedObject )
        .to.have.property( 'msg', ERROR_MESSAGES.EMAIL.INVALID_ES );
    }
  );

  it( 'should return an error message for a missing user', () => {
    testField.value = '@demo.com';
    returnedObject = validators.email( testField );

    expect( returnedObject ).to.have.property( 'email', false );
    expect( returnedObject )
      .to.have.property( 'msg', ERROR_MESSAGES.EMAIL.INVALID );
  } );
} );

describe( 'Phone number field validator', () => {
  jsdom();

  beforeEach( () => {
    testField = document.createElement( 'input' );
  } );

  it( 'should return an empty object for a valid phone number', () => {
    testField.value = '2345678901';
    returnedObject = validators.phone( testField );

    expect( returnedObject ).to.be.empty;
  } );

  it( 'should return an empty object for a valid phone number using spaces',
    () => {
      testField.value = '567 890 1234';
      returnedObject = validators.phone( testField );

      expect( returnedObject ).to.be.empty;
    }
  );

  it( 'should return an empty object for a valid phone number using dashes',
    () => {
      testField.value = '890-723-4567';
      returnedObject = validators.phone( testField );

      expect( returnedObject ).to.be.empty;
    }
  );

  it( 'should return an empty object for a valid phone number ' +
    'using mixed separators',
    () => {
      testField.value = '(345) 678-9012';
      returnedObject = validators.phone( testField );

      expect( returnedObject ).to.be.empty;
    }
  );

  it( 'should return an empty object for a valid phone number ' +
    'using a US country code',
    () => {
      testField.value = '12345678901';
      returnedObject = validators.phone( testField );

      expect( returnedObject ).to.be.empty;
    }
  );

  it( 'should return an error message for an empty field', () => {
    testField.setAttribute( 'required', '' );
    testField.value = '';
    returnedObject = validators.phone( testField );

    expect( returnedObject )
      .to.have.property( 'msg', ERROR_MESSAGES.PHONE.REQUIRED );
  } );

  it( 'should return a Spanish-specific error message for an empty field',
    () => {
      testField.setAttribute( 'required', '' );
      testField.value = '';
      returnedObject = validators.phone(
        testField,
        null,
        { 'language': 'es' }
      );

      expect( returnedObject )
        .to.have.property( 'msg', ERROR_MESSAGES.PHONE.REQUIRED_ES );
    }
  );

  it( 'should return an error message for a area code starting with 0',
    () => {
      testField.value = '0123456789';
      returnedObject = validators.phone( testField );

      expect( returnedObject ).to.have.property( 'phone', false );
      expect( returnedObject )
        .to.have.property( 'msg', ERROR_MESSAGES.PHONE.INVALID );
    }
  );

  it( 'should return a Spanish-specific error message for a area code ' +
    'starting with 0',
    () => {
      testField.value = '0123456789';
      returnedObject = validators.phone(
        testField,
        null,
        { 'language': 'es' }
      );

      expect( returnedObject ).to.have.property( 'phone', false );
      expect( returnedObject )
        .to.have.property( 'msg', ERROR_MESSAGES.PHONE.INVALID_ES );
    }
  );

  it( 'should return an error message for a area code starting with 1',
    () => {
      testField.value = '1234567890';
      returnedObject = validators.phone( testField );

      expect( returnedObject ).to.have.property( 'phone', false );
      expect( returnedObject )
        .to.have.property( 'msg', ERROR_MESSAGES.PHONE.INVALID );
    }
  );

  it( 'should return an error message for an exchange code starting with 0',
    () => {
      testField.value = '4560129876';
      returnedObject = validators.phone( testField );

      expect( returnedObject ).to.have.property( 'phone', false );
      expect( returnedObject )
        .to.have.property( 'msg', ERROR_MESSAGES.PHONE.INVALID );
    }
  );

  it( 'should return an error message for an exchange code starting with 1',
    () => {
      testField.value = '4561029876';
      returnedObject = validators.phone( testField );

      expect( returnedObject ).to.have.property( 'phone', false );
      expect( returnedObject )
        .to.have.property( 'msg', ERROR_MESSAGES.PHONE.INVALID );
    }
  );
} );

describe( 'Required field validator', () => {
  jsdom();

  beforeEach( () => {
    testField = document.createElement( 'input' );
    testField.setAttribute( 'required', '' );
  } );

  it( 'should return an empty object for a filed field', () => {
    testField.value = 'testing';
    returnedObject = validators.required( testField );

    expect( returnedObject ).to.be.empty;
  } );

  it( 'should return an error message for am empty field', () => {
    testField.value = '';
    returnedObject = validators.required( testField );

    expect( returnedObject ).to.have.property( 'required', false );
    expect( returnedObject )
      .to.have.property( 'msg', ERROR_MESSAGES.FIELD.REQUIRED );
  } );
} );

describe( 'Checkbox field validator', () => {
  jsdom();

  beforeEach( () => {
    testField = document.createElement( 'label' );
    testField.setAttribute( 'name', 'test-checkboxes' );
    testField.setAttribute( 'data-required', '2' );
  } );

  it( 'should return an empty object ' +
      'when total checkboxes equals required total', () => {
    const fieldset = [
      document.createElement( 'input' ),
      document.createElement( 'input' )
    ];
    returnedObject = validators.checkbox( testField, null, fieldset );

    expect( returnedObject ).to.be.empty;
  } );

  it( 'should return an empty object ' +
      'when total checkboxes is more than required total', () => {
    const fieldset = [
      document.createElement( 'input' ),
      document.createElement( 'input' ),
      document.createElement( 'input' )
    ];
    returnedObject = validators.checkbox( testField, null, fieldset );

    expect( returnedObject ).to.be.empty;
  } );

  it( 'should return an error message ' +
       'when total checkboxes is less than required total', () => {
    const fieldset = [
      document.createElement( 'input' )
    ];
    returnedObject = validators.checkbox( testField, null, fieldset );

    expect( returnedObject ).to.have.property( 'checkbox', false );
    expect( returnedObject ).to.have.property(
      'msg', ERROR_MESSAGES.CHECKBOX.REQUIRED.replace( '%s', '2' )
    );
  } );

  it( 'should return an empty object when required total is empty', () => {
    testField.removeAttribute( 'data-required' );
    const fieldset = [
      document.createElement( 'input' )
    ];
    returnedObject = validators.checkbox( testField, null, fieldset );

    expect( returnedObject ).to.be.empty;
  } );
} );

describe( 'Radio field validator', () => {
  jsdom();

  beforeEach( function() {
    testField = document.createElement( 'label' );
    testField.setAttribute( 'name', 'test-radios' );
    testField.setAttribute( 'data-required', '1' );
  } );

  it( 'should return an empty object ' +
      'when total radios equals required total', () => {
    const fieldset = [
      document.createElement( 'input' )
    ];
    returnedObject = validators.radio( testField, null, fieldset );

    expect( returnedObject ).to.be.empty;
  } );

  it( 'should return an empty object ' +
      'when total radios is more than required total', () => {
    const fieldset = [
      document.createElement( 'input' ),
      document.createElement( 'input' )
    ];
    returnedObject = validators.radio( testField, null, fieldset );

    expect( returnedObject ).to.be.empty;
  } );

  it( 'should return an error message ' +
      'when total checkboxes is less than required total', () => {
    const fieldset = [];
    returnedObject = validators.radio( testField, null, fieldset );

    expect( returnedObject ).to.have.property( 'radio', false );
    expect( returnedObject ).to.have.property(
      'msg', ERROR_MESSAGES.CHECKBOX.REQUIRED.replace( '%s', '1' )
    );
  } );

  it( 'should return an empty object ' +
      'when required total is empty', () => {
    testField.removeAttribute( 'data-required' );
    const fieldset = [
      document.createElement( 'input' )
    ];
    returnedObject = validators.radio( testField, null, fieldset );

    expect( returnedObject ).to.be.empty;
  } );
} );
