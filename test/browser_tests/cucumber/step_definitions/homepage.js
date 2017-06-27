'use strict'

const chai = require( 'chai' );
const chaiAsPromised = require( 'chai-as-promised' );
const { defineSupportCode } = require( 'cucumber' );
const { expect } = require( 'chai' );

const HEADER_SEL = 'h1.m-home-hero_heading';

let _dom;

defineSupportCode( function( { Then, When, Before } ) {

  Before ( function( ) {
    _dom = {
      header: element( by.css( HEADER_SEL ) ) 
    } 
  } );

  Then( 'the header should say {stringInDoubleQuotes}', function (stringInDoubleQuotes ) {
    return expect( _dom.header.getText() ).to.eventually.equal( stringInDoubleQuotes );
  } );

} );
